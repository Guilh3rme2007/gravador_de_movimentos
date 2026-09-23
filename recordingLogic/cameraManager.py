import cv2
import urllib.request
import numpy 

class IPCameraHTTP:
    def __init__(self, url):
        self.url = url.replace('/video', '/shot.jpg').replace('?.mjpg', '')
        self.opened = True

        try:
            urllib.request.urlopen(self.url, timeout=3)
        except Exception:
            print(f'Falha de rede: {Exception}')
            self.opened = False

    def isOpened(self):
        return self.opened

    def read(self):
        try:
            img_resp = urllib.request.urlopen(self.url, timeout=2)
            img_np = numpy.array(bytearray(img_resp.read()), dtype=numpy.uint8)
            frame = cv2.imdecode(img_np, -1)
            return True, frame
        except Exception:
            return False, None
        
    def release(self):
        self.opened = False

def notebookConnect():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print('Não foi possível conectar com a camera do notebook')
        return None

    return camera

def cellphoneConnect(ip_url = None):
    if ip_url:
        camera = IPCameraHTTP(ip_url)
        source = ip_url
    else:
        source = 1
        camera = cv2.VideoCapture(source)

    if not camera.isOpened():
        print(f"Erro: Não foi possível acessar o celular na fonte: {source}")
        return None
    return camera

