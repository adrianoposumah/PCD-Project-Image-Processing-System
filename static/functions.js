let currentFile = ""; // Simpan nama file saat ini

function processImage(action) {
  const fileInput = document.getElementById("uploadBtn");
  const file = fileInput.files[0];
  let formData = new FormData();
  formData.append("file", file);
  formData.append("action", action);

  // Append scale, translate, crop, or other parameters if applicable
  if (action === "scale") {
    const sy = document.getElementById("sy").value;
    const sx = document.getElementById("sx").value;
    formData.append("sy", sy);
    formData.append("sx", sx);
  } else if (action === "translate") {
    const ty = document.getElementById("ty").value;
    const tx = document.getElementById("tx").value;
    formData.append("ty", ty);
    formData.append("tx", tx);
  } else if (action === "crop") {
    const f1 = document.getElementById("f1").value;
    const f2 = document.getElementById("f2").value;
    formData.append("f1", f1);
    formData.append("f2", f2);
  }

  fetch("/", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
      } else {
        currentFile = data.filepath;
        updateImagePreview(data.filepath);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// Fungsi untuk menjalankan fungsi mirrorh dengan menggunakan file terbaru
function processMirrorH() {
  processImage("mirrorh");
}

// Fungsi untuk menjalankan fungsi mirrorv dengan menggunakan file terbaru
function processMirrorV() {
  processImage("mirrorv");
}

// Fungsi untuk menjalankan fungsi scale dengan menggunakan file terbaru
function processScale() {
  processImage("scale");
}

function processTranslate() {
  processImage("translate");
}

function processCrop() {
  processImage("crop");
}
