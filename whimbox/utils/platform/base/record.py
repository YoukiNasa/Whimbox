from abc import ABC, abstractmethod
from typing import Tuple, Optional, List
from dataclasses import dataclass

class RecordService(ABC):
    """输入记录服务，平台特定"""
    @abstractmethod
    def start(self):
        """开始录制"""
        pass
    
    @abstractmethod
    def stop(self):
        """停止录制"""
        pass
    
    @abstractmethod
    def get_events(self) -> List[Tuple[str, dict]]:
        """获取录制的事件列表，每个事件是一个 (event_type, event_data) 的元组"""
        pass