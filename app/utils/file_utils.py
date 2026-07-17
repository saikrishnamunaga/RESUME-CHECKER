import os
from werkzeug.utils import secure_filename


def allowed_file(filename: str, allowed_extensions=None) -> bool:
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    allowed_extensions = allowed_extensions or {'pdf', 'docx'}
    return ext in allowed_extensions


def save_uploaded_file(file_storage, upload_folder: str) -> str:
    filename = secure_filename(file_storage.filename)
    filepath = os.path.join(upload_folder, filename)
    os.makedirs(upload_folder, exist_ok=True)
    file_storage.save(filepath)
    return filepath
