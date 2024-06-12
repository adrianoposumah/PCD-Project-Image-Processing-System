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
        updateImagePreview(data.filepath);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// Function to update the image preview
function updateImagePreview(imagePath) {
  const imagePreview = document.getElementById("imagePreview");
  imagePreview.src = imagePath;
}
