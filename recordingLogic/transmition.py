import csv
import cv2
import mediapipe as mp
import socket
import json

class MoCapExporter:
    def __init__(self, path_video, path_csv, width, height, fps=30, enable_udp=True):
        self.enable_udp = enable_udp

        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        self.video_recorder = cv2.VideoWriter(path_video, fourcc, fps, (width, height))

        csv_file = open(path_csv, mode='w', newline='')
        csv_writer = csv.writer(csv_file)
        
        csv_writer.writerow(['Frame', 'Timestamp', 'Ombro_D_X', 'Ombro_D_Y', 'Ombro_D_Z', 'Ombro_E_X', 'Ombro_E_Y', 'Ombro_E_Z', 'Cotovelo_D_X', 'COTOVELO_D_Y', 'Cotovelo_D_Z', 'Cotovelo_E_X', 'Cotovelo_E_Y', 'Cotovelo_E_Z', 'PULSO_D_X', 'PULSO_D_Y', 'PULSO_D_Z', 'PULSO_E_X', 'PULSO_E_Y', 'PULSO_E_Z', 'JOELHO_D_X', 'JOELHO_D_Y', 'JOELHO_D_Z', 'JOELHO_E_X', 'JOELHO_E_Y', 'JOELHO_E_Z'])

        if self.enable_udp:
            self.UDP_IP = "127.0.0.1"
            self.UDP_PORT = 5005
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(min_detection_confidence =0.5, min_tracking_confidence=0.5)

    def processFrame(self, frame, frame_count, timestamp):
        image_rgd = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(image_rgd)

        if result.pose_landmarks:
            self.mp_drawing.draw_landmarks(frame, result.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

            pose = self.mp_pose.PoseLandmark
            point = result.pose_landmarks.landmark

            ombro_d, ombro_e = point[pose.RIGHT_SHOULDER], point[pose.LEFT_SHOULDER]
            cotovelo_d, cotovelo_e = point[pose.RIGHT_ELBOW], point[pose.LEFT_ELBOW]
            pulso_d, pulso_e = point[pose.RIGHT_WRIST], point[pose.LEFT_WRIST]
            joelho_d, joelho_e = point[pose.RIGHT_KNEE], point[pose.LEFT_KNEE]
            tornozelo_d, tornozelo_e = point[pose.RIGHT_ANKLE], point[pose.LEFT_ANKLE]

            self.csv_writer.writerow([
                frame_count, timestamp, ombro_d.x, ombro_d.y,ombro_d.z,ombro_e.x,ombro_e.y,ombro_e.z,cotovelo_d.x,cotovelo_d.y,cotovelo_d.z,cotovelo_e.x,cotovelo_e.y,cotovelo_e.z,pulso_d.x,pulso_d.y,pulso_d.z,pulso_e.x,pulso_e.y,pulso_e.z,joelho_d.x,joelho_d.y,joelho_d.z,joelho_e.x,joelho_e.y,joelho_e.z,tornozelo_d.x,tornozelo_d.y, tornozelo_d.z,tornozelo_e.x,tornozelo_e.y,tornozelo_e.z
                ])

            if self.enable_udp:
                data = {
                    "ombro_d":{"x":ombro_d.x,"y":ombro_d.y,"z":ombro_d.z},
                    "ombro_e":{"x":ombro_e.x,"y":ombro_e.y,"z":ombro_e.z},
                    "cotovelo_d":{"x":cotovelo_d.x,"y":cotovelo_d.y,"z":cotovelo_d.z},
                    "cotovelo_e":{"x":cotovelo_e.x,"y":cotovelo_e.y,"z":cotovelo_e.z},
                    "pulso_d":{"x":pulso_d.x,"y":pulso_d.y,"z":pulso_d.z},
                    "pulso_e":{"x":pulso_e.x,"y":pulso_e.y,"z":pulso_e.z},
                    "joelho_d":{"x":joelho_d.x,"y":joelho_d.y,"z":joelho_d.z},
                    "joelho_e":{"x":joelho_e.x,"y":joelho_e.y,"z":joelho_e.z},
                    "tornozelo_d":{"x":tornozelo_d.x,"y":tornozelo_d.y,"z":tornozelo_d.z},
                    "tornozelo_e":{"x":tornozelo_e.x,"y":tornozelo_e.y,"z":tornozelo_e.z}
                }
                self.sock.sendto(json.dumps(data).encode('utf-8'), (self.UDP_IP, self.UDP_PORT))

        self.video_recorder.write(frame)
        return frame

    def close(self):
        self.video_recorder.release()
        self.csv_file.close()
        if self.enable_udp:
            self.sock.close()
