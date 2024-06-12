from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image
import numpy as np
import os

app = Flask(__name__)

# Fungsi untuk membuat direktori jika belum ada
def ensure_uploads_dir():
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

def perbesar(berkas, sy, sx):
    tinggi, lebar, channel = berkas.shape  # Mengambil dimensi gambar beserta channel warna

    tinggi_baru = int(tinggi * sy)
    lebar_baru = int(lebar * sx)

    F2 = np.zeros((tinggi_baru, lebar_baru, channel), dtype=np.uint8)  # Membuat array baru dengan dimensi yang diperbesar

    for y in range(tinggi_baru):
        y2 = int((y / sy))
        for x in range(lebar_baru):
            x2 = int((x / sx))
            for c in range(channel):  # Looping untuk setiap channel warna
                F2[y, x, c] = berkas[y2, x2, c]  # Memindahkan nilai pixel dari gambar asli ke gambar yang diperbesar

    return F2

def mirrorH(berkas):
    tinggi, lebar, channel = berkas.shape
    G = np.zeros((tinggi, lebar, channel), dtype=np.uint8)

    for y in range(tinggi):
        for x in range(lebar):
            x2 = lebar - x - 1
            for c in range(channel):
                G[y, x, c] = berkas[y, x2, c]  # Mengambil nilai pixel dari arah kanan ke kiri

    return G

def mirrorV(berkas):
    tinggi, lebar, channel = berkas.shape
    G = np.zeros((tinggi, lebar, channel), dtype=np.uint8)

    for y in range(tinggi):
        y2 = tinggi - y - 1
        for x in range(lebar):
            for c in range(channel):
                G[y, x, c] = berkas[y2, x, c]  # Mengambil nilai pixel dari arah bawah ke atas

    return G


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    ensure_uploads_dir()
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        sy = float(request.form['sy'])
        sx = float(request.form['sx'])
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        image = Image.open(filepath) # Mengubah gambar menjadi grayscale untuk proses
        image_array = np.array(image)
        
        # Terapkan fungsi perbesar
        scaled_image_array = perbesar(image_array, sy, sx)
        
        # Konversi kembali ke gambar untuk ditampilkan atau disimpan
        scaled_image = Image.fromarray(scaled_image_array)
        processed_filepath = os.path.join('uploads', 'processed_' + file.filename)
        scaled_image.save(processed_filepath)
        
        return jsonify({'message': 'Image uploaded and scaled successfully', 'filepath': processed_filepath})

@app.route('/process_image', methods=['POST'])
def process_image():
    ensure_uploads_dir()
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        action = request.form['action']
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        image = Image.open(filepath)  # Mengubah gambar menjadi grayscale untuk proses
        image_array = np.array(image)
        
        if action == 'mirrorh':
            processed_image_array = mirrorH(image_array)  # Ubah dari mirrorh menjadi mirrorH
        elif action == 'mirrorv':
            processed_image_array = mirrorV(image_array)
        else:
            return jsonify({'error': 'Invalid action'})
        
        processed_image = Image.fromarray(processed_image_array)
        processed_filepath = os.path.join('uploads', 'processed_' + file.filename)
        processed_image.save(processed_filepath)
        
        return jsonify({'message': 'Image processed successfully', 'filepath': processed_filepath})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == "__main__":
    app.run(debug=True)
