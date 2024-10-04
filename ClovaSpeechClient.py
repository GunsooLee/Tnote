import requests
import json
# import ssl
from time import sleep

#ssl._create_default_https_context = ssl._create_unverified_context

class ClovaSpeechClient:
    # Clova Speech invoke URL
    invoke_url = 'https://clovaspeech-gw.ncloud.com/external/v1/9174/5fc4aeab8b3fdd113df9f7e445550eb8f9c0b085a429272173e84df9e977b87c'
    # Clova Speech secret key
    secret = 'b71e5626a6a745e5b0c586e9c822a0ee' #유료 api
    
    # 인증서 파일 경로
    # cert_file_path = 'C:/Users/User/Downloads/Clova_Util/ncloud_CA.pem'

    def req_url(self, url, completion, callback=None, userdata=None, forbiddens=None, boostings=None, wordAlignment=True, fullText=True, diarization=None, sed=None):
        request_body = {
            'url': url,
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
            'sed': sed,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        return requests.post(headers=headers,
                             url=self.invoke_url + '/recognizer/url',
                             data=json.dumps(request_body).encode('UTF-8'), verify=False)

    def req_object_storage(self, data_key, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                           wordAlignment=True, fullText=True, diarization=None, sed=None):
        request_body = {
            'dataKey': data_key,
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
            'sed': sed,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        return requests.post(headers=headers,
                             url=self.invoke_url + '/recognizer/object-storage',
                             data=json.dumps(request_body).encode('UTF-8'), verify=False)

    def req_upload(self, file, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                   wordAlignment=True, fullText=True, diarization=None, sed=None):
        request_body = {
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
            'sed': sed,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        print(json.dumps(request_body, ensure_ascii=False).encode('UTF-8'))
        files = {
            'media': open(file, 'rb'),
            'params': (None, json.dumps(request_body, ensure_ascii=False).encode('UTF-8'), 'application/json')
        }
        response = requests.post(headers=headers, url=self.invoke_url + '/recognizer/upload', files=files, verify=False)
        return response

    def getSttSpeakResult(self):
        
        res = ClovaSpeechClient().req_upload(file='C:/Users/Emily/Downloads/T-Lab주제선정 녹음.m4a', completion='sync') #파일 업로드
        #print(res.text)
        
        json_obj = json.loads(res.text)
        
        #graph를 위한 result
        speaker_result = [] 
        speakers_arr = json_obj['speakers']
        segments_arr = json_obj['segments']

        for speaker in speakers_arr:
            tmp = speaker['label']
            text_edited = ''

            for segment in segments_arr:
                speaker_label = segment['speaker']['label']
                if tmp == speaker_label:
                    puct_delete = segment['textEdited'].replace('"', '').replace('.', ' ')
                    text_edited += puct_delete + ' '  

            speaker_result.append(text_edited.strip())  

        # 결과 출력 (맨 마지막 쉼표 제거)
        #print(', '.join(speaker_result))
        
        #print('\n'.join(stt_result))
        
        return speaker_result
    
    def getSttAllResult(self):
        
        res = ClovaSpeechClient().req_upload(file='C:/Users/Emily/Downloads/T-Lab주제선정 녹음.m4a', completion='sync') #파일 업로드
        #print(res.text)
        
        json_obj = json.loads(res.text)
        
        #회의록 녹취록 전문 위한 result
        stt_result = []

        segments_arr = json_obj['segments']
      
        for segment in segments_arr:
            speaker_label = segment['speaker']['label']
            stt_result.append(('화자'+speaker_label+': '+segment['textEdited']).strip())        
        
        return stt_result
    
    def getSttAllResultDf(self,save_path):
        
        res = ClovaSpeechClient().req_upload(file=save_path, completion='sync') #파일 업로드
        #print(res.text)
        
        json_obj = json.loads(res.text)
        
        #회의록 녹취록 전문 위한 result
        result = []

        segments_arr = json_obj['segments']
      
        for segment in segments_arr:
            stt_result = []
            speaker_label = segment['speaker']['label']
            stt_result.append('화자'+speaker_label)    
            stt_result.append(segment['textEdited'])  
            result.append(stt_result)
        
        return result
        