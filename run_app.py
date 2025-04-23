#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 01:33:11 2025

@author: anthony
"""
# run_app.py   ← 位于项目根
import sys, os, threading, webbrowser, time
from pathlib import Path
from streamlit.web import cli as stcli

BASE = Path(__file__).resolve().parent      # 项目根

# ──①── PyInstaller 解包目录 or 源码目录
bundle_dir = Path(getattr(sys, "_MEIPASS", BASE))

# ──②── 把 streamlit 的 static 目录路径写进环境变量
static_dir = (bundle_dir / "streamlit" / "static")
if static_dir.exists():
    os.environ["STREAMLIT_STATIC_PATH"] = str(static_dir)

# ──③── 让 Python 找到你的 src 代码
os.environ.setdefault("PYTHONPATH", str(bundle_dir / "src"))

# ──④── 用绝对文件路径启动 app.py
app_file = bundle_dir / "src" / "analysis" / "app.py"
sys.argv = ["streamlit", "run", str(app_file), "--server.port", "8501"]

# ──⑤── 打开浏览器一次
threading.Timer(2, lambda: webbrowser.open("http://localhost:8501")).start()

# ──⑥── 启动 Streamlit（阻塞）
stcli.main()