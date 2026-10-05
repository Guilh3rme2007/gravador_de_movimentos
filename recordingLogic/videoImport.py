import cv2
import time
from recordingLogic.transmition import MoCapExporter

def processVideo(input_path, path_video, path_csv):
    camera = cv2.VideoCapture(input_path)

    if not camera.isOpened():
        print(f"Erro: Não foi possível abrir o vídeo em {input_path}")
        return

    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = camera.get(cv2.CAP_PROP_FPS)

    if fps == 0 or fps != fps:  
        fps = 30.0

    exporter = MoCapExporter(path_video, path_csv, width, height, fps=fps, enable_udp=True)

    print("Processando vídeo... Pressione 'q' para cancelar a qualquer momento.")
    frame_count = 0

    while True:
        success, frame = camera.read()
        if not success:
            print(f"Processamento concluído com sucesso! {frame_count} frames analisados.")
            break

        frame_count += 1
        processed_frame = exporter.processFrame(frame, frame_count, time.time())

        cv2.imshow("Processando Importação", processed_frame)
        time.sleep(1.0/fps)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

    camera.release()
    cv2.destroyAllWindows()
    