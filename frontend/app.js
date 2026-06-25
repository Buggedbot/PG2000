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
const formatSelect = document.getElementById("format");
const tipsList = document.getElementById("tipsList");

const IDEA_MODES = new Set(["video_generation"]);

const TIPS = {
  image_generation: [
    "Lead with the subject, medium, and mood before piling on details — models weight earlier words more heavily.",
    "Add 4-6 high-signal details: lighting, framing/angle, color palette, and materials/textures.",
    "Use cinematic or photographic terms (e.g. \"35mm\", \"golden hour\", \"rule of thirds\") — models respond well to them.",
    "Describe art influences by genre or era (e.g. \"Art Nouveau poster style\") rather than naming a specific living artist.",
    "Add a short negative prompt for things to avoid (e.g. \"no extra fingers, no blurry background\") if your tool supports it.",
    "Try the JSON format below — separating subject/style/lighting/camera into fields stops attributes from \"bleeding\" into each other on complex scenes.",
  ],
  text_generation: [
    "Give the model a role or persona (\"You are an experienced travel writer...\") to anchor tone and expertise.",
    "State the output format and length explicitly (e.g. \"a 150-word product blurb\", \"3 bullet points\").",
    "Provide a quick example of the style you want (few-shot) if the task is nuanced.",
    "For multi-step or reasoning-heavy tasks, ask the model to think step by step before producing the final answer.",
    "Iterate by changing one thing at a time (tone, length, structure) so you know what each change affects.",
  ],
  video_generation: [
    "Use the SCAAL framework: Subject, Camera, Action, Atmosphere, Length — cover each briefly.",
    "Describe one clear camera movement per clip (e.g. \"slow dolly in\") rather than combining several.",
    "Describe the physics or forces driving motion (\"wind pushes the leaves\") instead of just the end appearance.",
    "Explicitly say if the background should stay static, since models often add unwanted motion everywhere.",
    "Add small natural imperfections (\"slight sway\", \"hair blown by wind\") for more believable motion.",
    "Keep clips to 5-8 seconds — longer, more complex moves tend to degrade in current video models.",
    "Many video models (Veo-style) respond especially well to JSON-schema-style structured prompts — try the JSON format below.",
  ],
};

function renderTips() {
  const tips = TIPS[modeSelect.value] || [];
  tipsList.innerHTML = tips.map((tip) => `<li>${tip}</li>`).join("");
}

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
  renderTips();
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
  formData.append("format", formatSelect.value);
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
    formData.append("format", formatSelect.value);

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
