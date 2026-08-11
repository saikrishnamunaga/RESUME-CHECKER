// Main JavaScript for UI interactions and future enhancements

document.addEventListener('DOMContentLoaded', function () {
  console.info('AI Resume Analyzer Pro: UI initialized');

  const suggestionsContainer = document.getElementById('suggestions-container');
  const suggestionsList = document.getElementById('suggestions-list');
  const btnGetSuggestions = document.getElementById('btn-get-suggestions');
  const btnAcceptChanges = document.getElementById('btn-accept-changes');
  const jobDescriptionInput = document.getElementById('job-description-input');
  const acceptingSpinner = document.getElementById('accepting-spinner');
  const linkDownloadDraft = document.getElementById('link-download-draft');

  if (!btnGetSuggestions || !btnAcceptChanges || !jobDescriptionInput) return;

  function setLoading(isLoading) {
    if (acceptingSpinner) acceptingSpinner.classList.toggle('d-none', !isLoading);
    btnGetSuggestions.disabled = isLoading;
    btnAcceptChanges.disabled = true;
    if (linkDownloadDraft) linkDownloadDraft.classList.toggle('disabled', isLoading);
  }

  function showSuggestions(suggestions) {
    if (!suggestionsList || !suggestionsContainer) return;
    suggestionsList.innerHTML = '';

    if (!Array.isArray(suggestions) || suggestions.length === 0) {
      const li = document.createElement('li');
      li.className = 'text-muted';
      li.textContent = 'No suggestions available.';
      suggestionsList.appendChild(li);
    } else {
      suggestions.forEach((s) => {
        const li = document.createElement('li');
        li.className = 'mb-2';
        li.innerHTML = `<i class="fas fa-circle me-2 text-primary small"></i>${String(s)}`;
        suggestionsList.appendChild(li);
      });
    }

    suggestionsContainer.classList.remove('d-none');
    btnAcceptChanges.disabled = false;
  }

  async function callEditResume({ resumeId = null, jobDescription }) {
    const payload = { job_description: jobDescription };
    if (resumeId !== null) payload.resume_id = resumeId;


    const res = await fetch('/dashboard/api/resume/edit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok || !data.ok) {
      throw new Error(data.error || 'Failed to generate suggestions.');
    }
    return data;
  }

  async function callAcceptResume({ resumeId = null, jobDescription }) {
    const payload = { job_description: jobDescription };
    if (resumeId !== null) payload.resume_id = resumeId;

    const res = await fetch('/dashboard/api/resume/accept', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok || !data.ok) {
      throw new Error(data.error || 'Failed to finalize draft.');
    }
    return data;
  }

  btnGetSuggestions.addEventListener('click', async function () {
    const jobDescription = (jobDescriptionInput.value || '').trim();
    if (!jobDescription) {
      alert('Please paste a job description to get tailored suggestions.');
      return;
    }

    btnGetSuggestions.disabled = true;
    try {
      const data = await callEditResume({ jobDescription });
      showSuggestions(data.suggestions);
      if (data.edited) {
        // keep existing draft download link behavior; optionally store edited text in-memory.
        window.__latestEditedResume = data.edited;
      }


      // keep download link pointing to latest server-side draft
      if (btnAcceptChanges) btnAcceptChanges.disabled = false;
    } catch (e) {
      alert(e.message || String(e));
    } finally {
      btnGetSuggestions.disabled = false;
    }
  });

  btnAcceptChanges.addEventListener('click', async function () {
    const jobDescription = (jobDescriptionInput.value || '').trim();
    if (!jobDescription) {
      alert('Job description is required to accept and finalize the draft.');
      return;
    }

    setLoading(true);
    try {
      const data = await callAcceptResume({ jobDescription });

      // Trigger download
      const url = data.download_url;
      if (url) {
        window.location.href = url;
      } else {
        alert('Draft finalized, but download URL was not returned.');
      }
    } catch (e) {
      alert(e.message || String(e));
    } finally {
      setLoading(false);
      // After finalization, keep accept enabled in case user wants to rerun.
      btnAcceptChanges.disabled = false;
    }
  });
});

