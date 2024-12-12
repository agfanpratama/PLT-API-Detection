from flask import Flask, request, render_template, jsonify
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
        str: Predicted label.
    """
    try:
        image = Image.open(image_path).convert("RGB")
        image = transform(image).unsqueeze(0)

        with torch.no_grad():
            outputs = model(image)
            _, predicted_idx = torch.max(outputs, 1)

        # Map the predicted index to ImageNet labels
        predicted_label = IMAGENET_LABELS[predicted_idx.item()]
        return predicted_label

    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Handle the main route to upload an image and display the prediction result.
    """
    result = None
    if request.method == "POST":
        file = request.files.get("image")  # Expect 'image' as the key
        if not file or file.filename == "":
            result = "No file selected. Please upload an image."
        else:
            try:
                # Save the uploaded file
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)

                # Predict the uploaded image
                result = predict_image(file_path)

            except Exception as e:
                result = f"Error: {str(e)}"

    return render_template("index.html", result=result)

@app.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint to predict the class of an uploaded image, returns the result in JSON format.
    """
    file = request.files.get("image")  # Expect 'image' as the key
    if not file or file.filename == "":
        return jsonify({"error": "No file selected. Please upload an image."}), 400

    try:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Predict the uploaded image
        result = predict_image(file_path)

        # Return prediction result in JSON
        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5002)