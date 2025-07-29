# coding: utf-8
# Project：xbsSysStabilityAT
# File：zr.py
# Author：张炼武
# Date ：2025/4/27 11:48
# IDE：PyCharm
import os
import queue
import subprocess
import threading
from time import sleep
import serial.tools.list_ports
from xbsTestTools.system_tools.buring.download_tool import get_download_file


def zhanRui_flash(dev, com, softwarePath, burn_type):
    mirror_file = get_download_file("UNISOC", softwarePath)
    softwarePath = os.path.join(softwarePath, mirror_file)  # 拼接烧录镜像路径
    flash_cmd = 'CmdDloader.exe -pac {} -reset -port {}'.format(softwarePath, com)
    try:
        print(f"{dev} 执行展瑞烧录命令: {flash_cmd}")
        flash_result = subprocess.run(flash_cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8",
                                      timeout=400).stdout

        if 'Download Result = Passed' in flash_result:
            print(f"{dev} 刷机成功")
            burn_type.put(True)
            return True
        else:
            print(f"{dev} 刷机失败，刷机完成中没有 成功字段")
            burn_type.put(False)
            return
    except Exception as e:
        print(f"{dev} 烧写版本超时 ERROR_INFO: {e}")
        burn_type.put(False)
        return


def zhanRui_flash_run(dev, softwarePath):
    burn_type = queue.Queue()  # 定义状态变量
    patList = os.environ.get('Path')  # 获取当前系统环境变量list
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
    CmdDloader = root_path + r"utils\ZhanRui_Flash_Tool\Download_R27.22.4204\Download_R27.22.4204\Bin"  # 定义展锐烧录器path
    if CmdDloader not in patList:
        os.environ['Path'] = os.pathsep.join([CmdDloader, patList])
    # 获取设备串口号
    read = os.popen(f"adb -s {dev} shell getprop persist.sys.seewo.is_adb_on").read()  # 检查设备默认adb是否开启
    if "true" not in read:
        # 默认开启设备adb
        print("检查给设备设置默认开启adb")
        os.system(f"adb -s {dev} shell am broadcast -a com.seewo.action.SWITCH_ADB --ez open_usb true com.cvte.logtool")
    sleep(1)
    print(f"{dev} 设备进入烧录模式 adb reboot autodloader")
    subprocess.run(f"adb -s {dev} reboot autodloader")  # 设备进入烧录模式
    print(f"{dev} 正在获取设备串口COM")
    sleep(15)
    ports = []
    for port in serial.tools.list_ports.comports():
        if "SPRD U2S" in port.description:
            ports.append(port.name)

    if len(ports) < 1:
        return False

    t = threading.Thread(target=zhanRui_flash, args=(dev, ports[0], softwarePath, burn_type))  # 创建刷机线程
    t.start()  # 启动刷机线程
    print(f"{dev} {ports[0]} 正在烧录中...")
    t.join()

    print(f"{dev} 正在重启")
    sleep(10)
    return burn_type.get()
