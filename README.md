# Baixador de áudio do YouTube

O programa baixa o áudio de vídeos ou playlists e salva as músicas em MP3 na pasta `Music`, na raiz do projeto.

Playlists são separadas em pastas com até 100 músicas cada: a primeira usa o nome da playlist, a segunda acrescenta `2` ao nome, a terceira acrescenta `3` e assim por diante. Antes de baixar, o programa verifica se o MP3 já existe em qualquer pasta desse conjunto.

## Requisitos

- Python instalado.
- `pytubefix`, instalado no mesmo ambiente Python que será usado para executar o programa.
- FFmpeg instalado e disponível no `PATH`, necessário para converter o áudio para MP3.

## Instalação e execução no Windows (PowerShell)

Se Python já estiver instalado, pule o primeiro comando. Execute os comandos abaixo no PowerShell:

```powershell
winget install --id Python.Python.3.14 --exact
winget install --id Gyan.FFmpeg.Shared --exact
```

Depois da instalação, feche e abra novamente o PowerShell para atualizar o `PATH`. Vá até a pasta `MP3` do projeto, crie e ative o ambiente virtual, instale `pytubefix` e execute o programa:

```powershell
cd "C:\Users\ninja\OneDrive\Desktop\Hide\Download-de-m-sicas-e-playlist-inteiras-com-python-main\MP3"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pytubefix
python main.py
```

Se o ambiente virtual já existir, não é necessário criá-lo novamente: ative-o com `.\.venv\Scripts\Activate.ps1` e execute `python -m pip install pytubefix` e `python main.py`.

Se o PowerShell bloquear a ativação do ambiente virtual, permita scripts apenas nesta sessão e tente ativar novamente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```
