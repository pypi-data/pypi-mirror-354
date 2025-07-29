import os
import yt_dlp
import subprocess
import sys
import re
from typing import Dict, List, Optional
from ..utils.progress import ProgressHandler
from ..utils.quality import QualityHandler
from ..utils.notify import Notifier
from ..utils.file_handler import FileHandler

def copy_file_to_clipboard(filepath):
    """Copy file path to clipboard (cross-platform)"""
    abs_path = os.path.abspath(filepath)
    if sys.platform == "win32":
        path = abs_path.replace('\\', '\\\\')
        os.system(f'powershell Set-Clipboard -Path "{path}"')
    elif sys.platform == "darwin":
        os.system(f"echo '{abs_path}' | pbcopy")
    else:
        os.system(f"echo '{abs_path}' | xclip -selection clipboard")

class YouTubeHandler:
    def __init__(self):
        self.download_dir = os.path.expanduser('~/crec/videos')
        self.audio_dir = os.path.expanduser('~/crec/audio')
        self.thumbnail_dir = os.path.expanduser('~/crec/photos')
        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.thumbnail_dir, exist_ok=True)
        
        # Default best quality
        self.ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [self._progress_hook],
        }
        self.current_progress = 0

    def can_handle(self, url: str) -> bool:
        """Check if the URL is a valid YouTube URL."""
        return 'youtube.com' in url or 'youtu.be' in url

    def _get_next_filename(self, audio_only: bool = False, output_dir: Optional[str] = None, 
                          filename_pattern: Optional[str] = None, video_info: Optional[Dict] = None) -> str:
        """Get the next available filename."""
        base_name = "audio" if audio_only else "video"
        target_dir = output_dir or (self.audio_dir if audio_only else self.download_dir)
        
        if filename_pattern and video_info:
            # Replace placeholders in filename pattern
            filename = filename_pattern
            filename = filename.replace('{title}', video_info.get('title', 'video'))
            filename = filename.replace('{id}', video_info.get('id', ''))
            filename = filename.replace('{quality}', str(video_info.get('height', '')))
            filename = filename.replace('{date}', video_info.get('upload_date', ''))
            # Remove invalid characters
            filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.'))
            ext = "mp3" if audio_only else "mp4"
            return os.path.join(target_dir, f"{filename}.{ext}")
        
        counter = 1
        while True:
            ext = "mp3" if audio_only else "mp4"
            filename = f"{base_name}{counter}.{ext}"
            if not os.path.exists(os.path.join(target_dir, filename)):
                return os.path.join(target_dir, filename)
            counter += 1

    def _progress_hook(self, d):
        """Handle download progress."""
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                if total > 0:
                    progress = (downloaded / total) * 100
                    if progress > self.current_progress:
                        print(f"\rDownloading: {progress:.1f}%", end='', flush=True)
                        self.current_progress = progress
            except:
                pass
        elif d['status'] == 'finished':
            print("\nDownload completed, processing...")

    def _download_thumbnail(self, video_id: str, output_dir: Optional[str] = None) -> Optional[str]:
        """Download video thumbnail."""
        try:
            target_dir = output_dir or self.thumbnail_dir
            output_path = os.path.join(target_dir, f"{video_id}.jpg")
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
                'writethumbnail': True,
                'outtmpl': output_path.replace('.jpg', ''),
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
            
            # Move thumbnail to correct directory based on extension
            return FileHandler.move_to_correct_directory(output_path)
        except Exception as e:
            print(f"Error downloading thumbnail: {str(e)}")
            return None

    def _get_video_info(self, url: str) -> Optional[Dict]:
        """Get video information."""
        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                return ydl.extract_info(url, download=False)
        except:
            return None

    def download(self, url: str, audio_only: bool = False, quality: Optional[str] = None, 
                compress_level: int = 0, output_dir: Optional[str] = None, 
                download_thumbnail: bool = False, filename_pattern: Optional[str] = None,
                is_playlist: bool = False, ffmpeg_args: Optional[str] = None) -> Optional[str]:
        """Download a YouTube video."""
        try:
            # Reset progress
            self.current_progress = 0
            
            # Get video info for custom naming
            video_info = self._get_video_info(url)
            if not video_info:
                print("Error: Could not get video information")
                return None

            # Handle playlist
            if is_playlist and 'entries' in video_info:
                print(f"Downloading playlist: {video_info.get('title', 'Untitled')}")
                print(f"Total videos: {len(video_info['entries'])}")
                
                downloaded_files = []
                for i, entry in enumerate(video_info['entries'], 1):
                    print(f"\nDownloading video {i}/{len(video_info['entries'])}")
                    video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                    result = self.download(
                        video_url, audio_only, quality, compress_level,
                        output_dir, download_thumbnail, filename_pattern,
                        False, ffmpeg_args
                    )
                    if result:
                        downloaded_files.append(result)
                
                if downloaded_files:
                    print(f"\nSuccessfully downloaded {len(downloaded_files)} videos")
                    return downloaded_files[0]  # Return first file for clipboard
                return None

            # Get format ID for requested quality
            format_id = None
            if quality:
                try:
                    target_quality = int(quality)
                    format_id = QualityHandler.get_format_for_quality(url, target_quality)
                    if not format_id:
                        print(f"Quality {quality}p not available.")
                        formats = QualityHandler.get_available_qualities(url)
                        QualityHandler.list_qualities(formats)
                        return None
                except ValueError:
                    print(f"Invalid quality format: {quality}")
                    return None

            # Get the final output path
            final_output_path = self._get_next_filename(
                audio_only, output_dir, filename_pattern, video_info
            )

            # Update options
            if audio_only:
                self.ydl_opts['format'] = 'bestaudio/best'
                self.ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                # For audio, we need to specify the output template without extension
                output_path = final_output_path.replace('.mp3', '')
            else:
                self.ydl_opts['format'] = format_id if format_id else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
                self.ydl_opts['postprocessors'] = []
                output_path = final_output_path

            # Add custom FFmpeg arguments if provided
            if ffmpeg_args:
                self.ydl_opts['postprocessor_args'] = ffmpeg_args.split()

            self.ydl_opts['outtmpl'] = output_path

            # Download the video
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])

            # Handle compression if requested
            if compress_level > 0 and not audio_only:
                print("\nCompressing video...")
                output_file = output_path.replace('.mp4', '_compressed.mp4')
                if QualityHandler.compress_video(output_path, output_file, compress_level):
                    # Remove original file
                    os.remove(output_path)
                    final_output_path = output_file
                else:
                    print("Compression failed, keeping original file")

            # Download thumbnail if requested
            if download_thumbnail:
                thumbnail_path = self._download_thumbnail(video_info['id'], output_dir)
                if thumbnail_path:
                    print(f"Thumbnail downloaded: {thumbnail_path}")

            # Move file to correct directory based on extension
            final_output_path = FileHandler.move_to_correct_directory(final_output_path)

            # Copy path to clipboard
            copy_file_to_clipboard(final_output_path)
            return final_output_path

        except Exception as e:
            print(f"Error downloading video: {str(e)}")
            return None 