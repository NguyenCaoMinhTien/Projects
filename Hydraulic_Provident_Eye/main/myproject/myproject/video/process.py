import cv2
import os
from SwimmingDetector import SwimmingDetector

# Đường dẫn video
VIDEO_INPUT_PATH = 'main/myproject/myproject/video/uploaded_video.mp4'
VIDEO_OUTPUT_PATH = 'main/myproject/myproject/video/processed_video.mp4'

def process_and_save_video():
    # Kiểm tra file đầu vào
    if not os.path.exists(VIDEO_INPUT_PATH):
        print(f"Error: Input video not found at {VIDEO_INPUT_PATH}")
        return

    cap = cv2.VideoCapture(VIDEO_INPUT_PATH)
    if not cap.isOpened():
        print(f"Error: Unable to open video file {VIDEO_INPUT_PATH}")
        return

    # Khởi tạo SwimmingDetector
    try:
        detector = SwimmingDetector()
    except Exception as e:
        print(f"Error initializing SwimmingDetector: {e}")
        return

    # Lấy kích thước frame từ video đầu vào
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec cho video MP4
    out = cv2.VideoWriter(VIDEO_OUTPUT_PATH, fourcc, 30.0, (frame_width, frame_height))

    print("Processing video...")
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Xử lý frame với SwimmingDetector
            try:
                processed_frame = detector.process_frame(frame)
            except Exception as e:
                print(f"Error processing frame: {e}")
                continue

            # Ghi frame đã xử lý
            out.write(processed_frame)

    finally:
        cap.release()
        out.release()
        print(f"Video processing complete. Video saved to: {VIDEO_OUTPUT_PATH}")

def main():
    process_and_save_video()

if __name__ == "__main__":
    main()
