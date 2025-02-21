from pathlib import Path
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, CardItem

BASE_DIR = Path(__file__).parent.resolve()
XHS_SERVER = "http://127.0.0.1:11901"
LOCAL_CHROME_PATH = ""   # change me necessary！ for example C:/Program Files/Google/Chrome/Application/chrome.exe

webhook = 'https://oapi.dingtalk.com/robot/send?access_token=17d338657920f9c9ed02c613fb9111043ee9ebf25790b2abb976c084ebde7c70'
secret = 'SEC63370269c233098d22d8b2a7206d2f181de6ada99411697cbaada104e1e9d470'  # 可选：创建机器人勾选“加签”选项时使用
DING = DingtalkChatbot(webhook, secret)

def dinglog(msg):
    DING.send_text(msg)

#  windows
# HEADLESS = False

#  linux
HEADLESS = True

IMG_PATH = "./media/imgs"