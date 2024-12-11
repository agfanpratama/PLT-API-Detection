from flask import Flask, request, jsonify, render_template
import torch
from torchvision import models, transforms
from PIL import Image
import os
import json

app = Flask(__name__)

# Ensure the "uploads" folder exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define Electronics Categories (example based on ImageNet labels)
ELECTRONICS_CLASSES = {
    'laptop': [0],  # replace with actual ImageNet indices for laptop, etc.
    'smartphone': [1],  # same as above, adjust for smartphone
    'speaker': [2],
    'smartwatch': [3],
    'kulkas': [4],
    'air_conditioner': [5]
}

# Load a pre-trained ResNet model
model = models.resnet18(pretrained=True)
model.eval()

# Define a transformation for input images
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def predict_image(image_path):
    """
    Predict the class of an image using the pre-trained model.

    Args:
        image_path (str): Path to the image file.
    
    Returns:
        dict: Predicted label and confidence score.
    """
    try:
        image = Image.open(image_path).convert("RGB")
        image = transform(image).unsqueeze(0)

        with torch.no_grad():
            outputs = model(image)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            confidence, predicted_idx = torch.max(probabilities, 0)

        # Here we match the predicted class index with our ELECTRONICS_CLASSES
        predicted_label = None
        for label, indices in ELECTRONICS_CLASSES.items():
            if predicted_idx.item() in indices:
                predicted_label = label
                break

        return {"class": predicted_label, "confidence": confidence.item()}

    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict_electronics", methods=["POST"])
def predict_electronics():
    """
    Handle image upload via POST request for electronic devices.

    Returns:
        JSON response with prediction result.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    if not file or file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Predict the uploaded image
        result = predict_image(file_path)

        # Clean up the saved file
        os.remove(file_path)

        # Pass the result to the template for rendering
        return render_template("index.html", prediction=result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
