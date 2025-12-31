import time
from datetime import datetime
from typing import Optional
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from .status_bar import AIStatusBar

class ChatMessage:
    """聊天消息类，管理不同类型的消息"""
    def __init__(self, content: str, message_type: str, timestamp: Optional[float] = None):
        self.content = content
        self.message_type = message_type  # 'user', 'ai', 'log'
        self.timestamp = timestamp or time.time()
        self.avatar = self._get_avatar()
        self.color = self._get_color()
        self.is_processing = False  # 是否正在处理中
    
    def _get_avatar(self) -> str:
        """获取消息类型对应的头像"""
        avatars = {
            'user': '😊',
            'ai': '📦', 
            'log': '📝',
            'error': '❌',
            'success': '✅'
        }
        return avatars.get(self.message_type, '💬')
    
    def _get_color(self) -> str:
        """获取消息类型对应的颜色"""
        colors = {
            'user': '#2196F3',      # 更亮的蓝色
            'ai': '#424242',        # 深灰色（浅色主题下）
            'log': '#FF9800',       # 橙色
            'error': '#F44336',     # 红色
            'success': '#4CAF50'    # 绿色
        }
        return colors.get(self.message_type, '#333333')
    
    def get_formatted_time(self) -> str:
        """获取格式化的时间字符串"""
        return datetime.fromtimestamp(self.timestamp).strftime('%H:%M:%S')

class ChatMessageWidget(QWidget):
    """单个聊天消息的UI组件"""
    def __init__(self, message: ChatMessage, parent=None):
        super().__init__(parent)
        self.message = message
        self.status_bar = None  # AI消息的状态栏
        self.init_ui()
    
    def init_ui(self):
        # 消息内容布局
        message_layout = QHBoxLayout(self)
        message_layout.setContentsMargins(4, 2, 4, 2)
        message_layout.setSpacing(4)
        
        # 头像
        avatar_label = QLabel(self.message.avatar)
        avatar_label.setFixedSize(20, 20)
        avatar_label.setAlignment(Qt.AlignCenter)
        
        # 浅色主题的头像样式
        if self.message.message_type == 'user':
            avatar_bg = "#E3F2FD"  # 浅蓝色背景
        elif self.message.message_type == 'ai':
            avatar_bg = "#F5F5F5"  # 浅灰色背景
        elif self.message.message_type == 'error':
            avatar_bg = "#FFEBEE"  # 浅红色背景
        elif self.message.message_type == 'success':
            avatar_bg = "#E8F5E8"  # 浅绿色背景
        else:
            avatar_bg = "#FFF3E0"  # 浅橙色背景（日志）
            
        avatar_label.setStyleSheet(f"""
            QLabel {{
                background-color: {avatar_bg};
                border-radius: 10px;
                font-size: 8pt;
                border: 1px solid #E0E0E0;
            }}
        """)
        
        # 消息内容
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(0)
        
        # 消息类型和时间
        header_label = QLabel(f"{self.message.get_formatted_time()}")
        header_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: #757575; 
                font-size: 5pt; 
                border: none;
            }
        """)
        
        # 消息文本背景色
        if self.message.message_type == 'user':
            msg_bg = "#E3F2FD"      # 用户消息：浅蓝色
            text_color = "#1565C0"  # 深蓝色文字
        elif self.message.message_type == 'ai':
            msg_bg = "#F8F9FA"      # AI消息：浅灰色
            text_color = "#424242"  # 深灰色文字
        elif self.message.message_type == 'error':
            msg_bg = "#FFEBEE"      # 错误消息：浅红色
            text_color = "#C62828"  # 深红色文字
        elif self.message.message_type == 'success':
            msg_bg = "#E8F5E8"      # 成功消息：浅绿色
            text_color = "#2E7D32"  # 深绿色文字
        else:
            msg_bg = "#FFF8E1"      # 日志消息：浅黄色
            text_color = "#F57C00"  # 橙色文字
        
        # 消息文本
        self.content_label = QLabel(self.message.content)
        self.content_label.setWordWrap(True)
        self.content_label.setStyleSheet(f"""
            QLabel {{
                color: {text_color};
                font-size: 8pt;
                padding: 4px 4px;
                background-color: {msg_bg};
                border-radius: 6px;
                border: 1px solid #E0E0E0;
            }}
        """)
        
        if self.message.message_type == 'user':
            self.content_layout.addWidget(header_label, alignment=Qt.AlignRight)
        else:
            self.content_layout.addWidget(header_label, alignment=Qt.AlignLeft)
        self.content_layout.addWidget(self.content_label)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建内容容器
        content_widget = QWidget()
        content_widget.setLayout(self.content_layout)
        content_widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
        """) 
        
        # 消息内容布局
        if self.message.message_type == 'user':
            message_layout.addStretch()
            message_layout.addWidget(content_widget)
            message_layout.addWidget(avatar_label, alignment=Qt.AlignTop)
        else:
            message_layout.addWidget(avatar_label, alignment=Qt.AlignTop)
            message_layout.addWidget(content_widget)
            message_layout.addStretch()
        
        # 如果是AI消息且正在处理，显示状态栏
        if self.message.message_type == 'ai' and self.message.is_processing:
            self.show_status_bar()
    
    def show_status_bar(self):
        """显示状态栏"""
        if not self.status_bar and self.message.message_type == 'ai':
            self.status_bar = AIStatusBar(self)
            self.content_layout.addWidget(self.status_bar)
    
    def hide_status_bar(self):
        """隐藏状态栏"""
        if self.status_bar:
            self.status_bar.deleteLater()
            self.status_bar = None
    
    def update_status(self, status_type: str, message: str = ""):
        """更新状态栏"""
        if self.status_bar:
            self.status_bar.set_status(status_type, message)
    
    def update_content(self, content: str):
        """更新消息内容"""
        self.message.content = content
        self.content_label.setText(content)
    
    def set_processing(self, is_processing: bool):
        """设置处理状态"""
        self.message.is_processing = is_processing
        if is_processing and self.message.message_type == 'ai':
            self.show_status_bar()
        elif not is_processing:
            if self.status_bar:
                self.status_bar.set_status('completed')