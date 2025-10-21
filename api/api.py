from flask import Flask, request, jsonify, render_template
import torch
from ultralytics import YOLO
import os
import io

# Initialize Flask app
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

# Load YOLOv11 model
model_path = os.path.join(os.path.dirname(__file__),'..', 'models', 'best.pt')
model = YOLO(model_path)
print("Model loaded successfully.", model_path)
print("Model details:", model)


@app.route('/')
def home():
    return render_template('upload.html')  # Simple HTML upload form


@app.route('/api/classify_outfit', methods=['GET','POST'])
def classify_outfit():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        file.save(file_path)

        # Run YOLO classification inference
        results = model(file_path)

        probs = results[0].probs  # class probabilities
        if probs is None:
            return jsonify({"error": "Model did not return classification probabilities"}), 500

        # Get top predicted class
        top_class_id = probs.top1
        top_class_name = results[0].names[top_class_id]
        confidence = float(probs.top1conf)

        # Optional: get full class distribution
        all_probs = {results[0].names[i]: float(prob) for i, prob in enumerate(probs.data.tolist())}

        return jsonify({
            "status": "success",
            "top_prediction": {
                "class": top_class_name,
                "confidence": round(confidence, 3)
            },
            "all_predictions": all_probs
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
