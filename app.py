from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image
import numpy as np
import os

app = Flask(__name__)

latest_processed_image = None

def ensure_uploads_dir():
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

def reset_saved_image():
    latest_processed_image = None
    return latest_processed_image

def brightness_up(berkas):
    F = berkas.astype(np.float64)
    F += 100  
    F[F > 255] = 255 
    G = F.astype(np.uint8)
    return G

def brightness_down(berkas):
    F = berkas.astype(np.float64)
    F -= 100  
    F[F < 0] = 0  
    G = F.astype(np.uint8)
    return G

def kontras(berkas, factor):
    b = factor * berkas
    b = np.clip(b, 0, 255).astype(np.uint8)
    return b

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

    return G

def translasi(F, gy, gx):
    tinggi, lebar, channel = F.shape
    G = np.zeros_like(F, dtype=np.uint8)

    for y in range(tinggi):
        for x in range(lebar):
            if 0 <= y + gy < tinggi and 0 <= x + gx < lebar:
                G[y + gy, x + gx] = F[y, x]

    return G

def crop(berkas, f1, f2):
    tinggi, lebar = berkas.shape  
    G = np.zeros((tinggi, lebar), dtype=np.uint8)

    for y in range(tinggi):
        for x in range(lebar):
            if f1 <= berkas[y, x] <= f2:  
                G[y, x] = berkas[y, x]

    return G

def rotate90(image):
    tinggi, lebar, channel = image.shape
    direction = "90"

    if direction == '90':
        rotated_image = np.zeros((lebar, tinggi, channel), dtype=np.uint8)
        
        for y in range(tinggi):
            for x in range(lebar):
                for c in range(channel):
                    rotated_image[x, tinggi - 1 - y, c] = image[y, x, c]
    else:
        raise ValueError("Invalid direction. Choose from '90deg', '90deg', or '180deg'.")
    
    return rotated_image


def rotate180(image):
    tinggi, lebar, channel = image.shape
    direction = "180"

    if direction == '180':
        rotated_image = np.zeros((tinggi, lebar, channel), dtype=np.uint8)
        
        for y in range(tinggi):
            for x in range(lebar):
                for c in range(channel):
                    rotated_image[tinggi - 1 - y, lebar - 1 - x, c] = image[y, x, c]
    else:
        raise ValueError("Invalid direction. Choose from '90deg', '90deg', or '180deg'.")
    
    return rotated_image

def rotate270(image):
    tinggi, lebar, channel = image.shape
    direction = "270"

    if direction == '270':
        rotated_image = np.zeros((lebar, tinggi, channel), dtype=np.uint8)
        
        for y in range(tinggi):
            for x in range(lebar):
                for c in range(channel):
                    rotated_image[lebar - 1 - x, y, c] = image[y, x, c]
    else:
        raise ValueError("Invalid direction. Choose from '90deg', '90deg', or '180deg'.")
    
    return rotated_image

@app.route('/', methods=['GET', 'POST'])
def home():
    global latest_processed_image

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
                if latest_processed_image is None:
                    filepath = os.path.join('uploads', 'processed_' + file.filename)
                    file.save(filepath)
                    latest_processed_image = filepath
                else:
                    filepath = latest_processed_image

                image = Image.open(filepath)
                image_array = np.array(image)

                if action == 'scale':
                    sy = float(request.form.get('sy', 1))
                    sx = float(request.form.get('sx', 1))
                    processed_image_array = perbesar(image_array, sy, sx)
                elif action == 'mirrorh':
                    processed_image_array = mirrorH(image_array)
                elif action == 'mirrorv':
                    processed_image_array = mirrorV(image_array)
                elif action == 'brightnessup':
                    processed_image_array = brightness_up(image_array)
                elif action == 'brightnessdown':
                    processed_image_array = brightness_down(image_array)
                elif action == 'contrast':
                    factor = float(request.form.get('factor', 1.0))
                    processed_image_array = kontras(image_array, factor)
                elif action == 'translate':
                    ty = int(request.form.get('ty', 0))  
                    tx = int(request.form.get('tx', 0))
                    processed_image_array = translasi(image_array, ty, tx)
                elif action == 'rotate90':  
                    image = Image.open(filepath)
                    image_array = np.array(image)
                    processed_image_array = rotate90(image_array)
                elif action == 'rotate180':  
                    image = Image.open(filepath)
                    image_array = np.array(image)
                    processed_image_array = rotate180(image_array)
                elif action == 'rotate270':  
                    image = Image.open(filepath)
                    image_array = np.array(image)
                    processed_image_array = rotate270(image_array)
                elif action == 'crop':
                        f1 = int(request.form.get('f1', 0)) 
                        f2 = int(request.form.get('f2', 255))
                        processed_image_array = crop(np.array(Image.open(filepath)), f1, f2)
                else:
                    return jsonify({'error': 'Invalid action'}), 400

                processed_image = Image.fromarray(processed_image_array)
                processed_filepath = os.path.join('uploads', 'processed_' + os.path.basename(filepath))
                processed_image.save(processed_filepath)

                latest_processed_image = processed_filepath

                return jsonify({'message': 'Image processed successfully', 'filepath': processed_filepath})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    else:
        latest_processed_image = None
        return render_template("index.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == "__main__":
    app.run(debug=True)
