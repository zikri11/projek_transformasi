from flask import Flask, request, render_template, send_file, url_for
from transformations import apply_rotation, apply_reflection, apply_dilation, apply_projection
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Buat folder uploads jika belum ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return "No file uploaded!", 400

    file = request.files['image']
    if file.filename == '':
        return "No file selected!", 400

    # Simpan gambar asli ke folder uploads
    original_path = os.path.join(app.config['UPLOAD_FOLDER'], 'original.png')
    image = Image.open(file)
    image.save(original_path)

    # Ambil jenis transformasi
    transform_type = request.form.get('transform')
    transformed_image = image

    if transform_type == 'rotate':
        degree = float(request.form.get('degree', 0))
        transformed_image = apply_rotation(image, degree)

    elif transform_type == 'reflect':
        axis = request.form.get('axis', 'x')
        transformed_image = apply_reflection(image, axis)

    elif transform_type == 'dilate':
        scale = float(request.form.get('scale', 1.0))
        transformed_image = apply_dilation(image, scale)

    elif transform_type == 'project':
        shear = float(request.form.get('shear', 0))
        axis = request.form.get('axis', 'x')
        transformed_image = apply_projection(image, shear, axis)

    else:
        return "Invalid transformation type.", 400

    # Simpan gambar hasil transformasi
    transformed_path = os.path.join(app.config['UPLOAD_FOLDER'], 'transformed.png')
    transformed_image.save(transformed_path)

    # Kirim jalur gambar asli dan transformasi ke template HTML
    return render_template('result.html', 
                           original_image=url_for('static', filename='uploads/original.png'),
                           transformed_image=url_for('static', filename='uploads/transformed.png'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
