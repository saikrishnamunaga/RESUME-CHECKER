import os
from flask import current_app, flash, redirect, render_template, request, send_from_directory, url_for

from flask_login import current_user, login_required


from . import dashboard_bp
from app.forms import ResumeUploadForm
from app.models import Resume, Report
from app.services.resume_service import analyze_resume_text, export_updated_resume, extract_resume_text, generate_improvement_suggestions, export_updated_docx, export_updated_pdf
from app.services.gemini_service import rewrite_resume_with_gemini
from app.utils.file_utils import save_uploaded_file
from app.extensions import db


@dashboard_bp.route('/')
@login_required
def dashboard_home():
    resume = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.uploaded_at.desc()).first()
    report = None
    if resume:
        report = Report.query.filter_by(resume_id=resume.id).order_by(Report.created_at.desc()).first()

    form = ResumeUploadForm()
    return render_template('dashboard/index.html', form=form, resume=resume, report=report)


@dashboard_bp.route('/upload', methods=['POST'])
@login_required
def upload_resume():
    form = ResumeUploadForm()
    if form.validate_on_submit():
        upload_folder = current_app.config['UPLOAD_FOLDER']
        filepath = save_uploaded_file(form.resume_file.data, upload_folder)
        text = extract_resume_text(filepath)

        previous_resume = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.uploaded_at.desc()).first()
        if previous_resume:
            Report.query.filter_by(resume_id=previous_resume.id).delete(synchronize_session=False)
            db.session.delete(previous_resume)
            db.session.commit()

        resume = Resume(
            user_id=current_user.id,
            filename=form.resume_file.data.filename,
            filepath=filepath,
            text=text,
        )
        db.session.add(resume)
        db.session.commit()

        analysis = analyze_resume_text(text, form.job_description.data.strip() or None)
        report = Report(
            resume_id=resume.id,
            user_id=current_user.id,
            score=min(100, max(0, int((analysis['word_count'] / 50) + analysis['skill_count'] * 10 + analysis.get('match_score', 0) / 2))),
            details=analysis,
        )
        db.session.add(report)
        db.session.commit()

        flash('Resume uploaded and analyzed successfully. Your latest CV is now updated.', 'success')
        return redirect(url_for('dashboard.dashboard_home'))

    flash('Failed to upload resume. Please provide a valid PDF or DOCX file.', 'danger')
    return redirect(url_for('dashboard.dashboard_home'))


@dashboard_bp.route('/improve', methods=['POST'])
@login_required
def improve_resume():
    resume = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.uploaded_at.desc()).first()
    if not resume:
        flash('Upload a resume first before requesting improvements.', 'warning')
        return redirect(url_for('dashboard.dashboard_home'))

    job_description = request.form.get('job_description', '').strip() or None
    suggestions = generate_improvement_suggestions(resume.text or '', job_description)
    export_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(export_dir, exist_ok=True)
    export_path = os.path.join(export_dir, f"updated_resume_{current_user.id}.txt")
    export_updated_resume(export_path, resume.text or '', job_description)

    flash('Suggestions created and a downloadable updated resume draft is ready.', 'success')
    return redirect(url_for('dashboard.dashboard_home'))


@dashboard_bp.route('/api/resume/edit', methods=['POST'])
@login_required
def api_edit_resume():
    payload = request.get_json(silent=True) or {}
    job_description = (payload.get('job_description') or '').strip() or None
    if not job_description:
        return {
            'ok': False,
            'error': 'job_description is required',
        }, 400

    resume_id = payload.get('resume_id')
    resume_query = Resume.query.filter_by(user_id=current_user.id)
    if resume_id is not None:
        resume_query = resume_query.filter_by(id=resume_id)
    resume = resume_query.order_by(Resume.uploaded_at.desc()).first()

    if not resume:
        return {
            'ok': False,
            'error': 'No resume found for this user',
        }, 404

    # Use Gemini once to produce the edited resume.
    try:
        edited = rewrite_resume_with_gemini(
            resume_text=resume.text or '',
            job_description=job_description,
        )
    except Exception as e:
        return {'ok': False, 'error': f'Gemini rewrite failed: {str(e)}'}, 400

    # Keep existing suggestion logic (non-ATS logic) unchanged.
    suggestions = generate_improvement_suggestions(resume.text or '', job_description)

    # Provide minimal ATS scoring fields too (frontend may expect them in future updates).
    ats_before = analyze_resume_text(resume.text or '', job_description).get('match_score', 0)
    ats_after = analyze_resume_text(edited, job_description).get('match_score', 0)

    # Preserve response shape.
    return {
        'ok': True,
        'resume_id': resume.id,
        'original': resume.text or '',
        'edited': edited,
        'suggestions': suggestions,
        'ats_score_before': ats_before,
        'ats_score_after': ats_after,
        'download_url': url_for('dashboard.download_updated_resume', _external=True),
    }, 200


@dashboard_bp.route('/api/resume/accept', methods=['POST'])
@login_required
def api_accept_resume():
    """Accept an edited resume and return an optimized file as DOCX or PDF."""
    payload = request.get_json(silent=True) or {}

    original_resume = (payload.get('original_resume') or '').strip()
    edited_resume = (payload.get('edited_resume') or '').strip()
    job_description = (payload.get('job_description') or '').strip() or None
    output_format = (payload.get('output_format') or payload.get('format') or '').strip().lower()

    if not edited_resume:
        return {'ok': False, 'error': 'edited_resume is required'}, 400
    if not output_format:
        return {'ok': False, 'error': 'output_format/format is required'}, 400
    if output_format not in {'docx', 'pdf'}:
        return {'ok': False, 'error': 'output_format/format must be one of: docx, pdf'}, 400


    # Generate a final optimized resume from the edited resume text.
    optimized_text = edited_resume
    if job_description:
        # Re-run the existing builder so structure/headings match the app's current conventions.
        from app.services.resume_service import build_updated_resume_text
        optimized_text = build_updated_resume_text(edited_resume, job_description)

    export_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(export_dir, exist_ok=True)

    filename = 'Resume_Optimized.docx' if output_format == 'docx' else 'Resume_Optimized.pdf'
    export_path = os.path.join(export_dir, filename)

    try:
        if output_format == 'docx':
            from app.services.resume_service import export_updated_docx
            export_updated_docx(export_path, optimized_text)
        else:
            from app.services.resume_service import export_updated_pdf
            export_updated_pdf(export_path, optimized_text)
    except Exception as e:
        return {'ok': False, 'error': f'File generation failed: {str(e)}'}, 400

    # Return generated file as attachment.
    from flask import send_file
    return send_file(export_path, as_attachment=True, download_name=filename)




@dashboard_bp.route('/download-updated-resume')
@login_required
def download_updated_resume():

    export_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"updated_resume_{current_user.id}.txt")
    if not os.path.exists(export_path):
        flash('No updated resume draft is available yet.', 'warning')
        return redirect(url_for('dashboard.dashboard_home'))
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], f"updated_resume_{current_user.id}.txt", as_attachment=True)


@dashboard_bp.route('/profile')
@login_required
def profile():
    reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.created_at.desc()).limit(5).all()
    return render_template('dashboard/profile.html', reports=reports)


@dashboard_bp.route('/reports')
@login_required
def reports():
    reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.created_at.desc()).all()
    return render_template('dashboard/reports.html', reports=reports)
