from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image
import numpy as np
import os

app = Flask(__name__)


# Fungsi untuk membuat direktori jika belum ada
def ensure_uploads_dir():
    if not os.path.exists("uploads"):
        os.makedirs("uploads")


def perbesar(berkas, sy, sx):
    F = np.array(berkas)
    tinggi, lebar = F.shape

    tinggi_baru = int(tinggi * sy)
    lebar_baru = int(lebar * sx)

    F2 = np.zeros((tinggi_baru, lebar_baru), dtype=np.uint8)
    for y in range(tinggi_baru):
        y2 = int((y / sy))
        for x in range(lebar_baru):
            x2 = int((x / sx))
            F2[y, x] = F[y2, x2]

    return F2


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    ensure_uploads_dir()
    if "file" not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})
    if file:
        sy = float(request.form["sy"])
        sx = float(request.form["sx"])
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)
        image = Image.open(filepath).convert(
            "L"
        )  # Mengubah gambar menjadi grayscale untuk proses
        image_array = np.array(image)

        # Terapkan fungsi perbesar
        scaled_image_array = perbesar(image_array, sy, sx)

        # Konversi kembali ke gambar untuk ditampilkan atau disimpan
        scaled_image = Image.fromarray(scaled_image_array)
        processed_filepath = os.path.join("uploads", "processed_" + file.filename)
        scaled_image.save(processed_filepath)

        return jsonify(
            {
                "message": "Image uploaded and scaled successfully",
                "filepath": processed_filepath,
            }
        )


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)


if __name__ == "__main__":
    app.run(debug=True)
