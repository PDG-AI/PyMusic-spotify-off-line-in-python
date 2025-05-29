PyMusic - Reproductor de Música Local
====================================

Un reproductor de música local con funcionalidades similares a Spotify, incluyendo descarga de música desde YouTube y Spotify.

Características
-------------
- Descarga de música desde YouTube y Spotify
- Creación y gestión de listas de reproducción
- Reproducción aleatoria de canciones
- Control de volumen ajustable
- Protección por contraseña para operaciones sensibles
- Interfaz de línea de comandos intuitiva
- Soporte para atajos de teclado
- Metadatos de canciones
- Barra de progreso en descargas

Requisitos
---------
- Python 3.6 o superior
- Bibliotecas Python:
  - pygame
  - spotipy
  - yt-dlp
  - pyperclip
  - ffmpeg-python
- FFmpeg instalado en el sistema

Instalación
----------
1. Clonar o descargar este repositorio
2. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Instalar FFmpeg:
   - Windows: `choco install ffmpeg`
   - Linux: `sudo apt-get install ffmpeg`
   - macOS: `brew install ffmpeg`
4. Configurar credenciales de Spotify en `config.py`

Estructura de Directorios
-----------------------
- `Songs/`: Almacena los archivos MP3 descargados
- `Lists/`: Almacena las listas de reproducción en formato JSON
- `Songs/metadata.json`: Almacena los títulos y metadatos de las canciones
- `config.py`: Configuración de Spotify y volumen por defecto
- `password.py`: Contraseña de administrador
- `main.py`: Programa principal

Comandos Disponibles
------------------
Comandos básicos:
- `Download/D [url_youtube]` - Descarga un video de YouTube como MP3
- `Download_Spotify/DS [url_playlist]` - Descarga una playlist de Spotify
- `Create/C [nombre_lista] [id_cancion1] [id_cancion2] ...` - Crea una nueva lista
- `Delete/DEL [id_lista_o_cancion] [contraseña]` - Elimina una lista o canción
- `Play/P [id_lista]` - Reproduce una lista
- `Play_Song/PS [id_cancion]` - Reproduce una canción específica
- `Lists/L` - Muestra todas las listas de reproducción
- `Songs/S` - Muestra todas las canciones disponibles
- `Paste/PA` - Pega y procesa automáticamente una URL del portapapeles
- `Volume/V [0-50]` - Ajusta el volumen del reproductor (máximo 50%)
- `Pass/NEXT/N` - Pasa a la siguiente canción
- `Help/H` - Muestra la ayuda

Características Especiales
------------------------
1. Control de Volumen:
   - Rango: 0-50% del volumen del sistema
   - Comando: `Volume 30` o `V 30`
   - El volumen máximo está limitado al 50% para evitar daños auditivos

2. Descarga de Spotify:
   - Soporta playlists completas
   - Descarga canciones individuales
   - Búsqueda inteligente en YouTube
   - Filtrado de podcasts y videos largos
   - Barra de progreso durante la descarga

3. Gestión de Canciones:
   - Títulos reales de las canciones
   - Metadatos guardados automáticamente
   - Eliminación segura de canciones
   - Limpieza automática de referencias

4. Listas de Reproducción:
   - Creación con nombre personalizado
   - Reproducción aleatoria
   - Protección por contraseña para eliminación
   - Visualización de canciones incluidas

5. Portapapeles:
   - Copia y pega URLs automáticamente
   - Detecta si es YouTube o Spotify
   - Procesa playlists y canciones individuales

Consejos de Uso
-------------
1. Para descargar música:
   - Copia la URL de YouTube o Spotify
   - Usa el comando `Paste` o `PA`
   - Espera a que se complete la descarga

2. Para reproducir música:
   - Usa `Songs` o `S` para ver las canciones disponibles
   - Usa `Play_Song` o `PS` seguido del ID para reproducir
   - Usa `Pass` o `N` para pasar a la siguiente canción

3. Para gestionar el volumen:
   - Usa `Volume` o `V` seguido de un número del 0 al 50
   - El volumen se ajusta inmediatamente

4. Para eliminar contenido:
   - Usa `Delete` o `DEL` seguido del ID
   - Proporciona la contraseña de administrador
   - Se eliminarán todas las referencias

Notas
-----
- La calidad de audio se establece en 192kbps
- Los archivos se guardan en formato MP3
- Se requiere conexión a Internet para descargar
- Las credenciales de Spotify son necesarias para descargar de Spotify
- El volumen máximo está limitado al 50% por seguridad
