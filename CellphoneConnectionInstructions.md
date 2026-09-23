# Guia de Conexão: Celular como Câmera no Sistema

Este documento descreve os passos necessários para conectar um dispositivo móvel (Android ou iOS) ao computador e utilizá-lo como câmera no sistema de captura de movimento. Você pode optar por uma conexão sem fio (via Wi-Fi/IP) ou com fio (via cabo USB).

---

## 1. Conexão via Wi-Fi/IP (Sem Fio)

Este método é o mais direto, pois não requer instalação de drivers ou softwares extras no computador, utilizando apenas a rede local.

### Requisitos Prévios
* O celular e o computador devem estar conectados **exatamente à mesma rede Wi-Fi**.

### Configuração no Dispositivo Móvel
1. **Para Android:** Baixe o aplicativo **IP Webcam** na Google Play Store.
2. **Para iOS:** Baixe um aplicativo equivalente, como **EpocCam** ou **IP Camera**.
3. Abra o aplicativo e procure pela opção de iniciar a transmissão (no *IP Webcam*, role até o final da tela e toque em **Start server**).
4. O aplicativo exibirá um endereço IP e uma porta na tela do celular (por exemplo: `http://192.168.0.103:8080`)[cite: 5]. Anote esse endereço.

### Utilização no Sistema
1. Execute o arquivo principal (`main.py`).
2. Escolha a opção **3 - Conectar Celular** e, em seguida, **2 - via Wifi/IP**[cite: 4].
3. Digite a URL fornecida pelo aplicativo e adicione o sufixo `/video` ao final (exemplo: `http://192.168.0.103:8080/video`)[cite: 4, 5].

---

## 2. Conexão via Cabo USB

Este método oferece maior estabilidade de quadros e menor latência, mas exige o uso de um software de "Webcam Virtual" (como Iriun Webcam, Camo ou DroidCam) instalado tanto no celular quanto no computador.

### 2.1 Preparação do Dispositivo Móvel

**Android (Habilitar Depuração USB)**
1. Acesse **Configurações** > **Sobre o telefone** e toque 7 vezes em **Número da Versão** (ou Número da Compilação) para habilitar o modo desenvolvedor.
2. Volte às **Configurações**, acesse **Sistema** > **Opções do Desenvolvedor** e ative a **Depuração USB**.
3. Conecte o cabo USB ao computador.
4. Na tela do celular, aceite a solicitação de segurança marcando "Sempre permitir neste computador" e toque em **OK**.

**iOS (iPhone - Confiar no Computador)**
1. Conecte o iPhone ao computador via cabo com a tela do celular ativa e desbloqueada.
2. Toque em **Confiar** no alerta "Confiar Neste Computador?" que aparecerá na tela do aparelho.
3. Digite sua senha numérica de desbloqueio para confirmar.

### 2.2 Configuração no Computador (Sistema Operacional)

**macOS**
1. Instale o cliente desktop do aplicativo de webcam virtual (Iriun, Camo, etc.) no seu Mac.
2. Abra o aplicativo no Mac e no celular simultaneamente.
3. No primeiro uso, o macOS pode bloquear o vídeo por segurança. Acesse **Ajustes do Sistema** > **Privacidade e Segurança** > **Câmera** e conceda permissão para o aplicativo.
4. Verifique no Finder se o celular está sendo reconhecido como um dispositivo conectado.

**Windows**
1. Instale o cliente desktop do aplicativo de webcam virtual no Windows.
2. **Para usuários de Android:** O Windows geralmente instala os drivers ADB/USB automaticamente. Caso o aplicativo não reconheça o celular, instale o driver USB oficial correspondente à fabricante do seu smartphone (Samsung, Motorola, Xiaomi, etc.).
3. **Para usuários de iOS:** É estritamente necessário ter o **iTunes** instalado e rodando em segundo plano no Windows para garantir que os drivers de comunicação via cabo do iPhone funcionem corretamente (recomendável baixar o executável direto do site da Apple).
4. Abra o aplicativo no Windows e no celular para estabelecer a conexão.

### 2.3 Utilização no Sistema
1. Execute o arquivo principal (`main.py`).
2. Escolha a opção **3 - Conectar Celular** e, em seguida, **1 - via Cabo**[cite: 4].
3. O sistema tentará buscar a câmera no índice `1` por padrão[cite: 2]. Caso retorne erro ou abra a câmera errada (como a webcam nativa do notebook), o sistema solicitará que você insira o índice manualmente. Teste os índices sequenciais (`1`, `2` ou `3`) até localizar a porta virtual que o sistema operacional atribuiu ao aplicativo.