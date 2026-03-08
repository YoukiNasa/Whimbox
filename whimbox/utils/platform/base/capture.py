import numpy as np
from abc import ABC, abstractmethod
from typing import Tuple, Optional, List
from dataclasses import dataclass

class CaptureServiceBase(ABC):
    """
    捕获服务抽象基类
    """
    
    def __init__(self):
        self._initialized = False
    
    @abstractmethod
    def initialize(self, game_config: dict) -> bool:
        """初始化捕获资源"""
        pass
    
    @abstractmethod
    def capture_frame(self) -> Optional[np.ndarray]:
        """捕获一帧图像并返回为numpy数组"""
        pass
    
    @abstractmethod
    def cleanup(self):
        """清理资源"""
        pass