import subprocess
import time
import schedule
import os
from conf import DING, dinglog, IMG_PATH, VIDEO_PATH, MUSIC_PATH
from jimengmain import generator_video
from webapi.image import generate_image
from webapi.image2 import generate_image2
from datetime import datetime


def gen_image():
    generate_image()
    generate_image2()

def move_image_to_history(img):
    from shutil import move
    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # 创建历史目录
    history_dir = os.path.join(IMG_PATH, "history")
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)
    # 将图片移动到历史目录并添加时间后缀
    new_img_path = os.path.join(history_dir, f"{current_time}_{img}")
    move(os.path.join(IMG_PATH, img), new_img_path)
    print(f"已将 {img} 移动到 {new_img_path}")

def move_video_to_history(img):
    from shutil import move
    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # 创建历史目录
    history_dir = os.path.join(VIDEO_PATH, "history")
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)
    # 将图片移动到历史目录并添加时间后缀
    new_img_path = os.path.join(history_dir, f"{current_time}_{img}")
    move(os.path.join(VIDEO_PATH, img), new_img_path)
    print(f"已将 {img} 移动到 {new_img_path}")

def generator2video():
    # 读取指定目录下的所有图片
    img_list = os.listdir(IMG_PATH)
    # 过滤掉不是jpg 或 png 的文件
    img_list = [img for img in img_list if img.endswith(('.jpg', '.png'))]
    # 随机排序且取10个
    import random
    random.shuffle(img_list)
    img_list = img_list[:20]

    for img in img_list:
        path = generator_video(os.path.join(IMG_PATH, img))
        if path:
            dinglog(f"生成视频成功: {path}")
            move_image_to_history(img)
        else:
            dinglog(f"生成视频失败: {img}")
        break;    

def upload_video(account = "177"):
    # 时间戳
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_video = os.path.join(VIDEO_PATH, f"{timestamp}.mp4")
    print(f"生成视频: {output_video}")
    # 读取视频文件夹
    video_list = os.listdir(VIDEO_PATH)
    video_list = [video for video in video_list if video.endswith(('.mp4', '.avi', '.mov'))]
    # 随机排序且取10个
    import random
    random.shuffle(video_list)
    video_list = video_list[:1]
    if len(video_list) == 0:
        return
    path = os.path.join(VIDEO_PATH, video_list[0])
    # 第三步：添加背景音乐
    subprocess.run([
        "ffmpeg", "-y", "-i", path, "-i", MUSIC_PATH + "/10s.mp3", "-c:v", "copy", "-c:a", "aac", "-shortest", output_video
    ])
    # 删除中间文件
    os.remove(path)

    #  循环10次
    for i in range(10):
        cmd = f'python cli_main.py douyin {account} upload "{output_video}" -pt 0'
        # 在项目根目录下执行命令
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()
        error_msg = ""
        if process.returncode != 0:
            error_msg = stderr.decode()
        print(stdout.decode())
        dinglog(stdout.decode())
        if stdout.decode().find("视频发布成功") != -1:
            move_video_to_history(f"{timestamp}.mp4")
            break;

if __name__ == '__main__':
    # 每天定时生成照片
    schedule.every().day.at("03:20").do(gen_image)

    # 每天定时生成视频
    schedule.every().day.at("05:00").do(generator2video)

    schedule.every().day.at("07:21").do(upload_video)
    schedule.every().day.at("09:11").do(upload_video)
    schedule.every().day.at("12:33").do(upload_video)
    schedule.every().day.at("15:57").do(upload_video)
    schedule.every().day.at("19:14").do(upload_video)
    schedule.every().day.at("22:16").do(upload_video)
    #
    while True:
        schedule.run_pending()
        time.sleep(1)

