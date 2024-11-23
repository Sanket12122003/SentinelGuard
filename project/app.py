from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import torch.nn as nn
import cv2
import numpy as np
import warnings
import os
from scipy.fftpack import fft2, fftshift

# Suppress FutureWarnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow CORS for frontend-backend communication

# Define the Discriminator class
class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.model = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 64 * 3, 512),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, img):
        return self.model(img)


# Load the trained Discriminator model
model_path = os.path.join(os.path.dirname(__file__), "models", "discriminator.pth")
discriminator = Discriminator()

try:
    # Load the model weights
    state_dict = torch.load(model_path, map_location="cpu", weights_only=True)
    discriminator.load_state_dict(state_dict, strict=False)
    discriminator.eval()
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

# Function to analyze frequency domain
def analyze_frequency(img):
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    f_transform = fft2(grayscale)
    f_shift = fftshift(f_transform)
    magnitude_spectrum = np.log(np.abs(f_shift) + 1)
    return np.mean(magnitude_spectrum)

# Function to analyze edges and texture
def analyze_edges_and_texture(img):
    edges = cv2.Canny(img, 100, 200)
    edge_density = np.sum(edges) / (img.shape[0] * img.shape[1])
    return edge_density

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    # Ensure a file is uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    try:
        # Load and preprocess the image
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        img_resized = cv2.resize(img, (64, 64)) / 127.5 - 1.0  # Normalize to [-1, 1]
        img_resized = np.transpose(img_resized, (2, 0, 1))  # Convert to channel-first format
        img_tensor = torch.FloatTensor(img_resized).unsqueeze(0)  # Add batch dimension

        # Discriminator prediction
        with torch.no_grad():
            prediction = discriminator(img_tensor).item()  # Output from the discriminator

        # Additional measures
        frequency_score = analyze_frequency(img)
        edge_score = analyze_edges_and_texture(img)

        # Combined decision-making logic
        if prediction > 0.5 and frequency_score > 5 and edge_score > 0.01:
            result = "Real"
        else:
            result = "Fake"

        # Return result
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'Backend is running'}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
