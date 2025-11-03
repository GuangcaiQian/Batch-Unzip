#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化构建脚本：运行一次生成可分发的解压助手 EXE。

依赖项：
    pip install PySide6 pyinstaller
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_NAME = "extract_zips_gui.py"
APP_NAME = "解压助手"


def ensure_dependencies():
    try:
        import PySide6  # noqa: F401
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "缺少 PySide6，请先运行: pip install PySide6 pyinstaller"
        ) from exc

    if shutil.which("pyinstaller") is None:  # pragma: no cover
        raise SystemExit("未找到 pyinstaller 命令，请先安装: pip install pyinstaller")


def run_pyinstaller():
    root = Path(__file__).resolve().parent
    script_path = root / SCRIPT_NAME
    if not script_path.exists():
        raise SystemExit(f"找不到脚本：{script_path}")

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconsole",
        "--clean",
        f"--name={APP_NAME}",
        str(script_path),
    ]
    print("运行命令:", " ".join(command))
    subprocess.check_call(command, cwd=root)


def post_process():
    dist_dir = Path("dist") / APP_NAME
    if not dist_dir.exists():
        raise SystemExit("打包失败，未找到 dist 目录。")

    exe_path = dist_dir / f"{APP_NAME}.exe"
    if not exe_path.exists():
        raise SystemExit("打包失败，未生成 EXE 文件。")

    print(f"打包成功：{exe_path.resolve()}")
    print("可将此目录打包或压缩后分享给同事直接使用。")


def main():
    ensure_dependencies()
    run_pyinstaller()
    post_process()


if __name__ == "__main__":
    main()
