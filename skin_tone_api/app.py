from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import io

app = Flask(__name__)

# Load TFLite model
MODEL_PATH = r"C:\Users\hasan\Rafi_SAA\Mobile_app_Cvindal1\PROJECT_CVINDAL1\skin_tone_detection\opt_model.tflite"

# Initialize TFLite interpreter
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


CLASS_LABELS = ['0', '1', '2', '3'] 

def preprocess_image(image_bytes):
    """Preprocess image for model input"""
    try:
        # Open image from bytes
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to model input size
        img = img.resize((224, 224))
        
        # Convert to numpy array and normalize
        img_array = np.array(img, dtype=np.float32) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        raise ValueError(f"Error preprocessing image: {str(e)}")

def predict(image_array):
    """Run inference on preprocessed image"""
    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], image_array)
    
    # Run inference
    interpreter.invoke()
    
    # Get output tensor
    output = interpreter.get_tensor(output_details[0]['index'])
    
    # Apply softmax to get probabilities
    probabilities = tf.nn.softmax(output[0]).numpy()
    
    # Get predicted class
    predicted_class = np.argmax(probabilities)
    confidence = float(probabilities[predicted_class])
    
    return predicted_class, confidence, probabilities

@app.route('/')
def home():
    return jsonify({
        "message": "Skin Tone Classification API",
        "endpoints": {
            "/": "Home route",
            "/api/classify_skin": "POST - Predict skin tone from image"
        }
    })


@app.route('/api/classify_skin', methods=['POST'])
def predict_skin_tone():
    """Predict skin tone from uploaded image"""
    try:
        # Check if image is in request
        if 'image' not in request.files:
            return jsonify({
                "error": "No image file provided",
                "message": "Please upload an image file with key 'image'"
            }), 400
        
        file = request.files['image']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                "error": "No file selected",
                "message": "Please select a valid image file"
            }), 400
        
        # Check file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}
        if not ('.' in file.filename and 
                file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({
                "error": "Invalid file type",
                "message": f"Allowed types: {', '.join(allowed_extensions)}"
            }), 400
        
        # Read image bytes
        image_bytes = file.read()
        
        # Preprocess image
        img_array = preprocess_image(image_bytes)
        
        # Make prediction
        predicted_class, confidence, probabilities = predict(img_array)
        
        # Prepare response
        result = {
            "success": True,
            "prediction": {
                "class": CLASS_LABELS[predicted_class],
                "class_id": int(predicted_class),
                "confidence": round(confidence * 100, 2)
            },
            "all_probabilities": {
                CLASS_LABELS[i]: round(float(prob) * 100, 2) 
                for i, prob in enumerate(probabilities)
            }
        }
        
        return jsonify(result), 200
        
    except ValueError as ve:
        return jsonify({
            "error": "Invalid image",
            "message": str(ve)
        }), 400
        
    except Exception as e:
        return jsonify({
            "error": "Prediction failed",
            "message": str(e)
        }), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Endpoint not found",
        "message": "Please check the API documentation at /"
    }), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "error": "Internal server error",
        "message": str(e)
    }), 500

if __name__ == '__main__':
    # Check if model exists
    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: Model not found at {MODEL_PATH}")
        print("Please update MODEL_PATH with correct path")
        exit(1)
    
    print(f"✅ Model loaded from: {MODEL_PATH}")
    print(f"🚀 Starting Flask API...")
    print(f"📊 Number of classes: {len(CLASS_LABELS)}")
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)