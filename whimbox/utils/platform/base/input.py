from abc import ABC, abstractmethod
from typing import Tuple, Optional, List
from dataclasses import dataclass
from enum import Enum

class KeyCode(Enum):
    """虚拟键码，平台无关"""
    W = "w"
    A = "a"
    S = "s"
    D = "d"
    SPACE = "space"
    SHIFT = "shift"
    CTRL = "ctrl"
    F = "f"
    # ... 其他通用按键

class MouseButton(Enum):
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"

@dataclass
class InputConfig:
    """输入配置，平台无关"""
    move_duration_base_ms: float = 100.0
    random_jitter: float = 0.2
    use_hardware_events: bool = True  # 硬件级还是软件级
    require_admin: bool = False       # 是否需要管理员权限

class InputControllerBase(ABC):
    """
    输入控制器抽象基类
    
    所有平台实现必须遵循此接口
    业务逻辑只依赖此接口，不感知具体平台
    """
    
    def __init__(self, config: InputConfig):
        self.config = config
        self._initialized = False
    
    @abstractmethod
    def initialize(self) -> bool:
        """初始化平台特定资源"""
        pass
    
    @abstractmethod
    def cleanup(self):
        """清理资源"""
        pass
    
    @abstractmethod
    def press_key(self, key: KeyCode, duration_ms: Optional[float] = None):
        """按下并释放按键"""
        pass
    
    @abstractmethod
    def hold_key(self, key: KeyCode):
        """按住不放"""
        pass
    
    @abstractmethod
    def release_key(self, key: KeyCode):
        """释放按键"""
        pass
    
    @abstractmethod
    def press_combo(self, keys: List[KeyCode], duration_ms: Optional[float] = None):
        """组合键"""
        pass
    
    @abstractmethod
    def move_mouse(self, x: int, y: int, absolute: bool = True):
        """移动鼠标"""
        pass
    
    @abstractmethod
    def move_mouse_relative(self, dx: int, dy: int):
        """相对移动"""
        pass
    
    @abstractmethod
    def click(self, button: MouseButton = MouseButton.LEFT, 
              duration_ms: float = 50):
        """点击"""
        pass
    
    @abstractmethod
    def scroll(self, delta: int):
        """滚轮"""
        pass
    
    @abstractmethod
    def get_mouse_pos(self) -> Tuple[int, int]:
        """获取鼠标位置"""
        pass
    
    def __enter__(self):
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()