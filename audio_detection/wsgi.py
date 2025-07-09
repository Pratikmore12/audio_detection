"""
WSGI config for audio_detection project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import platform

if platform.system() == "Windows":
    os.environ["PATH"] += os.pathsep + r"C:\Users\prati\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1.1-full_build\bin"
# On Linux (Docker), ffmpeg is already in the PATH, so do nothing

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audio_detection.settings')

application = get_wsgi_application() 