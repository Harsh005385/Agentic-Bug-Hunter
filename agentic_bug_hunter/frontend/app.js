const API_BASE = '';

const csvInput = document.getElementById('csv-file');
const runBtn = document.getElementById('run-btn');
const statusEl = document.getElementById('status');
const errorEl = document.getElementById('error');
const resultsSection = document.getElementById('results-section');
const resultsCount = document.getElementById('results-count');
const resultsTable = document.getElementById('results-table');
const downloadBtn = document.getElementById('download-btn');

let lastResults = [];

function setStatus(text) {
  statusEl.textContent = text;
}

function setError(text) {
  errorEl.textContent = text;
}

function clearError() {
  errorEl.textContent = '';
}

csvInput.addEventListener('change', () => {
  runBtn.disabled = !csvInput.files || csvInput.files.length === 0;
  clearError();
});

runBtn.addEventListener('click', async () => {
  const file = csvInput.files?.[0];
  if (!file) return;

  runBtn.disabled = true;
  clearError();
  setStatus('Running analysis…');
  resultsSection.hidden = true;
  lastResults = [];

  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch(`${API_BASE}/api/run`, {
      method: 'POST',
      body: formData,
    });
    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      setError(data.error || `Error ${res.status}`);
      setStatus('');
      runBtn.disabled = false;
      return;
    }

    lastResults = data.results || [];
    const count = data.count ?? lastResults.length;
    setStatus(`Done. ${count} row(s) processed.`);
    resultsCount.textContent = `${count} result(s)`;
    renderTable(lastResults);
    resultsSection.hidden = false;
  } catch (err) {
    setError(err.message || 'Request failed');
    setStatus('');
  } finally {
    runBtn.disabled = false;
  }
});

function renderTable(results) {
  const tbody = resultsTable.querySelector('tbody');
  tbody.innerHTML = '';
  results.forEach((row) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${escapeHtml(String(row.id ?? ''))}</td>
      <td>${escapeHtml(String(row.bug_line ?? ''))}</td>
      <td>${escapeHtml(String(row.explanation ?? ''))}</td>
    `;
    tbody.appendChild(tr);
  });
}

function escapeHtml(s) {
  const div = document.createElement('div');
  div.textContent = s;
  return div.innerHTML;
}

downloadBtn.addEventListener('click', async () => {
  if (lastResults.length === 0) return;

  try {
    const res = await fetch(`${API_BASE}/api/download`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ results: lastResults }),
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      setError(data.error || 'Download failed');
      return;
    }
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'bug_report.csv';
    a.click();
    URL.revokeObjectURL(url);
  } catch (err) {
    setError(err.message || 'Download failed');
  }
});
