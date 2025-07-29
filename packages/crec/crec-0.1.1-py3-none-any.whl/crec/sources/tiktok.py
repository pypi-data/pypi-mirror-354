import os
import yt_dlp
import subprocess
import sys
from typing import Optional
from ..utils.quality import QualityHandler

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

class TikTokHandler:
    def __init__(self):
        self.download_dir = os.path.expanduser('~/crec/videos')
        self.audio_dir = os.path.expanduser('~/crec/audio')
        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)
        
        # Default best quality
        self.ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [self._progress_hook],
        }
        self.current_progress = 0

    def can_handle(self, url: str) -> bool:
        """Check if the URL is a valid TikTok URL."""
        return 'tiktok.com' in url

    def _get_next_filename(self, audio_only: bool = False) -> str:
        """Get the next available filename."""
        base_name = "audio" if audio_only else "video"
        target_dir = self.audio_dir if audio_only else self.download_dir
        
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

    def download(self, url: str, audio_only: bool = False, quality: Optional[str] = None, compress_level: int = 0) -> Optional[str]:
        """Download a TikTok video."""
        try:
            # Reset progress
            self.current_progress = 0
            
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

            # Get the final output path (with extension)
            final_output_path = self._get_next_filename(audio_only)

            # Update options
            if audio_only:
                self.ydl_opts['format'] = 'bestaudio/best'
                self.ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                # For audio, we need to specify the output template without extension
                # as FFmpegExtractAudio will add .mp3
                output_path = final_output_path.replace('.mp3', '')
            else:
                self.ydl_opts['format'] = format_id if format_id else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
                self.ydl_opts['postprocessors'] = []
                output_path = final_output_path

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

            # Copy path to clipboard using the final path with extension
            copy_file_to_clipboard(final_output_path)
            return final_output_path

        except Exception as e:
            print(f"Error downloading video: {str(e)}")
            return None 