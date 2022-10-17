# encoding = UTF-8
import os
import argparse
import datetime
import calendar
import shutil
import urllib

import requests

import PyPDF2

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
}

temp_folder = "./part"  # 临时文件夹，存每一页的文件，每次运行会自动创建和删除
newspaper_saver_folder = './newspaper'  # 报纸保存位置，没有就自动创建


def get_input_arg():
    # 解析输入参数
    parser = argparse.ArgumentParser(description='Manual to this script')
    parser.add_argument("--date", type=str, default=None, help='input date,format: 20220901')
    return parser.parse_args()


def get_today_date():
    return datetime.date.today().strftime("%Y%m%d")


def get_monday(date_str):
    current_day = datetime.datetime.strptime(date_str, '%Y%m%d')
    oneday = datetime.timedelta(days=1)

    while current_day.weekday() != calendar.MONDAY:
        current_day -= oneday

    return current_day.strftime('%Y%m%d')


def get_this_monday():
    current_day = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    while current_day.weekday() != calendar.MONDAY:
        current_day -= oneday
    return current_day.strftime('%Y%m%d')


def get_date_list(start, end):
    date_list = []
    date = datetime.datetime.strptime(start, '%Y%m%d')
    end = datetime.datetime.strptime(end, '%Y%m%d')
    while date <= end:
        date_list.append(date.strftime('%Y%m%d'))
        date = date + datetime.timedelta(1)
    return date_list


def init_or_clear_dir(dir):
    # 清空临时文件缓存
    if os.path.exists(dir):
        print('清空临时文件')
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


def check_newspaper_exist(local_save_folder, remote_web_url, newspaper_filename):
    creat_folder_if_not_exist(local_save_folder)

    if os.path.exists(local_save_folder):
        filename_list = os.listdir(local_save_folder)

        if newspaper_filename in filename_list:
            print("该日期已经下载过了!")
            exit(0)

        # check web newspaper exist
        response = requests.get(remote_web_url, headers=headers)
        if response.status_code == 403:
            print("您选择的日期太久远，网站不提供")
            exit(0)
        if response.status_code == 404:
            print("未找到指定日期的报纸，请尝试其他日期")
            exit(0)


def read_html_as_str(web_url):
    response = requests.get(web_url, headers=headers)
    response.encoding = 'UTF-8'
    return response.text


def download_file(file_url, save_folder):
    file_name = os.path.basename(file_url)
    # response = requests.get(file_url, headers=headers)
    # file = response.content
    # with open(os.path.join(save_folder, file_name), "wb") as fn:
    #     fn.write(file)
    urllib.request.urlretrieve(file_url, os.path.join(save_folder, file_name))


def merge_pdf(source_dir, filename_list, final_filename, target_dir):
    print('合并{0}个PDF文件为单个PDF文件'.format(str(len(filename_list))))

    pdf_file_merger = PyPDF2.PdfFileMerger(strict=False)

    for file_name in filename_list:
        file_path = source_dir + '/' + file_name
        pdf_file_merger.append(file_path)
        # pdf_file_merger.append(PdfFileReader(open(file_path, 'rb')))

    target_file_path = target_dir + "/" + final_filename
    pdf_file_merger.write(target_file_path)
    pdf_file_merger.close()

    print("合并成功\n")
