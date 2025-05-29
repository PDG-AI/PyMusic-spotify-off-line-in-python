$ PyMusic-spotify-off-line-in-python
A local music player with Spotify-like features, including music download from YouTube and Spotify.

Features
--------
- Music download from YouTube and Spotify
- Playlist creation and management
- Random song playback
- Adjustable volume control
- Password protection for sensitive operations
- Intuitive command-line interface
- Keyboard shortcuts support
- Song metadata
- Download progress bar

Requirements
-----------
- Python 3.6 or higher
- Python libraries:
  - pygame
  - spotipy
  - yt-dlp
  - pyperclip
  - ffmpeg-python
- FFmpeg installed on the system

Installation
-----------
1. Clone or download this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Install FFmpeg:
   - Windows: `choco install ffmpeg`
   - Linux: `sudo apt-get install ffmpeg`
   - macOS: `brew install ffmpeg`
4. Configure Spotify credentials in `config.py`

Directory Structure
-----------------
- `Songs/`: Stores downloaded MP3 files
- `Lists/`: Stores playlists in JSON format
- `Songs/metadata.json`: Stores song titles and metadata
- `config.py`: Spotify configuration and default volume
- `password.py`: Administrator password
- `main.py`: Main program

Available Commands
----------------
Basic commands:
- `Download/D [youtube_url]` - Download a YouTube video as MP3
- `Download_Spotify/DS [playlist_url]` - Download a Spotify playlist
- `Create/C [playlist_name] [song_id1] [song_id2] ...` - Create a new playlist
- `Delete/DEL [playlist_or_song_id] [password]` - Delete a playlist or song
- `Play/P [playlist_id]` - Play a playlist
- `Play_Song/PS [song_id]` - Play a specific song
- `Lists/L` - Show all playlists
- `Songs/S` - Show all available songs
- `Paste/PA` - Paste and automatically process a URL from clipboard
- `Volume/V [0-50]` - Adjust player volume (maximum 50%)
- `Pass/NEXT/N` - Skip to next song
- `Help/H` - Show help

Special Features
--------------
1. Volume Control:
   - Range: 0-50% of system volume
   - Command: `Volume 30` or `V 30`
   - Maximum volume is limited to 50% to prevent hearing damage

2. Spotify Download:
   - Full playlist support
   - Individual song download
   - Smart YouTube search
   - Podcast and long video filtering
   - Download progress bar

3. Song Management:
   - Real song titles
   - Automatically saved metadata
   - Safe song deletion
   - Automatic reference cleanup

4. Playlists:
   - Custom named playlists
   - Random playback
   - Password protection for deletion
   - Included songs visualization

5. Clipboard:
   - Automatic URL copy and paste
   - YouTube and Spotify detection
   - Playlist and individual song processing

Usage Tips
---------
1. To download music:
   - Copy YouTube or Spotify URL
   - Use `Paste` or `PA` command
   - Wait for download to complete

2. To play music:
   - Use `Songs` or `S` to see available songs
   - Use `Play_Song` or `PS` followed by ID to play
   - Use `Pass` or `N` to skip to next song

3. To manage volume:
   - Use `Volume` or `V` followed by a number from 0 to 50
   - Volume adjusts immediately

4. To delete content:
   - Use `Delete` or `DEL` followed by ID
   - Provide administrator password
   - All references will be removed

Notes
-----
- Audio quality is set to 192kbps
- Files are saved in MP3 format
- Internet connection required for downloads
- Spotify credentials are required for Spotify downloads
- Maximum volume is limited to 50% for safety
