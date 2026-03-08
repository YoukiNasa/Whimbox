import json
import threading
from pathlib import Path
from typing import Optional
from win10toast import ToastNotifier
from whimbox.utils.logger import logger

class NotifyService:
    def __init__(self):
        self._toaster: Optional[ToastNotifier] = None
        self._enabled = False
        self._icon: Optional[str] = None
        try:
            self._toaster = ToastNotifier()
            logger.info("Windows 通知已启用")
            self._enabled = True
        except Exception as e:
            logger.error(f"初始化通知失败: {e}")
            

    def send(self, title: str, message: str, duration: int = 5, icon_path: Optional[str] = None):
        if not self._enabled or not self._toaster or not message:
            return

        ico = icon_path or self._icon

        def _show():
            try:
                self._toaster.show_toast(title, message, icon_path=ico, duration=duration, threaded=False)
            except Exception as e:
                logger.error(f"发送通知失败: {e}")

        threading.Thread(target=_show, daemon=True).start()