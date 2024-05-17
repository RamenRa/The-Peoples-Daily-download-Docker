# encoding = UTF-8
import os
import argparse
import datetime
import calendar
import shutil

import pytz
import requests

import PyPDF2
import glob
import logging

import warnings

warnings.filterwarnings("ignore")
logging.basicConfig(  
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",  
    level=logging.INFO,  
    datefmt="%Y-%m-%d %H:%M:%S",  # 添加了年、月、日  
    stream=sys.stdout,  
)  
# 在模块级别配置日志记录器
logger = logging.getLogger("helper")

logger.setLevel(logging.INFO)

current_directory = os.path.dirname(os.path.abspath(__file__))

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
}

timezone = pytz.timezone('Asia/Shanghai')

temp_folder = f"{current_directory}/part"  # 临时文件夹，存每一页的文件，每次运行会自动创建和删除
newspaper_saver_folder = f'{current_directory}/newspaper'  # 报纸保存位置，没有就自动创建


def get_input_arg():
    # 解析输入参数
    parser = argparse.ArgumentParser(description='Manual to this script')
    parser.add_argument("--date", type=str, default=None, help='input date,format: 20220901')
    parser.add_argument("--start_date", type=str, default=None, help='input start_date,format: 20220901')
    parser.add_argument("--end_date", type=str, default=None, help='input end_date,format: 20220901')
    return parser.parse_args()


def param_is_none(param):
    return param is None or "none" == param


def get_today_date():
    return datetime.datetime.now(timezone).strftime("%Y%m%d")


def get_last_weekday_date(date, weekday):
    current_day = datetime.datetime.strptime(date, '%Y%m%d')
    oneday = datetime.timedelta(days=1)

    while current_day.weekday() != weekday:
        current_day -= oneday

    return current_day.strftime('%Y%m%d')


def get_this_monday_date():
    current_day = datetime.datetime.now(timezone).date()
    oneday = datetime.timedelta(days=1)
    while current_day.weekday() != calendar.MONDAY:
        current_day -= oneday
    return current_day.strftime('%Y%m%d')


def get_date_list(start, end, week):
    date_list = []
    date = datetime.datetime.strptime(start, '%Y%m%d')
    end = datetime.datetime.strptime(end, '%Y%m%d')
    while date <= end:
        if date.weekday() == week:
            date_list.append(date.strftime('%Y%m%d'))
        date = date + datetime.timedelta(1)
    return date_list


def get_date_list(start, end):
    date_list = []
    date = datetime.datetime.strptime(start, '%Y%m%d')
    end = datetime.datetime.strptime(end, '%Y%m%d')
    while date <= end:
        date_list.append(date.strftime('%Y%m%d'))
        date = date + datetime.timedelta(1)
    return date_list


def date_is_before(date_str, standard_date_str):
    date = datetime.datetime.strptime(date_str, '%Y%m%d')
    standard_date = datetime.datetime.strptime(standard_date_str, '%Y%m%d')
    return date < standard_date


def init_or_clear_dir(dir):
    # 清空临时文件缓存
    if os.path.exists(dir):
        # print('清空临时文件')
        logger.info('清空临时文件')
        shutil.rmtree(dir)
        # 重建缓存目录
        os.makedirs(dir)
    else:
        os.makedirs(dir)


def clear_dir(dir):
    shutil.rmtree(dir)


def creat_folder_if_not_exist(folder):
    # if folder not exist, create folder
    if not os.path.exists(folder):
        os.makedirs(folder)


def check_local_newspaper_exist(local_save_folder, newspaper_filename):
    creat_folder_if_not_exist(local_save_folder)

    if not os.path.exists(local_save_folder):
        return False
    filename_list = os.listdir(local_save_folder)
    return newspaper_filename in filename_list


def check_web_newspaper_exist(remote_web_url):
    # check web newspaper exist

    # print(remote_web_url)
    response = requests.get(remote_web_url, headers=headers)

    if response.status_code == 200:
        return True

    if response.status_code == 403:
        # print("您选择的日期太久远，网站不提供")
        logger.info("您选择的日期太久远，网站不提供")
        return False

    if response.status_code == 404:
        # print("未找到指定日期的报纸，请尝试其他日期")
        logger.info("未找到指定日期的报纸，请尝试其他日期")
        return False

    # print("未找到指定日期的报纸，请尝试其他日期")
    logger.info("未找到指定日期的报纸，请尝试其他日期")
    return False


def read_html_as_str(web_url):
    response = requests.get(web_url, headers=headers)
    response.encoding = 'UTF-8'
    return response.text


def download_file(file_url, save_folder):
    file_name = os.path.basename(file_url)
    try:
        response = requests.get(file_url, headers=headers)
        file = response.content
        with open(os.path.join(save_folder, file_name), "wb") as fn:
            fn.write(file)
    except:
        # print("网络文件不存在，WebUrl:" + file_url)
        logger.info("网络文件不存在，WebUrl:" + file_url)


def merge_pdf(source_dir, filename_list, final_filename, target_dir):
    creat_folder_if_not_exist(target_dir)
    logger.info('合并{0}个PDF文件为单个PDF文件'.format(str(len(filename_list))))
    # print('合并{0}个PDF文件为单个PDF文件'.format(str(len(filename_list))))

    # pdf_file_merger = PyPDF2.PdfMerger(strict=False)
    try:
        pdf_file_merger = PyPDF2.PdfFileMerger(strict=False)
    except:
        pdf_file_merger = PyPDF2.PdfMerger(strict=False)

    for file_name in filename_list:
        file_path = source_dir + '/' + file_name
        pdf_file_merger.append(file_path)
        # pdf_file_merger.append(PdfFileReader(open(file_path, 'rb')))

    target_file_path = target_dir + "/" + final_filename
    pdf_file_merger.write(target_file_path)
    pdf_file_merger.close()

    # print("合并成功\n")
    logger.info("合并成功\n")


def limit_pdf_files(folder_path, max_files=366):
    """
    从指定文件夹中删除最旧的PDF文件，直到文件数量小于或等于max_files。
    
    参数:
    folder_path (str): 包含PDF文件的文件夹路径。
    max_files (int): 文件夹中允许保留的最大PDF文件数量。
    
    返回:
    None
    """
    # 获取指定文件夹下所有的PDF文件
    pdf_files = glob.glob(os.path.join(folder_path, '*.pdf'))
    
    # 如果PDF文件数量大于max_files
    if len(pdf_files) > max_files:
        # 按照修改时间对文件进行排序（最旧的在前）
        pdf_files.sort(key=os.path.getmtime)
        
        # 获取需要删除的文件列表
        files_to_delete = pdf_files[:len(pdf_files) - max_files]
        
        # 删除文件
        for file_to_delete in files_to_delete:
            try:
                os.remove(file_to_delete)
                logger.info(f"已删除文件: {file_to_delete}")
            except Exception as e:
                logger.error(f"删除文件时出错: {file_to_delete}, 错误信息: {e}")

    else:
        logger.info(f"当前PDF文件数量 {len(pdf_files)} 个，限制 {max_files} 个。")
