from flask import Flask, render_template, request
import os
from ultralytics import YOLO

# --- Flask setup ---
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

# --- Load YOLOv11 model ---
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'best.pt')
model_outfit = YOLO(model_path)

# --- Routes ---
@app.route('/')
def home():
    # Render your form.html (image upload page)
    return render_template('outfit_classification.html')

@app.route('/classify_outfit', methods=['POST'])
def classify_outfit():
    if 'outfit_image' not in request.files:
        return "No file uploaded", 400

    file = request.files['outfit_image']
    if file.filename == '':
        return "No selected file", 400

    # Save temporarily
    upload_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    image_path = os.path.join(upload_dir, file.filename)
    file.save(image_path)

    # Run YOLO inference
    results = model_outfit(image_path)
    top_class = results[0].names[results[0].probs.top1]

    # Clean up if you want
    os.remove(image_path)

    # Return result to browser
    return f"<h2>Predicted outfit: {top_class}</h2>"

if __name__ == '__main__':
    app.run(debug=True)
