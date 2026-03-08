import json
import threading
import time
from pynput import mouse, keyboard
from collections import deque

class RecordService:
    def __init__(self, max_buffer_size=65536):
        self.events = deque(maxlen=max_buffer_size)
        self.recording = False
        self.mouse_listener = None
        self.keyboard_listener = None
        self.lock = threading.Lock()
        self.thread = None
        
    def _on_mouse_move(self, x, y):
        """鼠标移动事件"""
        with self.lock:
            self.events.append({
                "type": "mouse_move",
                "x": x,
                "y": y,
                "timestamp": time.time(),
            })
    
    def _on_mouse_click(self, x, y, button, pressed):
        """鼠标点击事件"""
        action = "pressed" if pressed else "released"
        with self.lock:
            self.events.append({
                "type": "mouse_click",
                "action": action,
                "button": str(button),
                "x": x,
                "y": y,
                "timestamp": time.time()
            })
        print(f"鼠标 {button} {action} at ({x}, {y})")
    
    def _on_mouse_scroll(self, x, y, dx, dy):
        """鼠标滚轮事件"""
        with self.lock:
            self.events.append({
                "type": "mouse_scroll",
                "x": x,
                "y": y,
                "dx": dx,
                "dy": dy,
                "timestamp": time.time()
            })
        direction = "向上" if dy > 0 else "向下"
        print(f"鼠标滚轮 {direction} at ({x}, {y})")
    
    def _on_key_press(self, key):
        """键盘按下事件"""
        try:
            key_str = key.char  # 普通字符键
        except AttributeError:
            key_str = str(key)  # 特殊键如 Key.shift
        
        with self.lock:
            self.events.append({
                "type": "key_press",
                "key": key_str,
                "timestamp": time.time()
            })
        print(f"按键按下: {key_str}")
    
    def _on_key_release(self, key):
        """键盘释放事件"""
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)
        
        with self.lock:
            self.events.append({
                "type": "key_release",
                "key": key_str,
                "timestamp": time.time()
            })
        
        # 按 Esc 键停止录制
        if key == keyboard.Key.esc:
            print("检测到 Esc 键，停止录制...")
            self.stop()
            return False  # 停止监听器
    
    def _run_listeners(self):
        """在线程中运行监听器"""
        self.mouse_listener = mouse.Listener(
            on_click=self._on_mouse_click,
            on_scroll=self._on_mouse_scroll
            # 如需记录移动，取消下面注释（会产生大量数据）
            # on_move=self._on_mouse_move
        )
        
        # 创建键盘监听器
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        
        # 启动监听器
        self.mouse_listener.start()
        self.keyboard_listener.start()
        
        # 等待监听器结束
        self.mouse_listener.join()
        self.keyboard_listener.join()
    
    def start(self):
        """启动录制（在新线程中）"""
        if self.recording:
            print("已经在录制中...")
            return
        
        self.recording = True
        self.thread = threading.Thread(target=self._run_listeners, daemon=True)
        self.thread.start()
        print("=" * 50)
        print("开始录制鼠标和键盘操作...")
        print("按 Esc 键停止录制")
        print("=" * 50)
    
    def stop(self):
        """停止录制"""
        if not self.recording:
            return
        
        self.recording = False
        
        # 停止监听器
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        
        print("录制已停止")
    
    def save_to_json(self, filename="input_record.json"):
        """保存记录到 JSON 文件"""
        with self.lock:
            events_list = list(self.events)
        
        data = {
            "metadata": {
                "total_events": len(events_list),
                "duration_seconds": (
                    events_list[-1]["timestamp"] - events_list[0]["timestamp"]
                    if len(events_list) > 1 else 0
                )
            },
            "events": events_list
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"已保存 {len(events_list)} 条记录到 {filename}")
        return filename