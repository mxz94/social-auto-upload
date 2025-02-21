import os
import time

import requests

from conf import IMG_PATH
from utils.files_times import download_image_file

cookies = {
    'webid': '1740118182923yhzrmgiv',
    'webidExt': '1740118182923yhzrmgiv',
    'acw_tc': '1788ad74-d210-46fc-94a9-f6fcee2a55001680807bd456df31002ac40547c8d6b5',
    '_ga': 'GA1.1.1763216903.1740118183',
    '_bl_uid': '10mh47j6eR3dadfmFrmLrmRnh7dd',
    'usertoken': 'ddedf4e304484b0480aa2c3a9161bf3e31661047627d',
    'usertokenExt': 'ddedf4e304484b0480aa2c3a9161bf3e31661047627d',
    '_ga_24MVZ5C982': 'GS1.1.1740118183.1.1.1740118425.59.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.liblib.art',
    'priority': 'u=1, i',
    'referer': 'https://www.liblib.art/v4/editor',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'token': 'ddedf4e304484b0480aa2c3a9161bf3e31661047627d',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
    # 'cookie': 'webid=1740118182923yhzrmgiv; webidExt=1740118182923yhzrmgiv; acw_tc=1788ad74-d210-46fc-94a9-f6fcee2a55001680807bd456df31002ac40547c8d6b5; _ga=GA1.1.1763216903.1740118183; _bl_uid=10mh47j6eR3dadfmFrmLrmRnh7dd; usertoken=ddedf4e304484b0480aa2c3a9161bf3e31661047627d; usertokenExt=ddedf4e304484b0480aa2c3a9161bf3e31661047627d; _ga_24MVZ5C982=GS1.1.1740118183.1.1.1740118425.59.0.0',
}



