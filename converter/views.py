import os
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from pathlib import Path
from pytube import YouTube
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def main(request):
    if request.method == 'POST':
        DEVELOPER_KEY= settings.YOUTUBE_API_KEY
        YOUTUBE_API_SERVICE_NAME='youtube'
        YOUTUBE_API_VERSION='v3'

        youtube=build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

        search_response=youtube.search().list(
            q="잠시라도우리 lylics",
            order='relevance',
            part='snippet',
            type="video",
            maxResults=5
            ).execute()
        
        result = []
        for item in search_response['items']:
            result.append({'videoId': item['id']['videoId']})
        
        return JsonResponse({'response': result})

    return render(request, 'index.html')

def downloadMp3(request):
    try:
        url = request.POST.get('url')
        response = "success : " + url
            
        url = 'https://youtu.be/RHNY1hEHdIo?si=oRgoH26NyMHqGoQN'

        youtube = YouTube(url)
            
        video = youtube.streams.filter(only_audio=True).first()

        downloads_path = str(Path.home() / "Downloads")
        fileName = getFileName(downloads_path, youtube.title)
        filePath = f'{downloads_path}\{fileName}'
        video.download(downloads_path)
        
        os.rename(f'{downloads_path}\{video.default_filename}', filePath)

        return JsonResponse({'response': response})
    except Exception as e:
        return JsonResponse({'response': e})

def getFileName(path, _fileName):
    fileNo = 0
    fileName = f'{_fileName}.mp3'
    while(True):
        fileNo += 1
        filePath = f'{path}\{fileName}'
        if os.path.exists(filePath):
            fileName = f'{_fileName}({fileNo}).mp3'
        else:
            return fileName