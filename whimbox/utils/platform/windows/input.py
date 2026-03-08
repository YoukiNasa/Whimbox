import time
from typing import Tuple, Optional, List
import win32api
import win32con
from whimbox.utils.platform.base.input import InputServiceBase, InputConfig, KeyCode, MouseButton

class InputService(InputServiceBase):
    """
    Windows平台输入服务实现
    """
    
    # Windows虚拟键码映射表
    VK_CODE_MAP = {
        # 字母
        KeyCode.A: 0x41, KeyCode.B: 0x42, KeyCode.C: 0x43, KeyCode.D: 0x44,
        KeyCode.E: 0x45, KeyCode.F: 0x46, KeyCode.G: 0x47, KeyCode.H: 0x48,
        KeyCode.I: 0x49, KeyCode.J: 0x4A, KeyCode.K: 0x4B, KeyCode.L: 0x4C,
        KeyCode.M: 0x4D, KeyCode.N: 0x4E, KeyCode.O: 0x4F, KeyCode.P: 0x50,
        KeyCode.Q: 0x51, KeyCode.R: 0x52, KeyCode.S: 0x53, KeyCode.T: 0x54,
        KeyCode.U: 0x55, KeyCode.V: 0x56, KeyCode.W: 0x57, KeyCode.X: 0x58,
        KeyCode.Y: 0x59, KeyCode.Z: 0x5A,
        # 功能键
        KeyCode.ESCAPE: win32con.VK_ESCAPE,
        KeyCode.TAB: win32con.VK_TAB,
        KeyCode.SHIFT: win32con.VK_SHIFT,
        KeyCode.CTRL: win32con.VK_CONTROL,
        KeyCode.ALT: win32con.VK_MENU,
        KeyCode.SPACE: win32con.VK_SPACE,
        KeyCode.BACKSPACE: win32con.VK_BACK,
        KeyCode.ENTER: win32con.VK_RETURN,
        # F1-F9
        KeyCode.F1: win32con.VK_F1, KeyCode.F2: win32con.VK_F2,
        KeyCode.F3: win32con.VK_F3, KeyCode.F4: win32con.VK_F4,
        KeyCode.F5: win32con.VK_F5, KeyCode.F6: win32con.VK_F6,
        KeyCode.F7: win32con.VK_F7, KeyCode.F8: win32con.VK_F8,
        KeyCode.F9: win32con.VK_F9,
    }
    
    # 鼠标按钮映射
    MOUSE_BUTTON_MAP = {
        MouseButton.LEFT: (win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP),
        MouseButton.RIGHT: (win32con.MOUSEEVENTF_RIGHTDOWN, win32con.MOUSEEVENTF_RIGHTUP),
        MouseButton.MIDDLE: (win32con.MOUSEEVENTF_MIDDLEDOWN, win32con.MOUSEEVENTF_MIDDLEUP),
    }
    
    # Windows滚轮增量，通常为120
    WHEEL_DELTA = 120
    
    def __init__(self, config: InputConfig):
        super().__init__(config)
        self._pressed_keys = set()  # 跟踪当前按下的键
        
    def initialize(self) -> bool:
        """初始化Windows输入服务"""
        try:
            # 验证必要的Windows API可用
            win32api.GetCursorPos()
            self._initialized = True
            return True
        except Exception as e:
            print(f"WindowsInputService初始化失败: {e}")
            return False
    
    def cleanup(self):
        """清理资源，释放所有按下的键"""
        # 释放所有未释放的按键，防止按键卡住
        for key in list(self._held_keys):
            try:
                self.release_key(key)
            except:
                pass
        self._held_keys.clear()
        self._initialized = False
    
    def _get_vk_code(self, key: KeyCode) -> int:
        """获取虚拟键码"""
        if key not in self.VK_CODE_MAP:
            raise ValueError(f"不支持的键码: {key}")
        return self.VK_CODE_MAP[key]
    
    def press_key(self, key: KeyCode):
        """按下按键"""
        vk_code = self._get_vk_code(key)

        # 获取扫描码，特殊处理Shift键
        if key == KeyCode.SHIFT:
            scan_code = win32api.MapVirtualKey(win32con.VK_SHIFT, 0)
        else:
            scan_code = 0
            
        win32api.keybd_event(vk_code, scan_code, 0, 0)
        self._pressed_keys.add(key)

    def release_key(self, key: KeyCode):
        """释放按键"""
        vk_code = self._get_vk_code(key)
        
        if key == KeyCode.SHIFT:
            scan_code = win32api.MapVirtualKey(win32con.VK_SHIFT, 0)
        else:
            scan_code = 0
            
        win32api.keybd_event(vk_code, scan_code, win32con.KEYEVENTF_KEYUP, 0)
        self._pressed_keys.discard(key)
    
    def get_mouse_pos(self) -> Tuple[int, int]:
        """获取当前鼠标位置（屏幕坐标）"""
        return win32api.GetCursorPos()

    def move_mouse(self, x: int, y: int, absolute: bool = True):
        """
        移动鼠标到指定位置
        
        absolute=True: 绝对坐标（屏幕坐标）
        absolute=False: 相对当前位置移动
        """
        if absolute:
            win32api.SetCursorPos((int(x), int(y)))
        else:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(x), int(y), 0, 0)

    def press_mouse(self, button: MouseButton = MouseButton.LEFT):
        """按下鼠标按钮"""
        down_flag, _ = self.MOUSE_BUTTON_MAP[button]
        win32api.mouse_event(down_flag, 0, 0, 0, 0)

    def release_mouse(self, button: MouseButton = MouseButton.LEFT):
        """释放鼠标按钮"""
        _, up_flag = self.MOUSE_BUTTON_MAP[button]
        win32api.mouse_event(up_flag, 0, 0, 0, 0)

    def scroll_mouse(self, delta: int):
        """滚轮滚动，delta为正向上，为负向下"""
        # delta通常以WHEEL_DELTA(120)为单位
        win32api.mouse_event(
            win32con.MOUSEEVENTF_WHEEL, 
            0, 0, 
            int(delta * self.WHEEL_DELTA), 
            0
        )
    
    # ========== 额外实用方法 ==========

    def click_key(self, button: KeyCode, duration_ms: int = 50, random_jitter: float = 0.2):
        """点击键盘按钮"""
        self.press_key(button)
        time.sleep(self._get_duration(duration_ms, random_jitter))
        self.release_key(button)

    def click_key_combo(self, keys: List[KeyCode], duration_ms: int = 25, random_jitter: float = 0.2):
        """组合键（如Ctrl+C）"""
        if not keys:
            return
        
        # 依次按下所有键
        for key in keys:
            self.hold_key(key)
            time.sleep(self._get_duration(duration_ms, random_jitter))
        
        # 依次释放所有键（反向顺序）
        for key in reversed(keys):
            self.release_key(key)
            time.sleep(self._get_duration(duration_ms, random_jitter))
    
    def click_mouse(self, button: MouseButton = MouseButton.LEFT, 
              duration_ms: int = 50, random_jitter: float = 0.2):
        """点击鼠标"""
        self.press_mouse(button)
        time.sleep(self._get_duration(duration_ms, random_jitter))
        self.release_mouse(button)

    def click_mouse_double(self, button: MouseButton = MouseButton.LEFT, duration_ms: int = 50, random_jitter: float = 0.2, interval_ms: int = 200, interval_jitter: float = 0.1):
        """双击"""
        self.click_mouse(button, duration_ms, random_jitter)
        time.sleep(self._get_duration(interval_ms, interval_jitter))
        self.click_mouse(button, duration_ms, random_jitter)
    
    def move_mouse_smooth(self, target_x: int, target_y: int, duration: float = 0.2):
        """
        平滑移动到绝对坐标（带插值）
        
        这是move_mouse的增强版，提供平滑动画效果
        """
        current_x, current_y = self.get_mouse_pos()
        dx = target_x - current_x
        dy = target_y - current_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        
        # 距离很近时直接跳转
        if distance < 20:
            self.move_mouse(target_x, target_y, absolute=True)
            return
        
        steps = max(2, int(distance / 20))
        delay = duration / steps
        
        for i in range(1, steps + 1):
            progress = i / steps
            x = int(current_x + dx * progress)
            y = int(current_y + dy * progress)
            self.move_mouse(x, y, absolute=True)
            time.sleep(delay)
    
    def click_mouse_at(self, button: MouseButton = MouseButton.LEFT, x: int = 0, y: int = 0, duration_ms: int = 50, random_jitter: float = 0.2):
        """移动到指定位置并点击"""
        self.move_mouse(x, y, absolute=True)
        self.click_mouse(button, duration_ms, random_jitter)