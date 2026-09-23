from server import data
import cv2
from recordingLogic import cameraManager 
from recordingLogic import recordingSprites as sprites

data.createDB()

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
        print("3 - Voltar")

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
            break

        else:
            print('Valor inválido, por favor tente novamente com um valor entre 1 e 3')
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
        continue

    elif choice == 5:
        print('Saindo do sistema...')
        break

    else:
        print('Valor inválido, por favor tente novamente com um valor entre 1 e 4')
        continue