# coding: utf-8
# Project：xbsSysStabilityAT
# File：qz.py
# Author：张炼武
# Date ：2025/4/27 11:48
# IDE：PyCharm
import os
import queue
import subprocess
import threading
from time import sleep
from xbsTestTools.system_tools.buring.download_tool import get_download_file


def allwinner_flash(dev, softwarePath, burn_type):
    mirror_file = get_download_file("allwinner", softwarePath)
    scatterFile = os.path.join(softwarePath, mirror_file)
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
    tool_path = root_path + r"utils\PhoenixConsole_V2.0.8\PhoenixConsole.exe"
    download_cmd = f"{tool_path} -e 11 -r -s {dev} -o 1 -p {scatterFile}"
    print(f"{dev} 执行烧录  烧录命令：{download_cmd}")
    download_info = subprocess.run(download_cmd, stdout=subprocess.PIPE)
    if "result=Success" in str(download_info.stdout):  # 全志下载信息
        print(f"{dev} download log info result=Success")
        burn_type.put(True)
        return True
    else:
        print(f"{dev} 烧写失败，没找到烧录成功关键词")
        burn_type.put(False)
        return False


def all_burn_run(dev, softwarePath):
    _type = queue.Queue()
    # 烧录启动
    t = threading.Thread(target=allwinner_flash, args=(dev, softwarePath, _type))
    t.start()
    sleep(5)
    t.join(600)
    print(f"{dev} 烧录完成")
    return _type.get()
