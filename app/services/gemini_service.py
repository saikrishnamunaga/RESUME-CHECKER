import os
import re
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


# Load environment variables from the project root .env (if present).
# Explicitly set path so we don't depend on current working directory.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
load_dotenv(dotenv_path=os.path.join(_PROJECT_ROOT, ".env"))


@dataclass(frozen=True)
class GeminiConfig:
    api_key: str
    model: str = "gemini-1.5-pro"


class GeminiIntegrationError(RuntimeError):
    """Base class for Gemini integration errors."""


class GeminiMissingApiKeyError(GeminiIntegrationError):
    pass


class GeminiInvalidApiKeyError(GeminiIntegrationError):
    pass


class GeminiUnsupportedModelError(GeminiIntegrationError):
    pass


class GeminiApiRequestError(GeminiIntegrationError):
    pass


def _validate_api_key_or_raise() -> str:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        # Required by task: clear startup validation.
        raise GeminiMissingApiKeyError("GEMINI_API_KEY is missing or empty")

    # Required by task: log only first 6 characters.
    preview = api_key[:6]
    print(f"[Gemini] GEMINI_API_KEY loaded, prefix={preview}...")

    return api_key


def _get_config() -> GeminiConfig:
    api_key = _validate_api_key_or_raise()
    return GeminiConfig(api_key=api_key)





def _detect_supported_sdk_model_prefixes(model_name: str) -> str:
    """Best-effort guard to distinguish unsupported model names.

    Note: We can't guarantee full model availability without calling
    the API. This is still useful to fail fast and return a clear
    unsupported-model error.
    """
    allowed_prefixes = (
        "gemini-1.5",
        "gemini-1.0",
        "gemini-2.",
    )
    if not model_name or not any(model_name.startswith(p) for p in allowed_prefixes):
        raise GeminiUnsupportedModelError(f"Unsupported/unknown Gemini model: {model_name}")
    return model_name




def rewrite_resume_with_gemini(*, resume_text: str, job_description: str, model: Optional[str] = None) -> str:

    """Rewrite resume text to match job description using Gemini.

    Returns: improved resume text only (markdown/plain text).
    """
    cfg = _get_config()
    model_name = model or cfg.model

    # google-genai is the current official SDK name.
    try:
        from google import genai
    except Exception as e:
        raise RuntimeError(
            "google-genai SDK is required. Install with: pip install google-genai"
        ) from e

    client = genai.Client(api_key=cfg.api_key)

    prompt = (
        "You are an expert ATS Resume Writer and Career Coach.\n\n"
        "Rewrite the user's resume to match the given job description.\n\n"
        "Rules:\n"
        "* Never invent experience, education, skills, certifications, or projects.\n"
        "* Do not add fake companies or achievements.\n"
        "* Preserve all factual information.\n"
        "* Rewrite bullet points using strong action verbs.\n"
        "* Improve grammar and professional wording.\n"
        "* Include relevant ATS keywords from the job description where they genuinely match the user's experience.\n"
        "* Keep the same resume sections (Summary, Education, Experience, Projects, Skills, Certifications).\n"
        "* Maintain a clean, professional resume format.\n"
        "* Return only the improved resume in Markdown or plain text.\n\n"
        "Inputs:\n"
        f"Resume:\n{resume_text}\n\n"
        f"Job Description:\n{job_description}\n"
    )

    # Validate model name (best-effort)
    model_name = _detect_supported_sdk_model_prefixes(model_name)

    # google-genai API
    try:
        resp = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config={"temperature": 0.2},
        )
    except Exception as e:
        msg = str(e)
        # Required by task: distinguish missing API key / invalid API key / unsupported model / network/API.
        if isinstance(e, GeminiMissingApiKeyError):
            raise
        if re.search(r"API key not valid|API_KEY_INVALID", msg, re.IGNORECASE):
            raise GeminiInvalidApiKeyError("Gemini API key is invalid") from e
        if re.search(r"model|unsupported|not found|unknown model", msg, re.IGNORECASE):
            raise GeminiUnsupportedModelError(f"Gemini model unsupported: {model_name}") from e
        raise GeminiApiRequestError(f"Gemini API request failed: {msg}") from e

    # genai response object varies; best-effort extraction
    text = getattr(resp, "text", None)
    if text:
        return text.strip()

    # Fallback: attempt common nested shapes
    try:
        return resp.candidates[0].content.parts[0].text.strip()  # type: ignore[attr-defined]
    except Exception:
        pass

    raise RuntimeError("Gemini response did not contain any text")


