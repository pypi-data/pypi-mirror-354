# coding: utf-8
# Project：xbsSysStabilityAT
# File：mtk.py
# Author：张炼武
# Date ：2025/4/27 11:48
# IDE：PyCharm
import os
import queue
import threading
from time import sleep
from xbsTestTools.system_tools.buring.download_tool import get_download_file, cmd_to_file, query_update_folder, getMtkLog_keywords


def mtk_flash(dev, softwarePath, burn_type):
    """
    烧录方法
    dev 设备device
    message 烧录消息
    _type 烧录状态
    softwarePath 烧录软件地址
    """
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
    flashTool = rf"{root_path}utils\SP_Flash_Tool\flash_tool.exe"
    daFile = rf"{root_path}utils\SP_Flash_Tool\MTK_ALLInOne_DA.bin"
    # 软件Path
    mirror_file = get_download_file("MTK", softwarePath)
    scatterFile = os.path.join(softwarePath, mirror_file)
    flashCmd = flashTool + ' -c firmware-upgrade -b -d {} -s {}'.format(daFile, scatterFile)
    print(f"{dev} 执行MTK烧录命令: {flashCmd}")
    # 执行cmd命令并输出txt
    cmdType, value = cmd_to_file(flashCmd, "flashRead.txt", 400)
    if not cmdType:
        print(f"{dev} 烧写版本超时")
        burn_type.put(False)
        return

    print("解析MTK烧录Log")
    # 获取MTK最新日志
    newTimeFolder = query_update_folder(r'C:\ProgramData\SP_FT_Logs')

    if newTimeFolder is None:
        print(f"{dev} 未能获取到MTK烧录器中最新的日志文件")
    else:
        # 检查是否烧录成功
        if not getMtkLog_keywords(newTimeFolder):
            print(f"{dev} 烧写失败，没找到烧录成功关键词")
            burn_type.put(False)
            return

    print(f"{dev} 烧写成功%s")
    burn_type.put(True)


def mtk_burn_run(dev, softwarePath):
    print(f"{dev} 开始烧录")
    burn_type = queue.Queue()
    # 烧录启动
    t = threading.Thread(target=mtk_flash, args=(dev, burn_type, softwarePath))
    t.start()
    sleep(10)
    print(f"{dev} 进入下载模式")
    os.system(f'adb -s {dev} reboot')
    print(f"{dev} 版本烧录中")

    t.join()
    print(f"{dev} 烧录进程结束")
    sleep(20)
    return burn_type.get()
