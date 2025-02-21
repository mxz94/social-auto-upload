import asyncio
import logging
import sys
import os
from typing import Optional, List
from pathlib import Path
import time
from video_generator import create_video

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VideoManager:
    """视频管理器：统一处理视频生成和下载流程"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    async def process_video_task(self, image_path: str, prompt: str, account: str) -> bool:
        """处理视频任务的完整流程"""
        try:
            # 1. 验证输入参数
            if not image_path or not prompt:
                raise ValueError("图片路径和提示词不能为空")

            if not os.path.exists(image_path):
                raise FileNotFoundError(f"图片文件不存在: {image_path}")
            
            # 2. 生成视频
            self.logger.info(f"开始生成视频...")
            self.logger.info(f"使用图片: {image_path}")
            self.logger.info(f"提示词: {prompt}")
            
            video_id = await create_video(image_path, prompt, account)
            if not video_id:
                raise Exception("视频生成失败")
            
            self.logger.info(f"视频生成成功! 视频ID: {video_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"处理视频任务失败: {str(e)}")
            return False

async def batch_process_videos(tasks: List[dict]) -> List[dict]:
    """批量处理多个视频任务"""
    results = []
    manager = VideoManager()
    
    for task in tasks:
        image_path = task.get('image_path')
        prompt = task.get('prompt')
        list = ["177", "1561", "1562"]
        for account in list:
            isLast = account == list[-1]
                
            try:
                success = await manager.process_video_task(image_path, prompt, account)
                if not success:
                    continue
                results.append({
                    'image_path': image_path,
                    'account': account,
                    'prompt': prompt,
                    'isLast': isLast,
                    'success': success,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                })

                # 任务间隔
                await asyncio.sleep(2)
                break;
            except Exception as e:
                results.append({
                    'image_path': image_path,
                    'prompt': prompt,
                    'isLast': isLast,
                    'success': False,
                    'error': str(e),
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                })
    
    return results

def generator_video(path:str, prompt="move forward"):
    try:
        # 示例任务列表
        tasks = [
            {
                'image_path': path,
                'prompt': prompt,
            }
        ]
        
        # 运行批处理
        results = asyncio.run(batch_process_videos(tasks))
        
        # 输出结果
        logger.info("\n处理结果汇总:")
        for result in results:
            status = "成功" if result['success'] else "失败"
            error_msg = f" - 错误: {result.get('error', 'N/A')}" if not result['success'] else ""
            logger.info(f"图片: {result['image_path']}, 提示词: {result['prompt']}, 状态: {status}{error_msg}")
            return result['image_path']
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        return None

if __name__ == '__main__':
    try:
        # 示例任务列表
        tasks = [
            {
                'image_path': 'scene_017.jpg',
                'prompt': 'move forward',
                'account': '177'
            }
        ]
        
        # 运行批处理
        results = asyncio.run(batch_process_videos(tasks))
        
        # 输出结果
        logger.info("\n处理结果汇总:")
        for result in results:
            status = "成功" if result['success'] else "失败"
            error_msg = f" - 错误: {result.get('error', 'N/A')}" if not result['success'] else ""
            logger.info(f"图片: {result['image_path']}, 提示词: {result['prompt']}, 状态: {status}{error_msg}")
            
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        sys.exit(1) 