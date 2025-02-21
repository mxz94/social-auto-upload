import os
import time

import requests

from conf import IMG_PATH
from utils.files_times import download_image_file

cookies = {
    'webid': '1739944690701vpwqtser',
    'webidExt': '1739944690701vpwqtser',
    'AGL_USER_ID': 'c7290528-a090-46a4-b541-d8e7d5051077',
    '_bl_uid': 'n4mn27wIbgaiah53ya9Id0mfwtde',
    'usertoken': 'd667c940a84348cfb3f67ea6a1b0fe54',
    'pic_newly_favorited_model': 'fc087a41946246c6a1803fcd822a5788',
    'acw_tc': '151472ee-4d6f-4c2a-8335-27661f83e18141ba29aea6989d1edaea7d5741bd1016',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
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
    'token': 'd667c940a84348cfb3f67ea6a1b0fe54',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
    # 'cookie': 'webid=1739944690701vpwqtser; webidExt=1739944690701vpwqtser; AGL_USER_ID=c7290528-a090-46a4-b541-d8e7d5051077; _bl_uid=n4mn27wIbgaiah53ya9Id0mfwtde; usertoken=d667c940a84348cfb3f67ea6a1b0fe54; pic_newly_favorited_model=fc087a41946246c6a1803fcd822a5788; acw_tc=151472ee-4d6f-4c2a-8335-27661f83e18141ba29aea6989d1edaea7d5741bd1016',
}



def generate_image():
    json_data = {
        'checkpointId': 2669985,
        'promptMagic': 0,
        'generateType': 21,
        'frontCustomerReq': {
            'frontId': '4d052cb6-4a71-4835-a356-8f3df78333ca',
            'windowId': '',
            'tabType': 'txt2img',
            'conAndSegAndGen': 'gen',
        },
        'originalPrompt': 'A young woman of East Asian descent sits in a light beige/cream colored chair; she may be in her late teens or early twenties. She is wearing a simple light cream colored button up short sleeve shirt. Her hair is dark brown and tied back in a ponytail. She wears small,understated earrings. She has a light complexion and a thoughtful or pensive expression as she gazes into the camera. She has a slender frame and the background is an indoor space,possibly a classroom or restroom. The lighting is soft and natural and the color palette is subdued and neutral. The background colors are predominantly light beige,cream and navy,providing a soft backdrop for the subject. The composition is simple and straightforward,focusing on the subject and her pose with her arms crossed while standing in front of the camera. The overall style is relaxed,elegant and beautiful. There are some subtle little details in the image such as the button down shirt,earrings and background.,',
        'triggerWords': 'fengyao',
        'text2img': {
            'prompt': 'fengyao,A young woman of East Asian descent sits in a light beige/cream colored chair; she may be in her late teens or early twenties. She is wearing a simple light cream colored button up short sleeve shirt. Her hair is dark brown and tied back in a ponytail. She wears small,understated earrings. She has a light complexion and a thoughtful or pensive expression as she gazes into the camera. She has a slender frame and the background is an indoor space,possibly a classroom or restroom. The lighting is soft and natural and the color palette is subdued and neutral. The background colors are predominantly light beige,cream and navy,providing a soft backdrop for the subject. The composition is simple and straightforward,focusing on the subject and her pose with her arms crossed while standing in front of the camera. The overall style is relaxed,elegant and beautiful. There are some subtle little details in the image such as the button down shirt,earrings and background.,',
            'negativePrompt': 'ng_deepnegative_v1_75t,(badhandv4:1.2),EasyNegative,(worst quality:2),',
            'extraNetwork': '',
            'samplingMethod': 1,
            'samplingStep': 30,
            'width': 1024,
            'height': 1024,
            'imgCount': 1,
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
                'url': 'https://liblibai-online.liblib.cloud/img/e316e54bb4204bf6aa0222d384967333/6e4e07995b23e4397b6a76f3aa0f94d2d79d19b7d385c2e59a4932ee75afe51c.png?x-oss-process=image%2Fresize%2Cm_lfit%2Cw_300%2Ch_300',
                'name': '蜂腰大雷，抖音小红书图文专用',
                'id': 2896091,
                'edit': False,
                'addFlag': True,
                'nickTitle': '蜂腰大雷，抖音小红书图文专用',
                'focus': False,
                'titles': '蜂腰大雷，抖音小红书图文专用',
                'weight': 0.8,
                'type': 0,
                'selectedTriggerWords': [
                    'fengyao',
                ],
                'trigger_word': 'fengyao',
            },
            {
                'modelId': 2903068,
                'modelVersionId': 2903068,
                'modelVersionUuid': '916cfda25c9b4fdda72dd259c3f9168f',
                'modelTypeId': 5,
                'modelName': 'F.1白净可爱美女写真72号_极致逼真人像摄影',
                'modelVersionName': '1.0',
                'modelTypeName': 'LORA',
                'subscribeType': 1,
                'defaultModel': False,
                'nickname': '',
                'cover': 'https://liblibai-online.liblib.cloud/img/df699aeb0f4a4d51adedae2f32b16ff4/6cca2b93a493ee905ba80da0ea17395f3e906712a0f8091ba60914c27e3af9e6.png',
                'suffix': 'safetensors',
                'baseType': 19,
                'needTriggerWord': False,
                'triggerWord': '',
                'hideGenerateInfo': False,
                'sendStatus': 1,
                'showType': 1,
                'vipUsed': 2,
                'userId': 924362,
                'versionIntro': '{"noTriggerWord":1,"loraDes":"F.1白净可爱美女写真7","weight":0.8,"vae":"none","cfg":3.4,"noHdSamplerMethods":1,"ckpt":["2295774"]}',
                'executionScope': '{"defaultScope":"webui","scopes":{"comfy":true,"webui":true}}',
                'auditStatus': 1,
                'isXingliu': 0,
                'addFlag': True,
                'weight': 0.8,
                'url': 'https://liblibai-online.liblib.cloud/img/df699aeb0f4a4d51adedae2f32b16ff4/6cca2b93a493ee905ba80da0ea17395f3e906712a0f8091ba60914c27e3af9e6.png?x-oss-process=image%2Fresize%2Cm_lfit%2Cw_300%2Ch_300',
                'name': 'F.1白净可爱美女写真72号_极致逼真人像摄影',
                'id': 2903068,
                'edit': False,
                'nickTitle': 'F.1白净可爱美女写真72号_极致逼真人像摄影',
                'focus': False,
                'titles': 'F.1白净可爱美女写真72号_极致逼真人像摄影',
                'type': 0,
                'selectedTriggerWords': [],
                'trigger_word': '',
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