from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
import ssl
import os


# Desabilitar verificação SSL para resolver erro de certificado
ssl._create_default_https_context = ssl._create_unverified_context

# Informe o link da música/vídeo (YouTube)
url_padrao = "https://www.youtube.com/watch?v=ERnA797fkoA&list=RDydI5Od5CeKk&index=16"
destino = "C:/Users/ninja/Desktop/MP3/Music"


def baixar(url: str) -> None:
    """Baixa o vídeo pelo link informado."""
    yt = YouTube(url, on_progress_callback=on_progress)
    print(f"Baixando: {yt.title}")
    video_stream = yt.streams.get_highest_resolution()

    os.makedirs(destino, exist_ok=True)
    alvo = os.path.join(destino, video_stream.default_filename)

    if os.path.exists(alvo):
        print(f"Já existe, pulando: {alvo}\n")
        return

    video_stream.download(output_path=destino)
    print(f"Concluído! Salvo em: {alvo}\n")


def baixar_playlist(url: str) -> None:
    """Baixa todos os vídeos de uma playlist."""
    pl = Playlist(url)
    print(f"Playlist: {pl.title} ({len(pl.video_urls)} vídeos)")
    
    # Criar pasta com o nome da playlist (remover caracteres inválidos)
    nome_pasta = "".join(c for c in pl.title if c.isalnum() or c in (' ', '-', '_')).strip()
    pasta_playlist = os.path.join(destino, nome_pasta)
    if not os.path.exists(pasta_playlist):
        os.makedirs(pasta_playlist, exist_ok=True)
        print(f"Pasta criada: {pasta_playlist}\n")
    else:
        print(f"Pasta já existe: {pasta_playlist}\n")

    for idx, video in enumerate(pl.videos, start=1):
        try:
            print(f"[{idx}/{len(pl.video_urls)}] {video.title}")
            stream = video.streams.get_highest_resolution()
            alvo = os.path.join(pasta_playlist, stream.default_filename)

            if os.path.exists(alvo):
                print(f"   Já existe, pulando: {alvo}")
                continue

            stream.download(output_path=pasta_playlist)
        except Exception as exc:
            print(f"Erro no vídeo {idx}: {exc}")
    print(f"\nPlaylist '{pl.title}' concluída! Arquivos salvos em: {pasta_playlist}\n")


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