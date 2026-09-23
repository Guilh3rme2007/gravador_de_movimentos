# Sistema de Captura de Movimento (MoCap)

Um sistema de Rastreamento de Movimento baseado em Inteligência Artificial que dispensa o uso de marcadores físicos no corpo[cite: 16]. O projeto processa feeds de vídeo para identificar a estrutura corporal humana e extrair coordenadas 3D das articulações em tempo real[cite: 16].

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem base para processamento rápido de vídeo e integração de bibliotecas[cite: 16].
* **MediaPipe (Google):** Módulo de visão computacional (Pose) para rastrear os pontos do corpo[cite: 13, 16].
* **OpenCV:** Responsável por acessar as câmeras, manipular os frames de vídeo e desenhar o esqueleto na tela[cite: 13, 16].
* **SQLite:** Banco de dados integrado para gerenciar o histórico de gravações e sessões[cite: 14].

## ⚙️ Funcionalidades Atuais

* **Captura de Articulações:** Rastreamento simultâneo dos eixos X, Y e Z para Ombros, Cotovelos, Pulsos e Joelhos (lados direito e esquerdo)[cite: 13].
* **Gravação Sincronizada (Sprints):** Durante a captura, o sistema gera automaticamente um vídeo `.mp4` com o esqueleto sobreposto e um arquivo `.csv` contendo o timestamp e as coordenadas exatas de cada frame[cite: 13, 14].
* **Gerenciamento de Dados:** Criação de um banco de dados local (`mydatabase.db`) que salva o histórico de sprints gerados, organizando os arquivos fisicamente na pasta `records/`[cite: 14].
* **Suporte a Múltiplas Câmeras:** O módulo `cameraManager` permite capturar movimentos através da webcam do notebook ou integrar a câmera de um celular externo[cite: 11, 12].
* **Integração Mobile:** Permite usar smartphones via Cabo USB (webcam virtual) ou via Wi-Fi/IP (solicitando frames via HTTP para contornar restrições de codecs do sistema operacional)[cite: 12, 15].

## 🚀 Como Executar

1. Inicie o sistema rodando o arquivo principal: `python main.py`[cite: 11].
2. Navegue pelo Menu Principal no terminal[cite: 11]:
   * **1 - Gravar nova Sprint:** Inicia o processo de captura. O sistema pedirá o nome da pasta, o nome da Sprint e qual câmera utilizar[cite: 11, 14].
   * **2 - Buscar registros no Banco de Dados:** Permite listar todos os diretórios gravados ou buscar um arquivo específico pelo nome[cite: 11, 14].
   * **3 - Conectar Celular:** Menu dedicado para configurar um dispositivo móvel via Cabo (informando o índice da porta USB) ou via Wi-Fi/IP (inserindo a URL da rede)[cite: 11].

Para instruções detalhadas de como configurar o celular, consulte o arquivo `CellphoneConnectionInstructions.md`[cite: 15].

## 🔮 Futuras Features (Roadmap)

De acordo com a arquitetura base para sistemas MoCap avançados, os próximos passos do projeto incluem:

* **Transmissão de Dados (Streaming UDP):** Configuração de um cliente UDP no Python para empacotar e enviar as coordenadas das articulações instantaneamente (ex: porta `localhost:5005`)[cite: 16].
* **Integração com Motor Gráfico (Front-End 3D):** Criação de scripts receptores em C# (Unity) ou Python (Blender) para escutar a porta UDP e mapear as coordenadas X, Y, Z para os ossos de um avatar 3D em tempo real[cite: 16].
* **Processamento Assíncrono (Opção 4 do Menu):** Implementar a funcionalidade pendente de importar um vídeo da memória do PC ou celular, permitindo que o sistema extraia as coordenadas e gere o CSV a partir de gravações pré-existentes[cite: 11].
* **Sistemas Multi-Câmera:** Utilização de duas ou mais câmeras calibradas para calcular a profundidade real (3D espacial) com precisão comercial, evitando problemas de oclusão (quando o personagem fica de costas)[cite: 16].