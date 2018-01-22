#1 네이버 음성합성 Open API 예제
import os
import sys
import urllib.request
client_id = "N_vYp3KR4GNFfVsLzN87"
client_secret = "72R5VwJAyZ"

def naverVoiceApi(txt):
    encText = urllib.parse.quote(txt)
    data = "speaker=mijin&speed=0&text=" + encText;
    url = "https://openapi.naver.com/v1/voice/tts.bin"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    if(rescode==200):
        #print("TTS mp3 저장")
        response_body = response.read()
        with open('result.mp3', 'wb') as f:
            f.write(response_body)
    else:
        print("Error Code:" + rescode)