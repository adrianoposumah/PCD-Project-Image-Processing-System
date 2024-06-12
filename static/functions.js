let currentFile = ""; // Simpan nama file saat ini

function processImage(action) {
  const fileInput = document.getElementById("uploadBtn");
  const file = fileInput.files[0];
  let formData = new FormData();
  formData.append("file", file);
  formData.append("action", action);

  // Append scale parameters if applicable
  if (action === "scale") {
    const sy = document.getElementById("sy").value;
    const sx = document.getElementById("sx").value;
    formData.append("sy", sy);
    formData.append("sx", sx);
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
        // Simpan nama file yang dihasilkan
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
