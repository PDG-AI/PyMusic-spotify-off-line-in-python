import os
import json
import random
import pygame
import pyperclip
import yt_dlp
import time
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from password import ADMIN_PASSWORD
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, DEFAULT_VOLUME

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.volume = DEFAULT_VOLUME
        pygame.mixer.music.set_volume(self.volume)
        self.current_playlist = []
        self.current_song_index = 0
        self.played_songs = set()
        
        # Diccionario de comandos con sus atajos
        self.commands = {
            "download": self.download_youtube_video,
            "d": self.download_youtube_video,
            "download_spotify": self.download_spotify_playlist,
            "ds": self.download_spotify_playlist,
            "create": self.create_playlist,
            "c": self.create_playlist,
            "delete": self.delete_playlist,
            "del": self.delete_playlist,
            "play": self.play_playlist,
            "pl": self.play_playlist,
            "play_song": self.play_song,
            "ps": self.play_song,
            "help": self.show_help,
            "h": self.show_help,
            "lists": self.show_lists,
            "l": self.show_lists,
            "songs": self.show_songs,
            "s": self.show_songs,
            "paste": self.paste_url,
            "volume": self.set_volume,
            "v": self.set_volume,
            "pass": self.play_next_song,
            "next": self.play_next_song,
            "p": self.play_next_song,
            "n": self.play_next_song
        }
        
        # Inicializar cliente de Spotify
        try:
            self.spotify = Spotify(auth_manager=SpotifyClientCredentials(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET
            ))
        except:
            print("Advertencia: No se pudo inicializar Spotify. Asegúrate de tener las credenciales configuradas en config.py")
            self.spotify = None
        
    def print_progress(self, current, total):
        """Imprime una barra de progreso y el porcentaje"""
        bar_length = 20
        filled_length = int(bar_length * current / total)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        percentage = int(100 * current / total)
        print(f"\r[{bar}] {percentage}% ({current}/{total})", end='', flush=True)
        if current == total:
            print()  # Nueva línea al completar

    def paste_url(self):
        """Pega la URL del portapapeles y la procesa automáticamente"""
        try:
            url = pyperclip.paste()
            if "youtube.com" in url or "youtu.be" in url:
                print(f"URL de YouTube detectada: {url}")
                self.download_youtube_video(url)
            elif "spotify.com" in url:
                print(f"URL de Spotify detectada: {url}")
                if "/track/" in url:
                    self.download_spotify_track(url)
                elif "/playlist/" in url:
                    self.download_spotify_playlist(url)
                else:
                    print("URL de Spotify no reconocida. Debe ser una canción o playlist.")
            else:
                print("URL no reconocida. Debe ser de YouTube o Spotify.")
        except Exception as e:
            print(f"Error al pegar URL: {e}")
        
    def process_command(self, command):
        try:
            cmd, *args = command.lower().split()  # Convertir a minúsculas
            if cmd in self.commands:
                return self.commands[cmd](*args)
            else:
                print(f"Comando no reconocido: {cmd}")
                self.show_help()
        except Exception as e:
            print(f"Error al procesar comando: {e}")
            self.show_help()

    def show_help(self):
        print("""
Comandos disponibles:
- Download/D [url_youtube] - Descarga un video de YouTube como MP3
- Download_Spotify/DS [url_playlist] - Descarga una playlist de Spotify
- Create/C [nombre_lista] [id_cancion1] [id_cancion2] ... - Crea una nueva lista
- Delete/DEL [id_lista_o_cancion] [contraseña] - Elimina una lista o canción
- Play/P [id_lista] - Reproduce una lista
- Play_Song/PS [id_cancion] - Reproduce una canción específica
- Lists/L - Muestra todas las listas de reproducción
- Songs/S - Muestra todas las canciones disponibles
- Paste/PA - Pega y procesa automáticamente una URL del portapapeles
- Volume/V [0-50] - Ajusta el volumen del reproductor (máximo 50%)
- Pass/NEXT/N - Pasa a la siguiente canción
- Help/H - Muestra esta ayuda
        """)

    def show_lists(self):
        try:
            lists = os.listdir("Lists")
            if not lists:
                print("No hay listas de reproducción disponibles")
                return
            
            print("\nListas de reproducción disponibles:")
            for i, list_file in enumerate(lists, 1):
                with open(f"Lists/{list_file}", "r") as f:
                    playlist = json.load(f)
                    print(f"{i}. {list_file[:-5]}: {playlist['name']} ({len(playlist['songs'])} canciones)")
        except Exception as e:
            print(f"Error al mostrar listas: {e}")

    def show_songs(self):
        try:
            songs = os.listdir("Songs")
            if not songs:
                print("No hay canciones disponibles")
                return
            
            print("\nCanciones disponibles:")
            for i, song in enumerate(songs, 1):
                if song.endswith(".mp3"):
                    song_id = song[:-4]  # Quitar la extensión .mp3
                    title = self.get_song_title(song_id)
                    print(f"{i}. {title} (ID: {song_id})")
        except Exception as e:
            print(f"Error al mostrar canciones: {e}")
        
    def download_spotify_track(self, track_url):
        """Descarga una canción individual de Spotify"""
        if not self.spotify:
            print("Error: Spotify no está configurado correctamente")
            return
        
        try:
            # Extraer el ID de la canción de la URL
            track_id = track_url.split("/track/")[1].split("?")[0]
            
            # Obtener información de la canción
            track = self.spotify.track(track_id)
            song_name = track['name']
            artist = track['artists'][0]['name']
            album = track['album']['name']
            
            print(f"Buscando: {song_name} - {artist}")
            
            # Buscar en YouTube con términos más específicos
            search_query = f"{song_name} {artist} {album} official audio"
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join('Songs', '%(id)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'default_search': 'ytsearch',
                'extract_flat': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    result = ydl.extract_info(f"ytsearch:{search_query}", download=False)
                    if result and 'entries' in result and result['entries']:
                        # Filtrar resultados para evitar podcasts y videos largos
                        valid_videos = []
                        for video in result['entries']:
                            title = video['title'].lower()
                            duration = video.get('duration', 0)
                            # Evitar podcasts, entrevistas y videos muy largos
                            if ('podcast' not in title and 
                                'interview' not in title and 
                                'live' not in title and
                                duration < 600):  # Menos de 10 minutos
                                valid_videos.append(video)
                        
                        if valid_videos:
                            video = valid_videos[0]
                            print(f"Encontrado: {video['title']}")
                            ydl.download([f"https://www.youtube.com/watch?v={video['id']}"])
                            # Guardar el título en un archivo de metadatos
                            self.save_song_metadata(video['id'], video['title'])
                            print(f"✓ Descargada: {song_name}")
                            time.sleep(1)
                            return video['id']
                        else:
                            print(f"No se encontró una versión adecuada para: {song_name}")
                            return None
                    else:
                        print(f"No se encontró el video para: {song_name}")
                        return None
                except Exception as e:
                    print(f"Error al descargar: {e}")
                    return None
                
        except Exception as e:
            print(f"Error al descargar canción de Spotify: {e}")
            return None

    def download_spotify_playlist(self, playlist_url):
        """Descarga una playlist de Spotify"""
        if not self.spotify:
            print("Error: Spotify no está configurado correctamente")
            return
        
        try:
            # Extraer el ID de la playlist de la URL
            playlist_id = playlist_url.split("/playlist/")[1].split("?")[0]
            
            # Obtener información de la playlist
            results = self.spotify.playlist(playlist_id)
            playlist_name = results['name']
            
            print(f"Descargando playlist: {playlist_name}")
            
            # Obtener todas las canciones de la playlist
            tracks = results['tracks']['items']
            downloaded_songs = []
            total_tracks = len(tracks)
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join('Songs', '%(id)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'default_search': 'ytsearch',
                'extract_flat': True,
            }
            
            for i, track in enumerate(tracks, 1):
                try:
                    song_name = track['track']['name']
                    artist = track['track']['artists'][0]['name']
                    album = track['track']['album']['name']
                    search_query = f"{song_name} {artist} {album} official audio"
                    
                    print(f"\nBuscando: {song_name} - {artist}")
                    self.print_progress(i, total_tracks)
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        try:
                            result = ydl.extract_info(f"ytsearch:{search_query}", download=False)
                            if result and 'entries' in result and result['entries']:
                                # Filtrar resultados para evitar podcasts y videos largos
                                valid_videos = []
                                for video in result['entries']:
                                    title = video['title'].lower()
                                    duration = video.get('duration', 0)
                                    # Evitar podcasts, entrevistas y videos muy largos
                                    if ('podcast' not in title and 
                                        'interview' not in title and 
                                        'live' not in title and
                                        duration < 600):  # Menos de 10 minutos
                                        valid_videos.append(video)
                                
                                if valid_videos:
                                    video = valid_videos[0]
                                    print(f"\nEncontrado: {video['title']}")
                                    ydl.download([f"https://www.youtube.com/watch?v={video['id']}"])
                                    # Guardar el título en un archivo de metadatos
                                    self.save_song_metadata(video['id'], video['title'])
                                    downloaded_songs.append(video['id'])
                                    print(f"✓ Descargada: {song_name}")
                                    time.sleep(1)
                                else:
                                    print(f"\nNo se encontró una versión adecuada para: {song_name}")
                            else:
                                print(f"\nNo se encontró el video para: {song_name}")
                        except Exception as e:
                            print(f"\nError al descargar: {e}")
                            continue
                        
                except Exception as e:
                    print(f"\nError al procesar canción: {e}")
                    continue
            
            if downloaded_songs:
                # Crear una lista de reproducción con las canciones descargadas
                playlist_id = self.create_playlist(f"Spotify - {playlist_name}", *downloaded_songs)
                print(f"\nPlaylist creada con ID: {playlist_id}")
                return playlist_id
            
        except Exception as e:
            print(f"Error al descargar playlist de Spotify: {e}")
            return None

    def save_song_metadata(self, song_id, title):
        """Guarda los metadatos de la canción en un archivo JSON"""
        try:
            metadata_file = os.path.join('Songs', 'metadata.json')
            metadata = {}
            
            # Cargar metadatos existentes si el archivo existe
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            
            # Actualizar metadatos
            metadata[song_id] = title
            
            # Guardar metadatos
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar metadatos: {e}")

    def get_song_title(self, song_id):
        """Obtiene el título de una canción desde los metadatos"""
        try:
            metadata_file = os.path.join('Songs', 'metadata.json')
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    return metadata.get(song_id, f"Canción {song_id}")
            return f"Canción {song_id}"
        except:
            return f"Canción {song_id}"

    def download_youtube_video(self, video_url):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join('Songs', '%(id)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                video_id = info['id']
                print(f"Canción descargada con ID: {video_id}")
                time.sleep(1)  # Pausa de 1 segundo
                return video_id
        except Exception as e:
            print(f"Error al descargar video: {e}")
            return None

    def create_playlist(self, playlist_name, *songs):
        playlist_id = f"{len(os.listdir('Lists')) + 1}L"
        playlist_data = {
            "name": playlist_name,
            "songs": list(songs)
        }
        with open(f"Lists/{playlist_id}.json", "w") as f:
            json.dump(playlist_data, f)
        print(f"Lista creada con ID: {playlist_id}")
        return playlist_id

    def delete_playlist(self, item_id, password):
        if password != ADMIN_PASSWORD:
            print("Contraseña incorrecta")
            return False
        try:
            # Verificar si es una lista o una canción
            if item_id.endswith('L'):  # Es una lista
                os.remove(f"Lists/{item_id}.json")
                print(f"Lista {item_id} eliminada")
            else:  # Es una canción
                # Eliminar el archivo MP3
                mp3_path = f"Songs/{item_id}.mp3"
                if os.path.exists(mp3_path):
                    os.remove(mp3_path)
                    # Eliminar de los metadatos
                    self.remove_song_metadata(item_id)
                    # Eliminar de todas las listas
                    self.remove_song_from_playlists(item_id)
                    print(f"Canción {item_id} eliminada")
                else:
                    print(f"No se encontró la canción {item_id}")
            return True
        except Exception as e:
            print(f"Error al eliminar: {e}")
            return False

    def remove_song_metadata(self, song_id):
        """Elimina una canción de los metadatos"""
        try:
            metadata_file = os.path.join('Songs', 'metadata.json')
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                if song_id in metadata:
                    del metadata[song_id]
                    
                    with open(metadata_file, 'w', encoding='utf-8') as f:
                        json.dump(metadata, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al eliminar metadatos: {e}")

    def remove_song_from_playlists(self, song_id):
        """Elimina una canción de todas las listas de reproducción"""
        try:
            for playlist_file in os.listdir("Lists"):
                playlist_path = f"Lists/{playlist_file}"
                with open(playlist_path, "r") as f:
                    playlist = json.load(f)
                
                if song_id in playlist['songs']:
                    playlist['songs'].remove(song_id)
                    with open(playlist_path, "w") as f:
                        json.dump(playlist, f, indent=2)
        except Exception as e:
            print(f"Error al eliminar canción de las listas: {e}")

    def play_playlist(self, playlist_id):
        try:
            with open(f"Lists/{playlist_id}.json", "r") as f:
                playlist = json.load(f)
            
            self.current_playlist = playlist["songs"]
            self.played_songs = set()
            print(f"Reproduciendo lista: {playlist['name']}")
            self.play_next_song()
        except Exception as e:
            print(f"Error al reproducir playlist: {e}")

    def play_next_song(self):
        if not self.current_playlist:
            return

        available_songs = [s for s in self.current_playlist if s not in self.played_songs]
        if not available_songs:
            self.played_songs.clear()
            available_songs = self.current_playlist

        next_song = random.choice(available_songs)
        self.played_songs.add(next_song)
        
        try:
            pygame.mixer.music.load(f"Songs/{next_song}.mp3")
            pygame.mixer.music.play()
            title = self.get_song_title(next_song)
            print(f"Reproduciendo: {title}")
        except Exception as e:
            print(f"Error al reproducir canción: {e}")

    def play_song(self, song_id):
        try:
            pygame.mixer.music.load(f"Songs/{song_id}.mp3")
            pygame.mixer.music.play()
            title = self.get_song_title(song_id)
            print(f"Reproduciendo: {title}")
        except Exception as e:
            print(f"Error al reproducir canción: {e}")

    def set_volume(self, volume_str):
        """Ajusta el volumen del reproductor (0-100)"""
        try:
            volume = float(volume_str) / 100
            # Limitar el volumen máximo al 50% del sistema
            volume = min(volume, 0.5)
            if 0 <= volume <= 0.5:
                self.volume = volume
                pygame.mixer.music.set_volume(volume)
                print(f"Volumen ajustado a {int(volume * 100)}%")
            else:
                print("El volumen debe estar entre 0 y 50")
        except ValueError:
            print("Por favor, introduce un número entre 0 y 50")

if __name__ == "__main__":
    player = MusicPlayer()
    print("PyMusic - Reproductor de Música Local")
    print("Escribe 'Help' para ver los comandos disponibles")
    print("Consejo: Copia una URL de YouTube o Spotify y usa el comando 'Paste' para procesarla")
    
    while True:
        try:
            command = input("\nComando > ")
            if command.lower() == "exit":
                break
            player.process_command(command)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
