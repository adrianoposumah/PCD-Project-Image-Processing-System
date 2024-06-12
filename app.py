from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image
import numpy as np
import os

app = Flask(__name__)

# Fungsi untuk memastikan direktori uploads ada jika belum
def ensure_uploads_dir():
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

def perbesar(berkas, sy, sx):
    tinggi, lebar, channel = berkas.shape

    tinggi_baru = int(tinggi * sy)
    lebar_baru = int(lebar * sx)

    F2 = np.zeros((tinggi_baru, lebar_baru, channel), dtype=np.uint8)

    for y in range(tinggi_baru):
        y2 = int((y / sy))
        for x in range(lebar_baru):
            x2 = int((x / sx))
            for c in range(channel):
                F2[y, x, c] = berkas[y2, x2, c]

    return F2

def mirrorH(berkas):
    tinggi, lebar, channel = berkas.shape
    G = np.zeros((tinggi, lebar, channel), dtype=np.uint8)

    for y in range(tinggi):
        for x in range(lebar):
            x2 = lebar - x - 1
            for c in range(channel):
                G[y, x, c] = berkas[y, x2, c]

    return G

def mirrorV(berkas):
    tinggi, lebar, channel = berkas.shape
    G = np.zeros((tinggi, lebar, channel), dtype=np.uint8)

    for y in range(tinggi):
        y2 = tinggi - y - 1
        for x in range(lebar):
            for c in range(channel):
                G[y, x, c] = berkas[y2, x, c]

    return 

def translasi(F, gy, gx):
    tinggi, lebar, channel = F.shape
    G = np.zeros_like(F, dtype=np.uint8)

    for y in range(tinggi):
        for x in range(lebar):
            if 0 <= y + gy < tinggi and 0 <= x + gx < lebar:
                G[y + gy, x + gx] = F[y, x]

    return G

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        ensure_uploads_dir()
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            try:
                action = request.form.get('action')
                sy = float(request.form.get('sy', 1))
                sx = float(request.form.get('sx', 1))

                # Use currentFile if available
                filepath = file.filename
                if file.filename.startswith('processed_'):
                    filepath = os.path.join('uploads', file.filename)
                else:
                    filepath = os.path.join('uploads', 'processed_' + file.filename)
                    file.save(filepath)

                image = Image.open(filepath)
                image_array = np.array(image)

                # Apply the appropriate function based on the selected action
                if action == 'scale':
                    processed_image_array = perbesar(image_array, sy, sx)
                    # Save the processed image with a specific filename
                    processed_filepath = os.path.join('uploads', 'scaled_' + os.path.basename(filepath))
                    processed_image = Image.fromarray(processed_image_array)
                    processed_image.save(processed_filepath)
                elif action == 'mirrorh':
                    # Check if there's a scaled image available
                    scaled_filepath = os.path.join('uploads', 'scaled_' + os.path.basename(filepath))
                    if os.path.exists(scaled_filepath):
                        filepath = scaled_filepath  # Use scaled image for mirror function
                    else:
                        return jsonify({'error': 'Scaled image not found'}), 400

                    # Continue with mirror function
                    image = Image.open(filepath)
                    image_array = np.array(image)
                    processed_image_array = mirrorH(image_array)
                elif action == 'mirrorv':
                    # Continue with mirror function using scaled image if available
                    scaled_filepath = os.path.join('uploads', 'scaled_' + os.path.basename(filepath))
                    if os.path.exists(scaled_filepath):
                        filepath = scaled_filepath  # Use scaled image for mirror function
                    else:
                        return jsonify({'error': 'Scaled image not found'}), 400

                    # Continue with mirror function
                    image = Image.open(filepath)
                    image_array = np.array(image)
                    processed_image_array = mirrorV(image_array)

                elif action == 'translate':
                    # Continue with translate function
                    ty = int(request.form.get('ty', 0))  # Get translation values from form
                    tx = int(request.form.get('tx', 0))

                    # Continue with translate function using scaled image if available
                    scaled_filepath = os.path.join('uploads', 'scaled_' + os.path.basename(filepath))
                    if os.path.exists(scaled_filepath):
                        filepath = scaled_filepath  # Use scaled image for translate function
                    else:
                        return jsonify({'error': 'Scaled image not found'}), 400

                    # Continue with translate function
                    image = Image.open(filepath)
                    image_array = np.array(image)
                    processed_image_array = translasi(image_array, ty, tx)

                else:
                    return jsonify({'error': 'Invalid action'}), 400

                # Convert back to image for display or saving
                processed_image = Image.fromarray(processed_image_array)
                processed_filepath = os.path.join('uploads', 'processed_' + os.path.basename(filepath))
                processed_image.save(processed_filepath)

                return jsonify({'message': 'Image processed successfully', 'filepath': processed_filepath})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    else:
        return render_template("index.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == "__main__":
    app.run(debug=True)
