from server import data
import os
import cv2
from recordingLogic import cameraManager 
from recordingLogic import recordingSprites as sprites
from recordingLogic import  videoImport as vi
from pathlib import Path

data.createDB()

def cleanScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def cellPhoneConnectionOptions():
    while True:
        print ("\nComo quer fazer a conexão? ")
        print("1 - via Cabo")
        print("2 - via Wifi/IP")
        print("3 - Voltar")

        try:
            option = int(input("Escolha uma opção: "))
        except ValueError:
            print('Por favor, digite um número.')
            continue

        if option == 1:
            try:
                index = int(input('Digite o índice da camera USB (tente 1, 2 ou 3): '))
            except ValueError:
                print('Valor inválido. Usando o índice 1 por padrão')
                index = 1
            cell_camera = cameraManager.cellphoneConnect(index)

        elif option == 2:
            ip = input("Digite a URL do vídeo (ex: http://192.168.0.5:8080/video): ")
            cell_camera = cameraManager.cellphoneConnect(ip)

        elif option == 3:
            break

        else:
            print('Valor inválido, por favor tente novamente com um valor entre 1 e 3')
            continue
        
    return cell_camera

def newSprintOptions():
   while True:
        print("\nQual câmera deseja usar? ")
        print("1 - Notebook")
        print("2 - Celular")
        print('3 - WebCam')
        print("4 - Voltar")

        try:
            op_cam = int(input("Escolha uma opção:  "))
        except ValueError:
            print('Por favor, digite um número.')
            continue

        if op_cam == 1:
            active_camera = cameraManager.notebookConnect()
            

        elif op_cam == 2:
            active_camera = cellPhoneConnectionOptions()
            

        elif op_cam == 3:
            active_camera = cameraManager.externalWebcamConnect()
            
        elif op_cam == 4:
            break

        else:
            print('Valor inválido, por favor tente novamente com um valor entre 1 e 4')
            continue

        if active_camera is None:
            continue

        video_path, csv_path = data.newSprint(active_camera)
        sprites.startRecording(active_camera, video_path, csv_path)

def dataOptions():
    while True:
        print('O que deseja consultar? ')  
        print('1 - Procurar arquivo especifico')
        print('2 - Ver todos os diretorios')
        print('3 - Voltar')

        try:
            option = int(input('Escolha uma opção:  '))
        except ValueError:
            print('Por favor, digite um número.')
            continue

        if option == 1:
            data.searchFile()

        elif option == 2:
            data.showFiles()

        elif option == 3:
            break

        else:
            print('Valor inválido, por favor tente novamente com um valor entre 1 e 3')
            continue


while True:
    cleanScreen()
    print('\n--- MENU ---')
    print('1 - Gravar nova Sprint')
    print('2 - Buscar registros no Banco de Dados')
    print('3 - Conectar Celular')
    print('4 - Importar Vídeo')
    print('5 - Sair')
    
    try:
        choice = int(input('Escolha uma opcao: '))
    except ValueError:
        print('Por favor, digite um número.')
        continue

    if choice == 1:
        # chamar funcao de nova Sprint
        newSprintOptions()
        continue

    elif choice == 2:
        # chamar funcao de buscar registros no banco
        dataOptions()
        continue

    elif choice == 3:
        #chamar funcao de conctar com celular
        cellPhoneConnectionOptions()
        continue

    elif choice == 4:
        #chamar funcao de importar video da memoria do pc ou do celular
        print("\n--- Importar Vídeo ---")
        input_path = input("Digite o caminho completo do vídeo (Exemplo mac:/users/meunome/Downloads/meu_video.mp4): ")
        
        if not Path(input_path).is_file():
            print("Erro: O arquivo não foi encontrado. Verifique o caminho e tente novamente.")
            continue
            
        print("\nConfigurando pasta para salvar os dados extraídos...")
        video_path, csv_path = data.newSprint(None) 

        vi.processVideo(input_path, video_path, csv_path)
        continue

    elif choice == 5:
        print('Saindo do sistema...')
        break

    else:
        print('Valor inválido, por favor tente novamente com um valor entre 1 e 4')
        continue