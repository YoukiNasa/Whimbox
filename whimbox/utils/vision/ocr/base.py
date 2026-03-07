# utils/ocr/base.py
from abc import ABC, abstractmethod
import numpy as np
from typing import List, Tuple

class OCREngine(ABC):
    """OCR引擎抽象基类，所有OCR实现需继承此类"""
    
    @abstractmethod
    def __init__(self, config: dict):
        """初始化OCR引擎，接收引擎专属配置"""
        pass
    
    @abstractmethod
    def recognize(self, image: np.ndarray) -> Tuple[str, Tuple]:
        """
        对图像执行OCR识别
        :param image: RGB格式的numpy数组图像
        :return: 识别结果列表，每个元素为(文本内容, 坐标框(x1,y1,x2,y2))
        """
        pass
    
    @abstractmethod
    def destroy(self):
        """资源释放（如模型卸载、句柄关闭等）"""
        pass