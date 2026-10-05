import cv2
import time
from recordingLogic.transmition import MoCapExporter

def startRecording(camera, path_video, path_csv):
    sucess_test, test_frame = camera.read()
    if not sucess_test:
        raise RuntimeError("Não foi possível acessar a câmera do notebook")
    height, width, _ = test_frame.shape

    exporter = MoCapExporter(path_video, path_csv, width, height, fps=30.0, enable_udp=True)

    print("Gravando... Aperte 'q' para sair.")
    frame_count = 0

    while True:
        success, frame = camera.read()
        if not success:
            break

        frame_count += 1

        processed_frame = exporter.processFrame(frame, frame_count, time.time())

        cv2.imshow("Captura de Movimento", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
