# coding: utf-8
# Project：xbsSysStabilityAT
# File：download_tool.py
# Author：张炼武
# Date ：2025/4/27 12:01
# IDE：PyCharm
import os
import shutil
import subprocess
from time import sleep
import patoolib
import requests
import time
import datetime

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep


def get_link():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'host': 'setup.gz.cvte.cn',
    }
    url = "https://setup.gz.cvte.cn/CrOS_new/xbs_os2/Seewo_XPG13/Image/XPG13/release/"  # XPG13
    response = requests.get(url, headers=headers)
    text_list = str(response.text).split("\n")

    link_list = {}
    index = 0
    for text in text_list:
        if 'href="seewoOS' in text and "V9.9.9" not in text:
            index += 1
            text = text[text.find('<a href="') + 9:text.find('/">')]
            link_list.update({str(index): url + "/" + text})
    return link_list


def get_link_file(link):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'host': 'setup.gz.cvte.cn',
    }
    url = link
    response = requests.get(url, headers=headers)
    text_list = str(response.text).split("\n")

    file_link = ""
    for text in text_list:
        if 'href="seewoOS' in text:
            text = text[text.find('<a href="') + 9:text.find('">')]
            file_link = text
            break
    return url + "/" + file_link


def get_file_size(url):
    response = requests.head(url)
    file_size = int(response.headers.get('content-length', 0))
    return file_size


def get_directories(path):
    """
    获取指定目录下的文件夹
    """
    return [entry.name for entry in os.scandir(path) if entry.is_dir()]


def query_update_folder(folder_path):
    """
    获取路径下最后修改时间的文件夹
    return 文件夹
    """
    # 初始化最后修改时间和对应的文件名
    last_modified_time = 0
    last_modified_file = None

    # 遍历文件夹中的文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # 确定为文件夹
        if os.path.isdir(file_path):
            mod_time = os.path.getmtime(file_path)

            # 比较时间戳，更新最后修改的文件信息
            if mod_time > last_modified_time:
                last_modified_time = mod_time
                last_modified_file = filename
    return last_modified_file


def getMtkLog_keywords(path):
    """
    获取mtk烧录完成后日志中打印刷机完成的信息
    """
    # SP_FT_Dump_03-21-2024-17-20-39
    with open(r'C:\ProgramData\SP_FT_Logs\%s\QT_FLASH_TOOL.log' % path) as f:
        # 使用生成器表达式和next()来找出第一个包含"a"的元素
        read = next((s for s in f.readlines()[-15:] if "FlashTool_EnableWatchDogTimeout Succeeded" in s), None)
        if read is None:
            return
        return True


def cmd_to_file(cmd, file, timeout):
    """
    执行cmd命令，重定向内容到指定文件
    cmd：执行的cmd
    file: 文件
    return: 目标文件
    """
    with open(root_path + "data\\" + file, 'w', encoding='utf-8') as fe:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            output, unused_err = process.communicate(timeout=timeout)
            fe.write(output.decode())
        except Exception as e:
            fe.write(str(e))
            print(e)
            return False, str(e)
    return True, root_path + "data\\" + file


def get_download_file(platform, file_path):
    """platform :平台类型
       file_path：版本路径
       返回烧录镜像文件"""
    filenames = os.listdir(file_path)
    for filename in filenames:
        if platform == "MTK":
            if "Android_scatter.txt" in filename:
                return filename
        elif platform == "UNISOC":
            if ".pac" in filename:
                return filename
        elif platform == "allwinner":
            if "img" in filename:
                return filename
    print("烧录镜像文件选择异常")


def delete_files_older_than_3days(folder_path):
    # 计算3天前的时间戳
    try:
        current_time = datetime.datetime.now()
        offset = datetime.timedelta(days=-3)
        three_days_ago = (current_time + offset)
        three_days_ago_timestamp = time.mktime(three_days_ago.timetuple())

        # 遍历文件夹
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # 获取文件最后修改时间
                file_mtime = os.path.getmtime(file_path)

                # 检查时间并删除
                if file_mtime < three_days_ago_timestamp:
                    try:
                        os.remove(file_path)
                        print(f"已删除: {file_path} (修改时间: {time.ctime(file_mtime)})")
                    except Exception as e:
                        print(f"删除失败 {file_path}: {str(e)}")
    except:
        ...


