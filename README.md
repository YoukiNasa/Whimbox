<p align="center">
  <img src="docs/logo.png" height=120>
</p>

# Whimbox
Whimbox is an AI agent based on large language models and image recognition technology that assists in playing Infinite Nikki!

<div align="center">

[Whimbox Home Page](https://nikkigallery.vip/whimbox/)

</div>

## 🛠️ Dependencies and Installation Process

1. Create and activate a conda environment (e.g., `conda create -n whimbox python=3.12`).

2. Enter the project root directory and install dependencies:
   ```bash
   conda activate whimbox
   pip install -r requirements.txt
   ```

3. Run the program using Python:
   ```bash
   python -m ./whimbox/main.py
   ```

After successful startup, you'll see:

```
whimbox is running on {IP}:{PORT}
```

## 🛠️ Features

* Daily tasks (such as Miko pear digging, Illusionary Realm challenges, Morning and Evening Wishes, monthly card collection, Crown of Miracles, etc.)
* Automated dialogue, collection, bug catching, cleaning, fishing, etc.
* Supports recording and automated execution of route paths for running around the map
* Can convert MIDI music scores to game scripts for automated piano playing

## 🚀 Future Plans

1. A complete home garden workflow: star planting, catching stars, liking photos
2. Remote control via mobile phone
3. Large model capability expansion: photo rating, outfit analysis, cover image recommendations, and more

## ⚠️ Important Notes

* Whimbox will not modify game files or read/write game memory; it only takes screenshots and simulates mouse and keyboard input. Theoretically, it won't result in a ban. However, the game's terms of service are comprehensive and cover all possible scenarios. Any consequences resulting from using Whimbox should be borne by you.
* Since the game itself already consumes significant PC performance, image recognition will additionally consume resources. Therefore, currently only mid-to-high-end PCs are supported. A cloud gaming version will be developed once features are fully matured.

## 💡 Acknowledgments

Thank you to the pioneers of various open-source big-world games who have provided Whimbox with learning and reference materials:

- [Genshin Impact Assistant · GIA](https://github.com/infstellar/genshin_impact_assistant)
- [Better Genshin Impact · BetterGI](https://github.com/babalae/better-genshin-impact)

Thank you to various AI models and AI programming tools including ChatGPT, Cursor, Claude, Codex, etc.