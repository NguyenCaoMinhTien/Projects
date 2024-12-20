from flask import Flask, send_file, jsonify
import cv2
import threading
from SwimmingDetector import SwimmingDetector
import os

app = Flask(__name__)

# Video paths
VIDEO_INPUT_PATH = 'uploaded_video.mp4'
VIDEO_OUTPUT_PATH = "processed_video.mp4"

def process_and_save_video():
    """Process video and save it to a file."""
    cap = cv2.VideoCapture(VIDEO_INPUT_PATH)
    if not cap.isOpened():
        print(f"Error: Unable to open video file at {VIDEO_INPUT_PATH}")
        return

    detector = SwimmingDetector()
    
    print("Proessing video")
    detector.process_video(VIDEO_INPUT_PATH, VIDEO_OUTPUT_PATH)
    print("finished processing video")

@app.route("/")
def index():
    return "Flask Server is Running. Use /video to stream the processed video."

@app.route("/video", methods=["GET"])
def stream_video():
    """Return the processed video file."""
    print("Processing and saving video...")
    process_and_save_video()
    print("Processed and saved video.")

    if os.path.exists(VIDEO_OUTPUT_PATH):
        print(f"Returning video file: {VIDEO_OUTPUT_PATH}")
        return send_file(VIDEO_OUTPUT_PATH, mimetype="video/mp4", as_attachment=False)
    else:
        return jsonify({"error": "Processed video not found!"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)