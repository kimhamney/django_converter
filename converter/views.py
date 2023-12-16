from django.shortcuts import render
from django.http import JsonResponse
from pytube import YouTube
from pathlib import Path
import os

downloads_path = str(Path.home() / "Downloads")

def main(request):
    if request.method == 'POST':
        try:
            url = request.POST.get('url')
            response = "success : " + url
            
            url = 'https://youtu.be/RHNY1hEHdIo?si=oRgoH26NyMHqGoQN'

            youtube = YouTube(url)
            
            video = youtube.streams.filter(only_audio=True).first()

            fileName = getFileName(youtube.title)
            filePath = f'{downloads_path}\{fileName}'
            video.download(downloads_path)
            
            os.rename(f'{downloads_path}\{video.default_filename}', filePath)

            return JsonResponse({'response': response})
        except Exception as e:
            return JsonResponse({'response': e})

    return render(request, 'index.html')


def getFileName(_fileName):
    fileNo = 0
    fileName = f'{_fileName}.mp3'
    while(True):
        fileNo += 1
        filePath = f'{downloads_path}\{fileName}'
        if os.path.exists(filePath):
            fileName = f'{_fileName}({fileNo}).mp3'
        else:
            return fileName