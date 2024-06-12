function scaleImage() {
  const fileInput = document.getElementById("uploadBtn");
  const file = fileInput.files[0];
  const sy = document.getElementById("sy").value;
  const sx = document.getElementById("sx").value;

  const formData = new FormData();
  formData.append("file", file);
  formData.append("sy", sy);
  formData.append("sx", sx);

  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
      } else {
        // Update the preview with the processed image
        updateImagePreview(data.filepath);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function mirrorHImage() {
  const fileInput = document.getElementById("uploadBtn");
  const file = fileInput.files[0];

  const formData = new FormData();
  formData.append("file", file);
  formData.append("action", "mirrorh");

  fetch("/process_image", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
      } else {
        updateImagePreview(data.filepath);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function mirrorVImage() {
  const fileInput = document.getElementById("uploadBtn");
  const file = fileInput.files[0];

  const formData = new FormData();
  formData.append("file", file);
  formData.append("action", "mirrorv");

  fetch("/process_image", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
      } else {
        updateImagePreview(data.filepath);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
