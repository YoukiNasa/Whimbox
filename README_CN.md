<p align="center">
  <img src="docs/logo.png" height=120>
</p>

# 奇想盒（Whimbox）

奇想盒（Whimbox）是一个基于大语言模型和图像识别技术的 AI 智能体，辅助游玩无限暖暖！

<div align="center">

[奇想盒主页](https://nikkigallery.vip/whimbox/)

</div>

## 🛠️ 依赖和安装流程

1. 创建并激活一个 conda 环境（例如 `conda create -n whimbox python=3.12`）。

2. 进入项目根目录并安装依赖：
   ```bash
   conda activate whimbox
   pip install -r requirements.txt
   ```

3. 使用 Python 运行程序：
   ```bash
   python -m ./whimbox/main.py
   ```

成功运行后，你会看到

```
whimbox is running on {IP}:{PORT}
```

## 🛠 功能介绍

* 日常任务（比如美鸭梨挖掘、幻境挑战、朝夕心愿、领取月卡、奇迹之冠等）
* 自动对话、采集、捕虫、清洁、钓鱼等
* 支持跑图路线的录制与自动执行，
* 可将 MIDI 乐谱可转为游戏脚本实现自动弹琴

## 🚀 未来计划

1. 简单的家园一条龙：星实、钓星、点赞
2. 手机端远程控制
3. 大模型能力扩展：照片评分、穿搭分析、封面推荐等等

## ⚠️ 注意事项

* Whimbox 不会修改游戏文件、读写游戏内存，只会截图和模拟鼠标键盘，理论上不会被封号。但游戏的用户条款非常完善，涵盖了所有可能出现的情况。所以使用 Whimbox 导致的一切后果请自行承担。
* 由于游戏本身已经消耗 PC 的大量性能，图像识别还会额外消耗性能，所以目前仅支持中高配 PC 运行，功能完善后会开发云游戏版本。

## 💡 致谢

感谢各个大世界游戏开源项目的先行者，供 Whimbox 学习参考。

- [原神小助手·GIA](https://github.com/infstellar/genshin_impact_assistant)
- [更好的原神·BetterGI](https://github.com/babalae/better-genshin-impact)

感谢chatgpt、cursor、claude、codex等各种AI模型和AI编程工具