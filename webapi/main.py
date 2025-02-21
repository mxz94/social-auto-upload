import subprocess
from typing import List
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
import shutil
import os
import logging

app = FastAPI(
    title="我的 FastAPI 应用",
    description="这是一个示例 FastAPI 应用",
    version="1.0.0"
)

# 模拟数据库
items_db = []

@app.get("/")
async def root():
    return {"message": "欢迎使用 FastAPI!"}

#   视频倒放 + 背景音乐
def kuoaddmusic(input_video):
    import subprocess
    import os

    # 定义输入和输出文件
    reversed_video = "reversed_video.mp4"
    output_video = "output_video.mp4"
    background_music = "musics/10s.mp3"

    # 第一步：倒放视频
    subprocess.run([
        "ffmpeg", "-y", "-i", input_video, "-vf", "reverse,setpts=N/FRAME_RATE/TB", "-an", reversed_video
    ])

    # 第二步：连接原视频和倒放视频
    subprocess.run([
        "ffmpeg", "-y", "-i", input_video, "-i", reversed_video,
        "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p,trim=duration=10;[0:v]fade=t=out:st=9.5:d=0.5[v0];[1:v]fade=t=in:st=0:d=0.5[v1];[v0][v1]concat=n=2:v=1:a=0",
        output_video
    ])

    # 第三步：添加背景音乐
    subprocess.run([
        "ffmpeg", "-y", "-i", output_video, "-i", background_music, "-c:v", "copy", "-c:a", "aac", "-shortest", input_video
    ])

    # 删除中间文件
    os.remove(reversed_video)
    os.remove(output_video)
@app.post(path= "/upload/", summary="douyin上传视频api")
async def upload_video(
        video: UploadFile = File(...),
        title: str = Form(...),
        desc: str = Form(...),
        account: str = Form(...),
        kuo: bool = Form(False)
):
    # 检查文件类型
    if not video.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="请上传视频文件")



    # 保存视频文件
    video_path = f"videos/{title}.mp4"
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    if kuo:
        kuoaddmusic(video_path)

    # 保存描述文件
    text_path = f"videos/{title}.txt"
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(f"{title}\n{desc}")


    # 执行 shell 命令
    cmd = f'python cli_main.py douyin {account} upload "./videos/{title}.mp4" -pt 0'
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


    return {
        "message": "上传并处理成功",
        "video_path": video_path,
        "text_path": text_path,
        "command_output": stdout.decode(),
        "error_msg": error_msg
    }