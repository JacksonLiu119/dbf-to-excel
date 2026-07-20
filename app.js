const fileInput = document.getElementById("dbfFiles");
const encodingSelect = document.getElementById("encoding");
const convertBtn = document.getElementById("convertBtn");
const clearBtn = document.getElementById("clearBtn");
const dropzone = document.getElementById("dropzone");
const statusEl = document.getElementById("status");
const fileList = document.getElementById("fileList");

let selectedFiles = [];

fileInput.addEventListener("change", () => {
  setFiles(Array.from(fileInput.files || []));
});

dropzone.addEventListener("dragover", (event) => {
  event.preventDefault();
  dropzone.classList.add("dragover");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("dragover");
});

dropzone.addEventListener("drop", (event) => {
  event.preventDefault();
  dropzone.classList.remove("dragover");
  const files = Array.from(event.dataTransfer.files || []).filter((file) =>
    file.name.toLowerCase().endsWith(".dbf")
  );
  setFiles(files);
});

clearBtn.addEventListener("click", () => {
  fileInput.value = "";
  setFiles([]);
});

convertBtn.addEventListener("click", async () => {
  if (!selectedFiles.length) return;

  convertBtn.disabled = true;
  clearBtn.disabled = true;
  setStatus("轉換中...", "");

  try {
    for (const file of selectedFiles) {
      const buffer = await file.arrayBuffer();
      const parsed = parseDbf(buffer, encodingSelect.value);
      downloadWorkbook(file.name, parsed.records, parsed.fields);
    }

    setStatus(`完成 ${selectedFiles.length} 個檔案轉換。`, "ok");
  } catch (error) {
    console.error(error);
    setStatus(error.message || "轉換失敗，請確認檔案是否為 DBF 格式。", "error");
  } finally {
    convertBtn.disabled = selectedFiles.length === 0;
    clearBtn.disabled = selectedFiles.length === 0;
  }
});

function setFiles(files) {
  selectedFiles = files;
  convertBtn.disabled = files.length === 0;
  clearBtn.disabled = files.length === 0;
  fileList.innerHTML = "";

  for (const file of files) {
    const item = document.createElement("li");
    item.innerHTML = `<strong>${escapeHtml(file.name)}</strong><span>${formatBytes(file.size)}</span>`;
    fileList.appendChild(item);
  }

  setStatus(files.length ? `已選擇 ${files.length} 個 DBF 檔案。` : "尚未選擇檔案。", "");
}

function parseDbf(buffer, encoding) {
  const bytes = new Uint8Array(buffer);
  const view = new DataView(buffer);

  if (bytes.length < 32) {
    throw new Error("檔案太小，不是有效的 DBF。");
  }

  const recordCount = view.getUint32(4, true);
  const headerLength = view.getUint16(8, true);
  const recordLength = view.getUint16(10, true);

  if (!recordCount || headerLength < 33 || recordLength < 1 || headerLength > bytes.length) {
    throw new Error("DBF 檔頭格式不正確。");
  }

  const textDecoder = new TextDecoder(normalizeEncoding(encoding));
  const asciiDecoder = new TextDecoder("ascii");
  const fields = [];

  for (let offset = 32; offset < headerLength; offset += 32) {
    if (bytes[offset] === 0x0d) break;

    const nameBytes = bytes.slice(offset, offset + 11);
    const zeroIndex = nameBytes.indexOf(0);
    const rawName = zeroIndex >= 0 ? nameBytes.slice(0, zeroIndex) : nameBytes;
    const name = asciiDecoder.decode(rawName).trim();
    const type = String.fromCharCode(bytes[offset + 11]);
    const length = bytes[offset + 16];
    const decimals = bytes[offset + 17];

    if (name && length > 0) {
      fields.push({ name, type, length, decimals });
    }
  }

  if (!fields.length) {
    throw new Error("DBF 沒有可讀取的欄位。");
  }

  const records = [];
  for (let index = 0; index < recordCount; index += 1) {
    const rowOffset = headerLength + index * recordLength;
    if (rowOffset + recordLength > bytes.length) break;
    if (bytes[rowOffset] === 0x2a) continue;

    const row = {};
    let fieldOffset = rowOffset + 1;

    for (const field of fields) {
      const raw = bytes.slice(fieldOffset, fieldOffset + field.length);
      row[field.name] = parseValue(raw, field, textDecoder);
      fieldOffset += field.length;
    }

    records.push(row);
  }

  return { fields, records };
}

function parseValue(raw, field, decoder) {
  const text = decoder.decode(raw).trim();
  if (text === "") return "";

  switch (field.type) {
    case "N":
    case "F": {
      const value = Number(text);
      return Number.isFinite(value) ? value : text;
    }
    case "D":
      if (/^\d{8}$/.test(text)) {
        return `${text.slice(0, 4)}-${text.slice(4, 6)}-${text.slice(6, 8)}`;
      }
      return text;
    case "L":
      if (/^[YyTt]/.test(text)) return true;
      if (/^[NnFf]/.test(text)) return false;
      return text;
    default:
      return text;
  }
}

function downloadWorkbook(sourceName, records, fields) {
  const workbook = XLSX.utils.book_new();
  const header = fields.map((field) => field.name);
  const worksheet = XLSX.utils.json_to_sheet(records, { header });
  XLSX.utils.book_append_sheet(workbook, worksheet, "DBF");

  const outputName = sourceName.replace(/\.dbf$/i, "") + ".xlsx";
  XLSX.writeFile(workbook, outputName);
}

function normalizeEncoding(encoding) {
  return encoding === "big5" ? "big5" : encoding;
}

function setStatus(message, type) {
  statusEl.textContent = message;
  statusEl.className = type ? `status ${type}` : "status";
}

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (char) => {
    const map = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;",
    };
    return map[char];
  });
}
