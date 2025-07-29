# coding: utf-8
# Project：xbsTestTools
# File：test_tools.py
# Author：张炼武
# Date ：2025/6/9 11:04
# IDE：PyCharm
import subprocess
from time import sleep

from xbsTestTools.system_tools.buring.download_tool import download_file, get_link, get_link_file
from xbsTestTools.system_tools.buring.zr import zhanRui_flash_run


class TestTools:
    def __init__(self, dev):
        from xbsTestTools import XbsUiOperate
        from xbsTestTools import AdbTools

        self.ats = AdbTools(dev)
        self.xuo = XbsUiOperate(dev)

        self.dev = dev
        self.test1_ = ""
        self.test2_ = "com.emdoor.pressure.tester"

    def start_to_name(self, test_name, test_number: int = 0):
        """启动指定测试"""
        print(f"启动指定测试 {test_name} {test_number}")
        run2_type = self.xuo.app_start(self.test2_)
        if not run2_type:
            print("平板压力测试工具2 打开失败")
            return True

        self.xuo.click_roll(text=test_name)

        self.xuo.click(text="复位")

        if test_number != 0:
            self.xuo.click(text="设置次数")
            self.xuo.click(text=f"{test_number}")
            self.xuo.click(text="确定")

        self.xuo.click(text="开始")
        return True

    def start_onoff(self):
        """启动开关机"""
        print("启动开关机")
        run2_type = self.xuo.app_start(self.test2_)
        if not run2_type:
            print("平板压力测试工具2 打开失败")
            return True

        self.xuo.click_roll(text="开关机测试")

        self.xuo.click(text="复位")

        self.xuo.click(text="设置次数")
        self.xuo.click(text="1")
        self.xuo.click(text="确定")
        self.xuo.click(text="开始")

        sleep(80)
        if not self.ats.wait_dev():
            # 超时3分钟
            print("开关机失败，adb设备不在线")
            return False
        return True

    def start_restore(self):
        """启动恢复出厂设置"""
        print("启动恢复出厂设置")
        run2_type = self.xuo.app_start(self.test2_)
        if not run2_type:
            print("平板压力测试工具2 打开失败")
            return True

        self.xuo.click_roll(text="恢复出厂设置")

        self.xuo.click(text="复位")

        self.xuo.click(text="设置次数")

        self.xuo.click(text="1")

        self.xuo.click(text="确定")
        self.xuo.click(text="开始")

        sleep(10)

        if not self.ats.wait_dev(timeout=300):
            # 超时3分钟
            print("恢复出厂设置失败，adb设备不在线")
            return False
        return True

    def start_hibernate(self, time_: int = 5):
        """休眠唤醒"""
        print(f"休眠{time_}s")
        try:
            subprocess.run(f"adb -s {self.dev} shell input keyevent 26")
            sleep(time_)
            subprocess.run(f"adb -s {self.dev} shell input keyevent 266")
            sleep(1)
            return True
        except:
            return False

    def start_restart(self):
        """重启"""
        print("重启")
        subprocess.run(f"adb -s {self.dev} reboot")
        sleep(10)
        if not self.ats.wait_dev():
            print("执行重启后设备不在线")
            return False
        return True

    def start_brun(self, burn_file=""):
        """启动刷机"""
        if not burn_file:
            links = get_link()
            for k,v in links.items():
                print(f"【{k}】 {v}")

            file_index = str(input("请选择刷机哪个版本: \n"))
            burn_file = get_link_file(links[file_index])

        # 下载软件
        download_type = download_file(burn_file)
        if not download_type:
            print(f"{self.dev} 烧录文件下载失败，无法烧录")
            return False
        # 开始烧录
        run_type = zhanRui_flash_run(self.dev, download_type)
        if not run_type:
            download_type(f"{self.dev} 烧录失败")
        return True


if __name__ == "__main__":
    dev = "00test4H01881655D00189"
    tt = TestTools(dev)
    tt.start_onoff()

