const fileInput = document.getElementById("fileInput");
const browseBtn = document.getElementById("browseBtn");
const dropZone = document.getElementById("dropZone");
const preview = document.getElementById("preview");
const dropPrompt = document.getElementById("dropPrompt");
const ideaArea = document.getElementById("ideaArea");
const ideaInput = document.getElementById("ideaInput");
const generateBtn = document.getElementById("generateBtn");
const resultSection = document.getElementById("resultSection");
const resultText = document.getElementById("resultText");
const copyBtn = document.getElementById("copyBtn");
const improveBtn = document.getElementById("improveBtn");
const statusEl = document.getElementById("status");
const modeSelect = document.getElementById("mode");

const IDEA_MODES = new Set(["video_generation"]);

let selectedFile = null;

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.classList.toggle("error", isError);
}

function isIdeaMode() {
  return IDEA_MODES.has(modeSelect.value);
}

function updateGenerateButtonState() {
  generateBtn.disabled = isIdeaMode() ? !ideaInput.value.trim() : !selectedFile;
}

function applyModeVisibility() {
  dropZone.hidden = isIdeaMode();
  ideaArea.hidden = !isIdeaMode();
  updateGenerateButtonState();
}

function selectFile(file) {
  if (!file || !file.type.startsWith("image/")) {
    setStatus("Please choose a valid image file.", true);
    return;
  }
  selectedFile = file;
  preview.src = URL.createObjectURL(file);
  preview.hidden = false;
  dropPrompt.hidden = true;
  setStatus("");
  resultSection.hidden = true;
  updateGenerateButtonState();
}

modeSelect.addEventListener("change", applyModeVisibility);
ideaInput.addEventListener("input", updateGenerateButtonState);

browseBtn.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", (e) => {
  selectFile(e.target.files[0]);
});

["dragenter", "dragover"].forEach((evt) =>
  dropZone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
  })
);

["dragleave", "drop"].forEach((evt) =>
  dropZone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
  })
);

dropZone.addEventListener("drop", (e) => {
  const file = e.dataTransfer.files[0];
  selectFile(file);
});

document.addEventListener("paste", (e) => {
  if (isIdeaMode()) return;
  const item = Array.from(e.clipboardData?.items || []).find((it) => it.type.startsWith("image/"));
  if (item) {
    e.preventDefault();
    selectFile(item.getAsFile());
  }
});

generateBtn.addEventListener("click", async () => {
  const mode = modeSelect.value;
  if (isIdeaMode() ? !ideaInput.value.trim() : !selectedFile) return;

  generateBtn.disabled = true;
  setStatus("Generating prompt...");
  resultSection.hidden = true;

  const formData = new FormData();
  formData.append("mode", mode);
  if (isIdeaMode()) {
    formData.append("idea", ideaInput.value.trim());
  } else {
    formData.append("image", selectedFile);
  }

  try {
    const response = await fetch("/api/prompt", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Failed to generate prompt");
    }

    resultText.value = data.prompt;
    resultSection.hidden = false;
    setStatus("Done.");
  } catch (err) {
    setStatus(err.message, true);
  } finally {
    updateGenerateButtonState();
  }
});

improveBtn.addEventListener("click", async () => {
  if (!resultText.value.trim()) return;

  improveBtn.disabled = true;
  setStatus("Improving prompt...");

  try {
    const formData = new FormData();
    formData.append("prompt", resultText.value.trim());
    formData.append("mode", modeSelect.value);

    const response = await fetch("/api/improve", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Failed to improve prompt");
    }

    resultText.value = data.prompt;
    setStatus("Improved.");
  } catch (err) {
    setStatus(err.message, true);
  } finally {
    improveBtn.disabled = false;
  }
});

copyBtn.addEventListener("click", async () => {
  await navigator.clipboard.writeText(resultText.value);
  setStatus("Copied to clipboard.");
});

applyModeVisibility();
