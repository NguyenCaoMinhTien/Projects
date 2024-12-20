import cv2
import mediapipe as mp
import numpy as np
import time
import matplotlib.pyplot as plt
import os
import glob

class SwimmingDetector:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        self.results = None

        # Swimming Style
        self.style = "Boi tu do"

        # Angles variables
        self.left_angles = []
        self.right_angles = []

        # Stroke counter variables
        self.left_stroke = 0
        self.right_stroke = 0
        self.l_stage = None
        self.r_stage = None

        # Timer variable
        self.start_time = time.time()
        self.end_time = None
        self.elapsed_time = None

    def get_strokes(self):
        if self.style == "Boi tu do" or self.style == "Boi ngua":
            return self.left_stroke + self.right_stroke

        return self.left_stroke

    def get_result(self):
        return self.results

    def calculate_angle(self, a, b, c):
        a = np.array(a)  # Đầu
        b = np.array(b)  # Thân
        c = np.array(c)  # Chân

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    def get_orientation(self, landmarks):
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]

        # Calculate the vectors between shoulders and hips
        shoulder_vector_x = right_shoulder.x - left_shoulder.x
        shoulder_vector_y = right_shoulder.y - left_shoulder.y
        hip_vector_x = right_hip.x - left_hip.x
        hip_vector_y = right_hip.y - left_hip.y

        # Calculate the dot product of shoulder and hip vectors
        dot_product = shoulder_vector_x * hip_vector_x + shoulder_vector_y * hip_vector_y

    
        if shoulder_vector_x < 0:
            return "Forward"
        else:
            return "Backward"

    def process_frame(self, frame):
        """
        Process a single frame and return the processed frame.
        """
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        self.results = self.pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Check if landmarks are detected
        if self.results.pose_landmarks is not None:
            try:
                landmarks = self.results.pose_landmarks.landmark

                # Get orientation (forward or backward)
                orientation = self.get_orientation(landmarks)

                # Get left arm coordinates
                l_hip = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
                l_shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                l_elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                        landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

                # Get right arm coordinates
                r_hip = [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                        landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                r_shoulder = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                r_elbow = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                        landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

                # Calculate angles
                l_angle = self.calculate_angle(l_hip, l_shoulder, l_elbow)
                r_angle = self.calculate_angle(r_hip, r_shoulder, r_elbow)

                # Store angles in a list for plotting
                self.left_angles.append(l_angle)
                self.right_angles.append(r_angle)

                # Visualize angle
                cv2.putText(image, "Left: " + str(int(l_angle)),
                            tuple(np.multiply(l_shoulder, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )
                cv2.putText(image, "Right: " + str(int(r_angle)),
                            tuple(np.multiply(r_shoulder, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )

                # Stroke counter logic
                if l_angle < 30:
                    if self.style == "Khong co ket qua":
                        if r_angle < 70:
                            self.style = "Boi buom hoac \nBoi ech"
                        elif orientation == "Backward":
                            self.style = "Boi tu do"
                        else:
                            self.style = "Boi ngua"
                    self.l_stage = "down"
                elif l_angle > 160 and self.l_stage == 'down':
                    self.l_stage = "up"
                    self.left_stroke += 1

                if r_angle < 30:
                    if self.style == "Khong co ket qua":
                        if l_angle < 70:
                            self.style = "Boi buom hoac \nBoi ech"
                        elif orientation == "Backward":
                            self.style = "Boi tu do"
                        else:
                            self.style = "Boi ngua"
                    self.r_stage = "down"
                elif r_angle > 160 and self.r_stage == 'down':
                    self.r_stage = "up"
                    self.right_stroke += 1

                # Render stroke counter
                cv2.rectangle(image, (0, 0), (225, 100), (45, 45, 45), -1)
                cv2.putText(image, f'Stroke: {self.get_strokes()}', (10, 30),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, str(self.style), (10, 70),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2, cv2.LINE_AA)

            except Exception as e:
                print(f"Error processing landmarks: {e}")
        else:
                    # Return the processed frame
            print("No landmarks detected in this frame.")
            # return image

        # Render detections
        self.mp_drawing.draw_landmarks(image, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                    self.mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                    self.mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                    )
        return image
    
    def plot_angles(self):
        # Plot the angles
        plt.figure(figsize=(8, 6))
        plt.plot(self.left_angles, label='Left Arm Angles')
        plt.plot(self.right_angles, label='Right Arm Angles')
        plt.xlabel('Frame Number')
        plt.ylabel('Angle (degrees)')
        plt.title('Angles of Left and Right Arms')
        plt.legend()
        plt.grid(True)
        plt.show()

    def count_strokes(self, src=0, w_cam=640, h_cam=480):
        # VIDEO FEED
        cap = cv2.VideoCapture('uploaded_video.mp4')
        cap.set(3, w_cam)
        cap.set(4, h_cam)
        
        while cap.isOpened():
            ret, frame = cap.read()

            self.process_frame(frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()

    def get_strokes_per_minute(self):
        return (self.get_strokes() / self.elapsed_time) * 60

    def process_video(self, input_path, output_path):
        """
        Processes the input video frame by frame, applies detections, and saves the output video.
        """
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"Error: Unable to open video file {input_path}")
            return False

        # Get video properties
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Define video writer to save processed video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        print(f"Processing video: {input_path}")
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                print("End of video or error reading frame.")
                break

            # Write the processed frame to the output video
            out.write(self.process_frame(frame))

            frame_count += 1
            print(f"Processed frame {frame_count}")

        cap.release()
        out.release()
        print(f"Processed video saved to: {output_path}")
        return True