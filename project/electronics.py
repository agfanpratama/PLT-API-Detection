from flask import Flask, request, jsonify
import torch
from torchvision import models, transforms
from PIL import Image
import os
import json

app = Flask(__name__)

# Ensure the "uploads" folder exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load ImageNet labels
with open("imagenet-simple-labels.json", "r") as f:
    IMAGENET_LABELS = json.load(f)

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

        # Map the predicted index to ImageNet labels
        predicted_label = IMAGENET_LABELS[predicted_idx.item()]
        return {"class": predicted_label, "confidence": confidence.item()}

    except Exception as e:
        return {"error": str(e)}

@app.route("/predict", methods=["POST"])
def predict():
    """
    Handle image prediction via POST request.

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

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