def download_file(link, jointly_model=None, sale_model=None):
    """
    下载软件方法
    downloadLink 软件链接
    """
    patList = os.environ.get('Path')
    wgetPath = root_path + "utils\\wget"
    if wgetPath not in patList:
        print("正在将wget加入系统环境变量中...")
        os.environ['Path'] = os.pathsep.join([wgetPath, patList])

    fileName = root_path + "data\\" + link.split('/')[-1]  # 软件文件名称
    delete_files_older_than_3days(f"{root_path}data")  # 删除3天前的旧文件
    # 软件文件名称去除.7z
    if ".7z" in fileName:
        softwarePath = fileName.split('.7z')[0]
    elif ".zip" in fileName:
        softwarePath = fileName.split('.zip')[0]
    else:
        softwarePath = fileName

    # 判断刷机文件是否下载
    if not os.path.exists(fileName):
        if ".7z" not in fileName and ".zip" not in fileName:
            print("请检查当前选择的链接是否正常，需要一个可用文件目标地址！！")
            return False, "下载软件失败"

        download = 'wget {} -P {} --no-check-certificate'.format(link, root_path + "data")

        print("软件未下载，开始下载...")
        try:
            subprocess.run(download, shell=True)
        except:
            print("下载失败, 删除残留文件重新下载...")
            os.remove(fileName)

            # 重试重新下载
            try:
                subprocess.run(download, shell=True)
            except:
                print("下载失败, 删除残留文件重新下载...")
                os.remove(fileName)
                return False

        download_file_size = get_file_size(link)  # 下载完成后检查文件大小
        local_file_size = os.path.getsize(fileName)

        if download_file_size != local_file_size:
            print(f"download_file_size: {download_file_size}     local_file_size: {local_file_size}")
            print("下载后的文件大小与实际的不相等")

            print("删除不完整文件")
            os.remove(fileName)
            # 重试重新下载  (暂时没添加)
            return False

    print("正在解压文件....")
    file_name = softwarePath.split('\\')[-1]
    if os.path.exists(f"{root_path}data\\{file_name}"):
        shutil.rmtree(f"{root_path}data\\{file_name}")
        sleep(2)
    try:
        patoolib.extract_archive(fileName, outdir=f"{root_path}data\\{file_name}")
        if len(get_directories(softwarePath)) == 1:
            softwarePath = softwarePath + "\\" + get_directories(softwarePath)[0]
    except Exception as e:
        print("解压失败")
        print(e)
        return False

    # 复制出默认items.ini
    if os.path.exists(f'{softwarePath}\\items.ini'):
        print("正在修改items")
        if not os.path.exists(f"{root_path}data\\items"):
            # 创建文件夹
            os.mkdir(f"{root_path}data\\items")
        file_name = softwarePath.split("\\")[-1]
        shutil.copy(f'{softwarePath}\\items.ini', f"{root_path}data\\items\\{file_name}_items.ini")

        modify_type = modify_items(softwarePath, jointly_model=jointly_model, sale_model=sale_model)
        if not modify_type:
            print("items修改失败")

    if os.path.exists(softwarePath + '\\Checksum.ini'):
        print("正在删除Checksum.ini文件....")
        os.remove(softwarePath + '\\Checksum.ini')
    return softwarePath


def modify_items(file_path, jointly_model, sale_model):
    """修改items"""
    update_path = None
    update_model = get_directories(rf"{root_path}data\update_items")
    for model in update_model:
        if model in file_path:
            update_path = rf"{root_path}data\update_items\{model}\items.ini"
            print(f"需要修改items文件路径：{update_path}")

    if not update_path:
        print("备份items 不存在")
        return False

    print("items 加密机型执行复制替换")
    file_path = file_path + r'\items.ini'
    shutil.copy2(file_path, update_path)

    file_items_path = file_path + '\\items.ini'
    if not os.path.exists(file_items_path):
        print(f"不存在此文件，修改itmes失败: {file_items_path}")
        return False

    print("正在修改items文件.....")
    with open(file_items_path, 'r') as f:
        line_list = f.readlines()
        if "ro.seewo.usb.adb" not in str(line_list):
            print("修改 默认 开启 adb")
            line_list.insert(line_list.index("items.end\n"), "persist.sys.seewo.develop.adb                   1\n")
            line_list.insert(line_list.index("items.end\n"), "ro.seewo.usb.adb                    1\n")
            line_list.insert(line_list.index("items.end\n"), "service.adb.tcp.port                    5555\n")
            line_list.insert(line_list.index("items.end\n"),
                             "persist.sys.seewo.monkey         true\n")  # monkey日志缓存增加
            line_list.insert(line_list.index("items.end\n"),
                             "persist.sys.mtklog.need.alert         1\n")  # 解决mtklog 弹窗警告问题

        if jointly_model or sale_model:
            file_name = file_path.split(r'\\')[-1]
            shutil.copy(f"{root_path}data\\items\\{file_name}_items.ini", file_items_path)  # 备份

        if jointly_model and len(str(jointly_model).strip()) >= 1:
            print("修改联名型号")
            for index, red in enumerate(line_list):
                if "ro.seewo.tags" in red:
                    line_list[index] = f'ro.seewo.tags {jointly_model}\n'
        if sale_model and len(str(sale_model).strip()) >= 1:
            print("修改销售型号")
            for index, red in enumerate(line_list):
                if "ro.seewo.sales.model" in red:
                    line_list[index] = f'ro.seewo.sales.model {sale_model}\n'

    with open(file_path + '\\items.ini', 'w', newline='\n') as f:
        f.writelines(line_list)
