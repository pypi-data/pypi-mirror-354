import os
import platform
import subprocess
from typing import Optional

class Notifier:
    @staticmethod
    def notify(title: str, message: str) -> None:
        """Send a system notification."""
        system = platform.system()
        
        if system == "Windows":
            Notifier._notify_windows(title, message)
        elif system == "Darwin":  # macOS
            Notifier._notify_macos(title, message)
        else:  # Linux and others
            Notifier._notify_linux(title, message)

    @staticmethod
    def _notify_windows(title: str, message: str) -> None:
        """Send notification on Windows."""
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=5)
        except ImportError:
            # Fallback to PowerShell
            ps_script = f'''
            Add-Type -AssemblyName System.Windows.Forms
            $notify = New-Object System.Windows.Forms.NotifyIcon
            $notify.Icon = [System.Drawing.SystemIcons]::Information
            $notify.Visible = $true
            $notify.ShowBalloonTip(0, "{title}", "{message}", [System.Windows.Forms.ToolTipIcon]::None)
            '''
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)

    @staticmethod
    def _notify_macos(title: str, message: str) -> None:
        """Send notification on macOS."""
        try:
            subprocess.run([
                'osascript',
                '-e',
                f'display notification "{message}" with title "{title}"'
            ], capture_output=True)
        except Exception:
            pass

    @staticmethod
    def _notify_linux(title: str, message: str) -> None:
        """Send notification on Linux."""
        try:
            # Try notify-send first
            subprocess.run(['notify-send', title, message], capture_output=True)
        except FileNotFoundError:
            try:
                # Fallback to zenity
                subprocess.run(['zenity', '--info', f'--title={title}', f'--text={message}'], capture_output=True)
            except FileNotFoundError:
                pass 