from abc import ABC, abstractmethod
from typing import Tuple, Optional, List
from dataclasses import dataclass
from enum import Enum
from random import random

class KeyCode(Enum):
    """虚拟键码，平台无关"""
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"
    H = "h"
    I = "i"
    J = "j"
    K = "k"
    L = "l"
    M = "m"
    N = "n"
    O = "o"
    P = "p"
    Q = "q"
    R = "r"
    S = "s"
    T = "t"
    U = "u"
    V = "v"
    W = "w"
    X = "x"
    Y = "y"
    Z = "z"
    ESCAPE = "escape"
    TAB = "tab"
    SHIFT = "shift"
    CTRL = "ctrl"
    ALT = "alt"
    SPACE = "space"
    BACKSPACE = "backspace"
    ENTER = "enter"
    F1 = "f1"
    F2 = "f2"
    F3 = "f3"
    F4 = "f4"
    F5 = "f5"
    F6 = "f6"
    F7 = "f7"
    F8 = "f8"
    F9 = "f9"

class MouseButton(Enum):
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"

@dataclass
class InputConfig:
    """输入配置，平台特定"""
    use_hardware_events: bool = True  # 硬件级还是软件级
    require_admin: bool = False       # 是否需要管理员权限
    wheel_scroll_amount: int = 120     # 滚轮增量，通常为120

class InputServiceBase(ABC):
    """
    输入服务抽象基类
    """
    
    def __init__(self):
        self._initialized = False
    
    @abstractmethod
    def initialize(self) -> bool:
        """初始化平台特定资源"""
        pass
    
    @abstractmethod
    def cleanup(self):
        """清理资源"""
        pass

    def _get_duration(self, base_duration: float, random_jitter: Optional[float]) -> float:
        """计算实际持续时间（带抖动）"""
        if random_jitter is None:
            return base_duration / 1000.0
        
        jitter = random.uniform(-random_jitter, random_jitter)
        return base_duration * (1 + jitter)
    
    @abstractmethod
    def press_key(self, key: KeyCode):
        """按下按键"""
        pass
    
    @abstractmethod
    def release_key(self, key: KeyCode):
        """释放按键"""
        pass
    
    @abstractmethod
    def get_mouse_pos(self) -> Tuple[int, int]:
        """获取鼠标位置"""
        pass

    @abstractmethod
    def move_mouse(self, x: int, y: int, absolute: bool = True):
        """移动鼠标"""
        pass
    
    @abstractmethod
    def press_mouse(self, button: MouseButton = MouseButton.LEFT):
        """按下鼠标按钮"""
        pass
    
    def release_mouse(self, button: MouseButton = MouseButton.LEFT):
        """释放鼠标按钮"""
        pass

    @abstractmethod
    def scroll_mouse(self, delta: int):
        """滚轮"""
        pass
    
    def __enter__(self):
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()