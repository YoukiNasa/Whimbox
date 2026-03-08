import numpy as np

from ctypes.wintypes import HWND
from winrt.windows.media.capture import MediaCapture
from winrt.windows.graphics.directx import DirectXPixelFormat
from winrt.windows.ai.machinelearning import LearningModelDevice, LearningModelDeviceKind
from winrt.windows.graphics.capture import Direct3D11CaptureFramePool, Direct3D11CaptureFrame
from winrt.windows.graphics.capture.interop import create_for_window
from whimbox.utils.platform.base import CaptureServiceBase
from whimbox.utils.platform.windows.misc import find_window_by_title, find_window_by_process, wait_for

class CaptureService(CaptureServiceBase):
    def __init__(self, game_config: dict):
        self._hwnd = self._find_window(
                game_config.get("window_title"),
                game_config.get("process_name")
            )
        self._device = self._get_direct3d_device() 
        self._is_running = False

    def _find_window(self, window_title: str, process_name: str) -> HWND:
        """通过窗口标题或进程名查找窗口句柄"""
        if not window_title and not process_name:
            raise ValueError("必须提供窗口标题或进程名以查找窗口句柄")

        if window_title:
            hwnd = find_window_by_title(window_title)

        # if not hwnd and process_name:
        #     hwnd = find_window_by_process(process_name)

        if hwnd:
            return hwnd
        else:
            raise ValueError("未找到窗口句柄")

    def _get_direct3d_device(self):
        """获取Direct3D设备，支持多种获取方式以提高兼容性"""
        media_capture = MediaCapture()
        wait_for(media_capture.initialize_async())
        device = media_capture.media_capture_settings.direct3d11_device
        if device:
            return device

        # 尝试通过机器学习设备获取高性能Direct3D设备
        device = LearningModelDevice(LearningModelDeviceKind.DIRECTX_HIGH_PERFORMANCE).direct3d11_device
        if device:
            return device
        else:
            raise RuntimeError("无法初始化Direct3D设备")

    def _create_frame_pool(self):
        """创建帧缓冲池，确保资源正确初始化"""
        if self._frame_pool:
            self._frame_pool.close()

        self._capture_item = create_for_window(self._hwnd)
        
        self._frame_pool = Direct3D11CaptureFramePool.create_free_threaded(
            self._device,
            DirectXPixelFormat.B8_G8_R8_A8_UINT_NORMALIZED,  # BGRA格式
            1,  # 缓冲池大小
            self._capture_item.size
        )
        
        # 创建并配置捕获会话
        self._session = self._frame_pool.create_capture_session(self._capture_item)
        self._session.is_border_required = False  # 不捕获窗口边框
        self._session.is_cursor_capture_enabled = False  # 不捕获鼠标光标
        self._is_running = True

    def capture_frame(self) -> np.ndarray:

        pass
    