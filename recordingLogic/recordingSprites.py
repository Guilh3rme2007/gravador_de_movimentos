import csv
import cv2
import time
import mediapipe as mp
 
def startRecording(camera, path_video, path_csv):
    sucess_test, test_frame = camera.read()
    if not sucess_test:
        raise RuntimeError("Não foi possível acessar a câmera do notebook")
    height, width, _ = test_frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    video_recorder = cv2.VideoWriter(path_video, fourcc, 30.0, (width, height))

    csv_file = open(path_csv, mode='w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Frame',
                         'Timestamp', 
                         'Ombro_D_X', 
                         'Ombro_D_Y', 
                         'Ombro_D_Z', 
                         'Ombro_E_X', 
                         'Ombro_E_Y', 
                         'Ombro_E_Z', 
                         'Cotovelo_D_X', 
                         'COTOVELO_D_Y', 
                         'Cotovelo_D_Z',
                         'Cotovelo_E_X',
                         'Cotovelo_E_Y',
                         'Cotovelo_E_Z',
                         'PULSO_D_X',
                         'PULSO_D_Y',
                         'PULSO_D_Z',
                         'PULSO_E_X',
                         'PULSO_E_Y',
                         'PULSO_E_Z',
                         'JOELHO_D_X',
                         'JOELHO_D_Y',
                         'JOELHO_D_Z',
                         'JOELHO_E_X',
                         'JOELHO_E_Y',
                         'JOELHO_E_Z'])

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose(min_detection_confidence =0.5, min_tracking_confidence=0.5)

    if not video_recorder.isOpened():
        raise RuntimeError(f"Não foi possível criar o vídeo em: {path_video}")

    print("Gravando... Aperte 'q' para sair.")

    frame_count = 0
    while True:
        sucess, frame = camera.read()
        if not sucess:
            break

        frame_count += 1
        actual_time = time.time()

        image_rgd = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(image_rgd)

        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            point = result.pose_landmarks.landmark
            ombro_d = point[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            ombro_e = point[mp_pose.PoseLandmark.LEFT_SHOULDER]
            cotovelo_d = point[mp_pose.PoseLandmark.RIGHT_ELBOW]
            cotovelo_e = point[mp_pose.PoseLandmark.LEFT_ELBOW]
            pulso_d = point[mp_pose.PoseLandmark.RIGHT_WRIST]
            pulso_e = point[mp_pose.PoseLandmark.LEFT_WRIST]
            joelho_d = point[mp_pose.PoseLandmark.RIGHT_KNEE]
            joelho_e = point[mp_pose.PoseLandmark.LEFT_KNEE]

            csv_writer.writerow([
                frame_count, 
                actual_time, 
                ombro_d.x, 
                ombro_d.y, 
                ombro_d.z, 
                ombro_e.x, 
                ombro_e.y, 
                ombro_e.z,
                cotovelo_d.x, 
                cotovelo_d.y, 
                cotovelo_d.z, 
                cotovelo_e.x, 
                cotovelo_e.y,
                cotovelo_e.z,
                pulso_d.x,
                pulso_d.y,
                pulso_d.z,
                pulso_e.x,
                pulso_e.y,
                pulso_e.z,
                joelho_d.x,
                joelho_d.y,
                joelho_d.z,
                joelho_e.x,
                joelho_e.y,
                joelho_e.z
            ])

        video_recorder.write(frame)
        cv2.imshow("Captura de Movimento", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    video_recorder.release()
    csv_file.close()
    cv2.destroyAllWindows()


