### 项目结构
```
Whimbox/
├── whimbox/                        
│   ├── assets/                   # 资源文件（UI 截图、图标、素材）
│   ├── core/                     # 核心引擎模块（状态管理、导航、游戏逻辑）
│   │   ├── state/                # 状态机（技能状态、场景状态等）
│   │   ├── perception/           # 游戏交互（UI 导航、坐标追踪、地图匹配）
│   │   ├── navigation/           # 导航系统
|   |   └── engine.py             # 
│   ├── utils/                    # 工具模块
│   │   ├── platform/             # 平台适配（截图、输入、录制等）
│   │   ├── vision/               # 视觉识别（OCR、模板匹配）
│   │   └── logger.py             # 日志系统
│   ├── config/                   # 配置模块（动作、游戏、地图、OCR 等 JSON 配置）
│   └── main.py                   # 程序入口
├── docs/                         # 文档目录
├── requirements.txt              # Python 依赖
├── LICENSE                       # 开源协议
├── README.md                     # 项目说明
```

## 加入开发
项目还有大量功能需要开发和适配。如果你对此感兴趣，欢迎加入一起研究。开发Q群：821908945。