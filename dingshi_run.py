import subprocess
import time
import schedule
import os
from conf import DING, dinglog, IMG_PATH
from jimengmain import generator_video

def move_image_to_history(img):
    from shutil import move
    from datetime import datetime
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
def generator2video():
    # 读取指定目录下的所有图片
    img_list = os.listdir(IMG_PATH)
    # 过滤掉不是jpg 或 png 的文件
    img_list = [img for img in img_list if img.endswith(('.jpg', '.png'))]
    for img in img_list:
        path = generator_video(os.path.join(IMG_PATH, img))
        if path:
            dinglog(f"生成视频成功: {path}")
            move_image_to_history(img)
        else:
            dinglog(f"生成视频失败: {img}")
        break;    

# def upload_video(account, path):
#     cmd = f'python cli_main.py douyin {account} upload "{path}" -pt 0'
#     # 在项目根目录下执行命令
#     process = subprocess.Popen(
#         cmd,
#         shell=True,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#     )
#     stdout, stderr = process.communicate()
#     error_msg = ""
#     if process.returncode != 0:
#         error_msg = stderr.decode()
#     return error_msg
#
# def job():
#     print("发布任务执行！")
#
# # 定义每天的执行时间
# schedule.every().day.at("09:00").do(job)
# schedule.every().day.at("12:00").do(job)
# schedule.every().day.at("15:00").do(job)
# schedule.every().day.at("18:00").do(job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)


if __name__ == '__main__':
    generator2video()