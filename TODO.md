# TODO (AI Resume project)

- [ ] 1) Implement backend minimal API changes:
  - [ ] Update `POST /dashboard/api/resume/edit` to return the exact response shape expected by the frontend:
    - [ ] `ats_score_before`, `ats_score_after`
    - [ ] `original`, `edited`
    - [ ] `suggestions`
  - [ ] Update `POST /dashboard/api/resume/accept` to accept JSON:
    - [ ] `original` resume text
    - [ ] `edited` resume text
    - [ ] `format` = `pdf` or `docx`
    - [ ] Generate DOCX via `python-docx` and PDF via `reportlab`
    - [ ] Return generated file via downloadable response (Content-Disposition)

- [ ] 2) Gemini integration debug & hardening:
  - [ ] Add startup validation for `GEMINI_API_KEY` (missing/empty) and log only first 6 chars
  - [ ] Distinguish missing vs invalid API key / unsupported model / network/API errors
  - [ ] Validate SDK usage (`google.genai` vs `google.generativeai`) and initialize correct client
  - [ ] Validate model name and supported models
  - [ ] Ensure `.env` is loaded correctly via python-dotenv

- [ ] 3) Implement service helpers in `app/services/resume_service.py`:
  - [ ] Add small helper(s) to export DOCX/PDF from the updated text
  - [ ] Keep existing `.txt` export intact

- [ ] 4) Frontend UI updates:
  - [ ] `templates/dashboard/index.html`
    - [ ] Add before/after comparison panel
    - [ ] Add suggestions panel
    - [ ] Add ATS before/after display
    - [ ] Add format selector (pdf/docx)
    - [ ] Add loading spinners and download buttons
    - [ ] Update Accept button to trigger accept API and reveal downloads
  - [ ] `static/js/main.js`
    - [ ] Update workflow:
      - [ ] Get suggestions via `/dashboard/api/resume/edit`
      - [ ] Render original/edited/suggestions/ATS before-after
      - [ ] Accept changes via `/dashboard/api/resume/accept` with JSON: original, edited, format
      - [ ] Trigger automatic download of `Resume_Optimized.docx` or `Resume_Optimized.pdf`
      - [ ] Add proper loading/disable-enable states

- [ ] 5) Smoke test
  - [ ] Run `pytest` (or existing tests/test_basic.py)
  - [ ] Start backend and manually verify /dashboard workflow:
    - [ ] Edit populates all panels
    - [ ] Accept downloads correct DOCX/PDF

