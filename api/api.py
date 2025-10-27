from flask import Flask, request, jsonify, render_template
import torch
from ultralytics import YOLO
import os
import io
from PIL import Image


# Initialize Flask app
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

# Load YOLOv11 model
model_path = os.path.join(os.path.dirname(__file__),'..', 'models', 'best.pt')
model = YOLO(model_path)
# print("Model loaded successfully.", model_path)
# print("Model details:", model)


@app.route('/')
def home():
    return render_template('upload.html')  # Simple HTML upload form


@app.route('/api/classify_outfit', methods=['POST'])

# @app.route('/api/classify_outfit', methods=['POST'])
def classify_outfit():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['image']
        image = Image.open(io.BytesIO(file.read())).convert("RGB")

        results = model.predict(image, verbose=False)
        probs = results[0].probs

        if probs is None:
            return jsonify({"error": "Model did not return probabilities"}), 500

        top_class_id = probs.top1
        top_class_name = results[0].names[top_class_id]
        confidence = float(probs.top1conf)

        return jsonify({
            "status": "success",
            "top_prediction": {
                "class": top_class_name,
                "confidence": round(confidence, 3)
            }
        })

    except Exception as e:
        # Send the actual error message in JSON instead of HTML
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
