from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
import ssl
import os
import shutil
import subprocess
import tempfile
import re


# Desabilitar verificação SSL para resolver erro de certificado
ssl._create_default_https_context = ssl._create_unverified_context

# Informe o link da música/vídeo (YouTube)
url_padrao = "https://www.youtube.com/watch?v=ERnA797fkoA&list=RDydI5Od5CeKk&index=16"
destino = os.path.join(
    r"C:\Users\ninja\Desktop\Hide\Download-de-m-sicas-e-playlist-inteiras-com-python-main",
    "Music",
)


def baixar(url: str) -> None:
    """Baixa e converte o áudio da música para MP3."""
    yt = YouTube(url, on_progress_callback=on_progress)
    print(f"Baixando: {yt.title}")
    os.makedirs(destino, exist_ok=True)
    baixar_audio(yt, destino)


def obter_stream(video):
    """Seleciona um stream que contenha somente áudio."""
    stream = video.streams.get_audio_only()
    if stream is None:
        raise RuntimeError("Nenhum stream de áudio compatível foi encontrado.")
    return stream


def nome_seguro_windows(nome: str, padrao: str = "audio") -> str:
    nome = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", nome).strip().rstrip(" .")
    if not nome:
        nome = padrao
    if re.match(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", nome, re.IGNORECASE):
        nome = f"_{nome}"
    return nome


def baixar_audio(video, pasta_destino: str, pastas_verificacao=None) -> None:
    stream = obter_stream(video)
    nome_base = os.path.splitext(stream.default_filename)[0]
    nome_mp3 = nome_seguro_windows(nome_base) + ".mp3"
    caminho_mp3 = os.path.join(pasta_destino, nome_mp3)

    caminhos_existentes = [caminho_mp3]
    if pastas_verificacao:
        caminhos_existentes.extend(
            os.path.join(pasta, nome_mp3)
            for pasta in pastas_verificacao
            if os.path.normcase(pasta) != os.path.normcase(pasta_destino)
        )
    for caminho_existente in caminhos_existentes:
        if os.path.exists(caminho_existente):
            print(f"Já existe, pulando: {caminho_existente}\n")
            return

    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError(
            "FFmpeg não foi encontrado. Instale o FFmpeg e adicione-o ao PATH "
            "para converter os arquivos para MP3."
        )

    with tempfile.TemporaryDirectory(prefix=".audio-", dir=pasta_destino) as pasta_temp:
        caminho_origem = stream.download(output_path=pasta_temp)
        resultado = subprocess.run(
            [
                ffmpeg,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                caminho_origem,
                "-vn",
                "-codec:a",
                "libmp3lame",
                "-b:a",
                "320k",
                "-ar",
                "44100",
                "-ac",
                "2",
                caminho_mp3,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if resultado.returncode != 0:
            raise RuntimeError(
                f"Falha ao converter o áudio para MP3: {resultado.stderr.strip()}"
            )

    if not os.path.isfile(caminho_mp3) or os.path.getsize(caminho_mp3) == 0:
        raise RuntimeError(f"A conversão não gerou um MP3 válido: {caminho_mp3}")

    print(f"Concluído! Salvo em: {caminho_mp3}\n")


def baixar_playlist(url: str) -> None:
    """Baixa a playlist em pastas com até 100 músicas cada."""
    pl = Playlist(url)
    total_videos = len(pl.video_urls)
    print(f"Playlist: {pl.title} ({total_videos} vídeos)")

    nome_pasta = nome_seguro_windows(pl.title, "playlist")
    quantidade_pastas = max(1, (total_videos + 99) // 100)
    pastas_playlist = [
        os.path.join(
            destino,
            nome_pasta if parte == 1 else f"{nome_pasta}{parte}",
        )
        for parte in range(1, quantidade_pastas + 1)
    ]
    for pasta in pastas_playlist:
        if not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True)
            print(f"Pasta criada: {pasta}\n")
        else:
            print(f"Pasta já existe: {pasta}\n")

    for idx, video in enumerate(pl.videos, start=1):
        try:
            print(f"[{idx}/{total_videos}] {video.title}")
            parte = (idx - 1) // 100
            pasta_playlist = pastas_playlist[parte]
            baixar_audio(video, pasta_playlist, pastas_playlist)
        except Exception as exc:
            print(f"Erro no vídeo {idx}: {exc}")
    print(
        f"\nPlaylist '{pl.title}' concluída! Arquivos salvos em: "
        f"{', '.join(pastas_playlist)}\n"
    )


def main():
    while True:
        url_digitada = input(
            "Cole o link do YouTube (Enter usa padrão, 'sair' encerra): "
        ).strip()

        if url_digitada.lower() == "sair":
            break

        url = url_digitada or url_padrao

        try:
            if "playlist" in url or "list=" in url:
                baixar_playlist(url)
            else:
                baixar(url)
        except Exception as exc:
            print(f"Erro ao baixar: {exc}\nTente outro link ou verifique a conexão.\n")


if __name__ == "__main__":
    main()