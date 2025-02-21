import asyncio
import logging
import sys
import re
import traceback
from typing import Optional, List
from playwright.async_api import Page, async_playwright, TimeoutError
import os
import json
import aiohttp
from urllib.parse import urlparse
from pathlib import Path

# 常量定义
STORAGE_STATE_PATH = "./cookies/auth.json"
VIDEO_DIR = "./media/videos"
LOGIN_URL = "https://jimeng.jianying.com/user/login"
GENERATE_URL = "https://jimeng.jianying.com/ai-tool/video/generate"

class VideoDownloader:
    """视频下载器"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if not os.path.exists(VIDEO_DIR):
            os.makedirs(VIDEO_DIR)
    
    async def download_file(self, url: str, filename: str) -> bool:
        """下载文件"""
        try:
            # 确保文件名以.mp4结尾
            if not filename.lower().endswith('.mp4'):
                filename = os.path.splitext(filename)[0] + '.mp4'
                
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        file_path = os.path.join(VIDEO_DIR, filename)
                        with open(file_path, 'wb') as f:
                            while True:
                                chunk = await response.content.read(8192)
                                if not chunk:
                                    break
                                f.write(chunk)
                        self.logger.info(f"文件下载成功: {file_path}")
                        return True
                    else:
                        self.logger.error(f"下载失败，状态码: {response.status}")
                        return False
        except Exception as e:
            self.logger.error(f"下载出错: {str(e)}")
            return False

class JiMengClient:
    """即梦视频生成客户端"""
    def __init__(self, account:str):
        self.logger = logging.getLogger(__name__)
        self.page: Optional[Page] = None 
        self.browser = None
        self.context = None
        self.playwright = None
        self.video_urls = []
        self.downloader = VideoDownloader()
        self.account = STORAGE_STATE_PATH.replace("auth.json", f"auth{account}.json")

    async def check_login_status(self) -> bool:
        """检查登录状态是否有效"""
        try:
            if not os.path.exists(self.account):
                self.logger.info("登录状态文件不存在")
                return False

            with open(self.account, 'r', encoding='utf-8') as f:
                storage_state = json.load(f)
                
            if not storage_state.get('cookies'):
                self.logger.info("登录状态文件中没有cookies信息")
                return False

            # 验证登录状态
            await self.page.goto(GENERATE_URL, wait_until="networkidle", timeout=30000)
            try:
                # 等待登录状态指示元素
                await self.page.wait_for_selector(
                    'div[class*="avatarContainer-"], div[class*="creditWrapper-"]',
                    state="visible",
                    timeout=10000
                )
                self.logger.info("登录状态有效")
                return True
            except TimeoutError:
                self.logger.info("登录状态已失效")
                return False

        except Exception as e:
            self.logger.error(f"检查登录状态时出错: {str(e)}")
            return False

    async def login(self) -> bool:
        """执行登录流程"""
        try:
            self.logger.info("开始登录流程...")
            await self.page.goto(LOGIN_URL, wait_until="networkidle", timeout=30000)
            
            # 等待用户手动登录
            self.logger.info("请在浏览器中手动完成登录...")
            try:
                # 等待登录成功的标志
                await self.page.wait_for_selector(
                    'div[class*="avatarContainer-"], div[class*="creditWrapper-"]',
                    state="visible",
                    timeout=300000  # 给用户5分钟时间登录
                )
                
                # 保存登录状态
                storage_state = await self.context.storage_state(path=STORAGE_STATE_PATH)
                self.logger.info("登录成功，已保存登录状态")
                return True
                
            except TimeoutError:
                self.logger.error("登录超时，请重试")
                return False
                
        except Exception as e:
            self.logger.error(f"登录过程出错: {str(e)}")
            return False

    async def initialize(self) -> None:
        """初始化Playwright浏览器"""
        try:
            self.playwright = await async_playwright().start()
            
            # 配置浏览器启动参数
            browser_args = [
                '--disable-blink-features=AutomationControlled',  # 禁用自动化检测
                '--disable-infobars',  # 禁用信息栏
                '--start-maximized',  # 最大化窗口
                '--no-sandbox',  # 禁用沙箱
                '--disable-setuid-sandbox',  # 禁用setuid沙箱
                '--disable-dev-shm-usage',  # 禁用/dev/shm使用
                '--no-first-run',  # 禁用首次运行界面
                '--no-default-browser-check',  # 禁用默认浏览器检查
                '--disable-gpu',  # 禁用GPU加速
                '--disable-extensions',  # 禁用扩展
                '--disable-background-networking',  # 禁用后台网络
                '--disable-background-timer-throttling',  # 禁用后台定时器限制
                '--disable-backgrounding-occluded-windows',  # 禁用后台窗口限制
                '--disable-breakpad',  # 禁用崩溃报告
                '--disable-component-extensions-with-background-pages',  # 禁用带后台页面的组件扩展
                '--disable-features=TranslateUI,BlinkGenPropertyTrees',  # 禁用一些特性
                '--disable-ipc-flooding-protection',  # 禁用IPC洪水保护
                '--enable-automation',  # 启用自动化
                '--password-store=basic'  # 使用基本密码存储
            ]

            # 启动浏览器
            self.browser = await self.playwright.chromium.launch(
                headless=False,
                args=browser_args,
                channel='chrome'  # 使用已安装的Chrome
            )
            
            # 创建上下文
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                locale='zh-CN',
                timezone_id='Asia/Shanghai',
                permissions=['camera', 'microphone', 'geolocation'],
                ignore_https_errors=True
            )
            
            # 修改浏览器指纹
            await self.context.add_init_script("""
                // 隐藏自动化特征
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                
                // 模拟真实的navigator属性
                Object.defineProperty(navigator, 'platform', {
                    get: () => 'Win32'
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['zh-CN', 'zh', 'en']
                });
                
                // 添加Chrome特有的属性
                window.chrome = {
                    runtime: {}
                };
                
                // 修改检测属性
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
            """)
            
            self.page = await self.context.new_page()
            
            # 设置更长的默认超时时间
            self.page.set_default_timeout(60000)
            
            # 启用JavaScript控制台日志
            self.page.on("console", lambda msg: self.logger.debug(f"浏览器控制台: {msg.text}"))
            
            # 监听网络请求
            self.page.on("response", self.handle_response)

            # 处理登录状态
            if os.path.exists(self.account):
                with open(self.account, 'r', encoding='utf-8') as f:
                    storage_state = json.load(f)
                    await self.context.add_cookies(storage_state.get('cookies', []))
            
            # 验证登录状态
            if not await self.check_login_status():
                if not await self.login():
                    raise Exception("登录失败")
            
            self.logger.info("初始化完成")
            
        except Exception as e:
            error_msg = f"初始化失败: {str(e)}\n{traceback.format_exc()}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

    async def handle_response(self, response):
        """处理网络响应"""
        try:
            url = response.url
            if ('vlabvod.com' in url.lower() and 
                any(ext in url.lower() for ext in ['.mp4', '.m3u8']) and 
                'video' in url.lower()):
                self.logger.info(f"捕获到视频URL: {url}")
                if url not in self.video_urls:  # 避免重复
                    self.video_urls.append(url)
        except Exception as e:
            self.logger.error(f"处理响应时出错: {str(e)}")

    async def wait_for_video_url(self):
        """等待视频元素加载完成"""
        try:
            # 使用evaluate获取所有视频元素
            videos = await self.page.evaluate("""
                () => {
                    const videos = document.querySelectorAll('video');
                    return Array.from(videos).map(v => ({
                        src: v.src,
                        readyState: v.readyState,
                        visible: v.offsetParent !== null
                    }));
                }
            """)
            
            # 检查是否有可用的视频
            for video in videos:
                if video['src'] and video['visible'] and video['readyState'] >= 2:
                    self.logger.info(f"找到可用视频: {video['src']}")
                    if video['src'] not in self.video_urls:
                        self.video_urls.append(video['src'])
                    return True
            
            return False
        except Exception as e:
            self.logger.error(f"等待视频元素时出错: {str(e)}")
            return False

    async def create_video(self, image_path: str, video_prompt: str) -> Optional[str]:
        """创建视频"""
        try:
            # 访问目标网页
            self.logger.info("正在加载页面...")
            await self.page.goto("https://jimeng.jianying.com/ai-tool/video/generate", 
                              wait_until="networkidle",
                              timeout=60000)
            
            # 等待页面完全加载
            await asyncio.sleep(5)
            
            # 检查登录状态
            self.logger.info("验证登录状态...")
            try:
                await self.page.wait_for_selector('div[class*="avatarContainer-"], div[class*="creditWrapper-"]', 
                                              state="visible",
                                              timeout=10000)
                self.logger.info("登录状态验证成功")
            except TimeoutError:
                self.logger.error("登录状态验证失败，请检查登录信息是否过期")
                return None
            element = self.page.locator('#platform')
            text_content = await element.inner_text()  # 或者使用 element.text_content()

            element = self.page.get_by_label("", exact=True).locator("svg")
            if element:
                await element.click()
            # 使用正则表达式提取数字
            fen = 100
            numbers = re.findall(r'\d+', text_content)  # 匹配所有数字
            if numbers:
                fen = int(numbers[0])
                self.logger.info(fen)
            else:
                print('没有找到数字')
            if fen < 20:
                return None
            if image_path:
                self.logger.info("等待上传组件加载...")
                try:
                    # 尝试多个可能的选择器
                    selectors = [
                        'input[type="file"]',
                        'input[accept*="image"]',
                        'input[type="file"][accept*="image"]'
                    ]
                    
                    file_input = None
                    for selector in selectors:
                        try:
                            file_input = await self.page.wait_for_selector(selector, timeout=10000, state='attached')
                            if file_input:
                                break
                        except:
                            continue
                    
                    if not file_input:
                        raise Exception("无法找到文件上传输入框")
                    
                    self.logger.info("开始上传图片...")
                    await file_input.set_input_files(image_path)
                    await asyncio.sleep(5)
                    self.logger.info("图片上传完成")
                except Exception as e:
                    self.logger.error(f"上传图片失败: {str(e)}")
                    raise e

            # 填写提示词
            self.logger.info("填写提示词...")
            try:
                textarea = await self.page.wait_for_selector('textarea', timeout=10000)
                if not textarea:
                    raise Exception("无法找到提示词输入框")
                await textarea.fill(video_prompt)
                await asyncio.sleep(2)
            except Exception as e:
                self.logger.error(f"填写提示词失败: {str(e)}")
                raise e
            # 修改为10s
            await self.page.locator("div").filter(has_text=re.compile(r"^视频 S2\.0by Seaweed alpha$")).nth(1).click()
            await self.page.locator("div").filter(has_text=re.compile(r"^视频 P2\.0 Pro精准响应提示词, 支持生成多镜头$")).first.click()
            if fen > 40:
                await self.page.get_by_text("10s").click()

            # 等待生成接口响应
            self.logger.info("准备生成视频...")
            try:
                # 创建响应等待事件
                async with self.page.expect_response(
                    lambda response: "mweb/v1/generate_video" in response.url,
                    timeout=30000
                ) as response_info:
                    # 点击生成按钮
                    generate_button = await self.page.wait_for_selector('div[class*="generateButton-"]', timeout=10000)
                    if not generate_button:
                        raise Exception("无法找到生成按钮")
                    
                    self.logger.info("点击生成按钮...")
                    await generate_button.click()
                    
                    # 等待响应
                    self.logger.info("等待视频生成...")
                    response = await response_info.value
                    response_data = await response.json()
                
                video_id = None
                if response_data.get('data', {}).get('aigc_data'):
                    flow = response_data['data']['aigc_data']['task']['process_flows'][0]
                    video_id = flow.get("history_id", "")
                    self.logger.info(f"获取视频ID: {video_id}")
                    
                    # 等待视频生成完成
                    self.logger.info("等待视频生成完成...")
                    progress = 0
                    retry_count = 0
                    max_retries = 60  # 最多等待5分钟 (60 * 5秒)
                    
                    while progress < 100 and retry_count < max_retries:
                        try:
                            # 获取进度条元素
                            progress_element = await self.page.wait_for_selector(
                                'div.lv-progress-circle-text',
                                timeout=5000
                            )
                            if progress_element:
                                progress_text = await progress_element.text_content()
                                current_progress = int(progress_text.replace('%', ''))
                                if current_progress != progress:
                                    progress = current_progress
                                    self.logger.info(f"视频生成进度: {progress}%")
                        except Exception as e:
                            self.logger.debug(f"获取进度失败: {str(e)}")
                        
                        # 检查是否已经生成完成
                        try:
                            processing = await self.page.query_selector('div.processing-FLhhee')
                            if not processing:
                                self.logger.info("视频生成完成")
                                break
                        except:
                            pass
                            
                        retry_count += 1
                        await asyncio.sleep(5)
                    
                    if retry_count >= max_retries:
                        self.logger.error("视频生成超时")
                        return None
                    
                    # 等待视频URL出现
                    self.logger.info("等待视频URL...")
                    retry_count = 0
                    video_found = False
                    
                    while not video_found and retry_count < 30:
                        video_found = await self.wait_for_video_url()
                        if not video_found:
                            retry_count += 1
                            self.logger.info(f"重试等待视频 ({retry_count}/30)...")
                            await asyncio.sleep(2)
                    
                    if self.video_urls:
                        video_url = self.video_urls[-1]  # 使用最后捕获的URL
                        # 确保文件名以.mp4结尾
                        filename = f"{video_id}_{Path(urlparse(video_url).path).stem}.mp4"
                        self.logger.info(f"开始下载视频: {filename}")
                        await self.downloader.download_file(video_url, filename)
                    else:
                        self.logger.warning("未能捕获到视频URL")
                else:
                    self.logger.error("未能获取到视频ID")

                return filename

            except Exception as e:
                self.logger.error(f"生成视频过程中出错: {str(e)}")
                raise e
            
        except Exception as e:
            self.logger.error(f"创建视频失败: {str(e)}")
            return None

    async def close(self) -> None:
        """关闭浏览器资源"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            self.logger.error(f"关闭资源时出错: {e}")

async def create_video(image_path: str, video_prompt: str, account: str) -> Optional[str]:
    """创建视频主函数"""
    client = None
    try:
        if sys.platform == 'win32':
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)
        
        client = JiMengClient(account)
        await client.initialize()
        return await client.create_video(image_path, video_prompt)
        
    except Exception as e:
        logging.error(f"创建视频失败: {e}")
        return None
    finally:
        if client:
            await client.close()

if __name__ == '__main__':
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    # 示例参数
    image_path = r"scene_017.jpg"
    prompt = "一个女孩，正在等待飞机起飞。她高兴的扮了个鬼脸"

    try:
        # 参数验证
        if not image_path or not prompt:
            raise ValueError("图片路径和提示词不能为空")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")

        logger.info(f"开始生成视频...")
        logger.info(f"使用图片: {image_path}")
        logger.info(f"提示词: {prompt}")

        # 运行视频生成
        video_id = asyncio.run(create_video(image_path, prompt, "177"))
        
        if video_id:
            logger.info(f"视频生成成功! 视频ID: {video_id}")
        else:
            logger.error("视频生成失败")

    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        traceback.print_exc()
        sys.exit(1)