const fileInput = document.getElementById("fileInput");
const browseBtn = document.getElementById("browseBtn");
const dropZone = document.getElementById("dropZone");
const preview = document.getElementById("preview");
const dropPrompt = document.getElementById("dropPrompt");
const generateBtn = document.getElementById("generateBtn");
const resultSection = document.getElementById("resultSection");
const resultText = document.getElementById("resultText");
const copyBtn = document.getElementById("copyBtn");
const statusEl = document.getElementById("status");
const modeSelect = document.getElementById("mode");

let selectedFile = null;

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.classList.toggle("error", isError);
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
  generateBtn.disabled = false;
  setStatus("");
  resultSection.hidden = true;
}

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

generateBtn.addEventListener("click", async () => {
  if (!selectedFile) return;

  generateBtn.disabled = true;
  setStatus("Generating prompt...");
  resultSection.hidden = true;

  const formData = new FormData();
  formData.append("image", selectedFile);
  formData.append("mode", modeSelect.value);

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
    generateBtn.disabled = false;
  }
});

copyBtn.addEventListener("click", async () => {
  await navigator.clipboard.writeText(resultText.value);
  setStatus("Copied to clipboard.");
});