def generate_image2():
    json_data = {
        'checkpointId': 2669985,
        'promptMagic': 0,
        'generateType': 21,
        'frontCustomerReq': {
            'frontId': 'ba4cc940-1f16-4d86-9c55-7361a877d6bb',
            'windowId': '',
            'tabType': 'txt2img',
            'conAndSegAndGen': 'gen',
        },
        'originalPrompt': 'A young woman of East Asian descent sits in a light beige/cream colored chair; she may be in her late teens or early twenties. She is wearing a simple light cream colored button up short sleeve shirt. Her hair is dark brown and tied back in a ponytail. She wears small,understated earrings. She has a light complexion and a thoughtful or pensive expression as she gazes into the camera. She has a slender frame and the background is an indoor space,possibly a classroom or restroom. The lighting is soft and natural and the color palette is subdued and neutral. The background colors are predominantly light beige,cream and navy,providing a soft backdrop for the subject. The composition is simple and straightforward,focusing on the subject and her pose with her arms crossed while standing in front of the camera. The overall style is relaxed,elegant and beautiful. There are some subtle little details in the image such as the button down shirt,earrings and background.,',
        'triggerWords': 'video picture,caomei,fengyao',
        'text2img': {
            'prompt': 'video picture,caomei,fengyao,A young woman of East Asian descent sits in a light beige/cream colored chair; she may be in her late teens or early twenties. She is wearing a simple light cream colored button up short sleeve shirt. Her hair is dark brown and tied back in a ponytail. She wears small,understated earrings. She has a light complexion and a thoughtful or pensive expression as she gazes into the camera. She has a slender frame and the background is an indoor space,possibly a classroom or restroom. The lighting is soft and natural and the color palette is subdued and neutral. The background colors are predominantly light beige,cream and navy,providing a soft backdrop for the subject. The composition is simple and straightforward,focusing on the subject and her pose with her arms crossed while standing in front of the camera. The overall style is relaxed,elegant and beautiful. There are some subtle little details in the image such as the button down shirt,earrings and background.,',
            'negativePrompt': 'ng_deepnegative_v1_75t,(badhandv4:1.2),EasyNegative,(worst quality:2),',
            'extraNetwork': '',
            'samplingMethod': 1,
            'samplingStep': 30,
            'width': 1024,
            'height': 1024,
            'imgCount': 3,
            'cfgScale': 3.5,
            'seed': -1,
            'seedExtra': 0,
            'clipSkip': 2,
            'randnSource': 0,
            'restoreFaces': 0,
            'hiResFix': 0,
            'tiling': 0,
            'original_prompt': 'A young woman of East Asian descent sits in a light beige/cream colored chair; she may be in her late teens or early twenties. She is wearing a simple light cream colored button up short sleeve shirt. Her hair is dark brown and tied back in a ponytail. She wears small,understated earrings. She has a light complexion and a thoughtful or pensive expression as she gazes into the camera. She has a slender frame and the background is an indoor space,possibly a classroom or restroom. The lighting is soft and natural and the color palette is subdued and neutral. The background colors are predominantly light beige,cream and navy,providing a soft backdrop for the subject. The composition is simple and straightforward,focusing on the subject and her pose with her arms crossed while standing in front of the camera. The overall style is relaxed,elegant and beautiful. There are some subtle little details in the image such as the button down shirt,earrings and background.,',
        },
        'additionalNetwork': [
            {
                'modelId': 18647533,
                'modelVersionId': 18647533,
                'modelVersionUuid': '03ebf15258c64a59825c9cba5b1c4047',
                'modelTypeId': 5,
                'modelName': '绘梦·主宰·F.1人像摄影_分层_分层',
                'modelVersionName': 'v2',
                'modelTypeName': 'LORA',
                'subscribeType': 1,
                'defaultModel': False,
                'nickname': '',
                'cover': 'https://liblibai-online.liblib.cloud/img/0f37258e861044879b8728309c0ac3b0/cbfbad919dc14dc11a97d654c5391683d9e2acd66c239473b55bab39b8908194.png',
                'suffix': 'safetensors',
                'baseType': 19,
                'needTriggerWord': False,
                'triggerWord': 'video picture',
                'hideGenerateInfo': False,
                'sendStatus': 1,
                'showType': 1,
                'vipUsed': 0,
                'userId': 248294,
                'versionIntro': '{"triggerWord":["video picture"],"noTriggerWord":0,"loraDes":"极致","weight":0.8,"vae":"none","hdSamplerMethods":[20],"cfg":3.5,"ckpt":["18420216","18627301"]}',
                'executionScope': '{"defaultScope":"webui","scopes":{"comfy":true,"webui":true}}',
                'auditStatus': 1,
                'isXingliu': 0,
                'url': 'https://liblibai-online.liblib.cloud/img/0f37258e861044879b8728309c0ac3b0/cbfbad919dc14dc11a97d654c5391683d9e2acd66c239473b55bab39b8908194.png?x-oss-process=image%2Fresize%2Cm_lfit%2Cw_300%2Ch_300',
                'name': '绘梦·主宰·F.1人像摄影_分层_分层',
                'id': 18647533,
                'edit': False,
                'addFlag': True,
                'nickTitle': '绘梦·主宰·F.1人像摄影_分层_分层',
                'focus': False,
                'titles': '绘梦·主宰·F.1人像摄影_分层_分层',
                'weight': 0.8,
                'type': 0,
                'selectedTriggerWords': [
                    'video picture',
                ],
                'trigger_word': 'video picture',
            },
            {
                'modelId': 18508504,
                'modelVersionId': 18508504,
                'modelVersionUuid': '4664412d054246809e3311919406af3f',
                'modelTypeId': 5,
                'modelName': '抖音快手流量密码，自拍,露背',
                'modelVersionName': '手机自拍，露背',
                'modelTypeName': 'LORA',
                'subscribeType': 1,
                'defaultModel': False,
                'nickname': '',
                'cover': 'https://liblibai-online.liblib.cloud/img/9f625da6d4e242e9bc43d64d7b801155/a654e3956faf201dc84847817317a47909e4e3a34bd982b426ee24f0d1c2f3c3.png',
                'suffix': 'safetensors',
                'baseType': 19,
                'needTriggerWord': False,
                'triggerWord': 'caomei',
                'hideGenerateInfo': False,
                'sendStatus': 1,
                'showType': 1,
                'vipUsed': 0,
                'userId': 2110834,
                'versionIntro': '{"triggerWord":["caomei"],"loraDes":"可以和任何大模型搭配","weight":0.8,"vae":"none","cfg":3.5,"noHdSamplerMethods":1,"ckpt":["2469081","2777773"]}',
                'executionScope': '',
                'auditStatus': 1,
                'isXingliu': 0,
                'addFlag': True,
                'weight': 0.8,
                'url': 'https://liblibai-online.liblib.cloud/img/9f625da6d4e242e9bc43d64d7b801155/a654e3956faf201dc84847817317a47909e4e3a34bd982b426ee24f0d1c2f3c3.png?x-oss-process=image%2Fresize%2Cm_lfit%2Cw_300%2Ch_300',
                'name': '抖音快手流量密码，自拍,露背',
                'id': 18508504,
                'edit': False,
                'nickTitle': '抖音快手流量密码，自拍,露背',
                'focus': False,
                'titles': '抖音快手流量密码，自拍,露背',
                'type': 0,
                'selectedTriggerWords': [
                    'caomei',
                ],
                'trigger_word': 'caomei',
            },
            {
                'modelId': 2896091,
                'modelVersionId': 2896091,
                'modelVersionUuid': 'fdf30e2a449f476da6a678f5391d3ca4',
                'modelTypeId': 5,
                'modelName': '蜂腰大雷，抖音小红书图文专用',
                'modelVersionName': 'v1.0',
                'modelTypeName': 'LORA',
                'subscribeType': 1,
                'defaultModel': False,
                'nickname': '',
                'cover': 'https://liblibai-online.liblib.cloud/img/e316e54bb4204bf6aa0222d384967333/6e4e07995b23e4397b6a76f3aa0f94d2d79d19b7d385c2e59a4932ee75afe51c.png',
                'suffix': 'safetensors',
                'baseType': 19,
                'needTriggerWord': False,
                'triggerWord': 'fengyao',
                'hideGenerateInfo': False,
                'sendStatus': 1,
                'showType': 1,
                'vipUsed': 2,
                'userId': 568731,
                'versionIntro': '{"triggerWord":["fengyao"],"loraDes":"完美身材，蜂腰大雷","weight":0.8,"vae":"none","cfg":3.5,"noHdSamplerMethods":1,"ckpt":["2295774"]}',
                'executionScope': '{"defaultScope":"webui","scopes":{"comfy":true,"webui":true}}',
                'auditStatus': 1,
                'isXingliu': 0,
                'addFlag': True,
                'weight': 0.8,
                'url': 'https://liblibai-online.liblib.cloud/img/e316e54bb4204bf6aa0222d384967333/6e4e07995b23e4397b6a76f3aa0f94d2d79d19b7d385c2e59a4932ee75afe51c.png?x-oss-process=image%2Fresize%2Cm_lfit%2Cw_300%2Ch_300',
                'name': '蜂腰大雷，抖音小红书图文专用',
                'id': 2896091,
                'edit': False,
                'nickTitle': '蜂腰大雷，抖音小红书图文专用',
                'focus': False,
                'titles': '蜂腰大雷，抖音小红书图文专用',
                'type': 0,
                'selectedTriggerWords': [
                    'fengyao',
                ],
                'trigger_word': 'fengyao',
            },
        ],
        'taskQueuePriority': 1,
    }
    while True:
        response = requests.post('https://www.liblib.art/gateway/sd-api/generate/image', cookies=cookies, headers=headers, json=json_data)
        data = response.json()
        print(data)
        if data["code"] != 0:
            break


        json_data2 = {
            'flag': 0,
        }
        while True:
            # 休眠2s
            time.sleep(4)
            response = requests.post(
                f'https://www.liblib.art/gateway/sd-api/generate/progress/msg/v3/{data["data"]}',
                cookies=cookies,
                headers=headers,
                json=json_data2,
            )
            data2 = response.json()
            print(data2)
            img_list = data2["data"]["images"]
            if img_list:
                for item in img_list:
                    print(item["previewPath"])
                    download_image_file(item["previewPath"], os.path.join(IMG_PATH, item["previewPath"].split("/")[-1]))
                break