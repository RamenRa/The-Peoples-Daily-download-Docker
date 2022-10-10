# encoding = UTF-8
import os
import re
import shutil
import datetime
import requests
import argparse

import PyPDF2


def creat_folder_if_not_exist(folder):
    # if folder not exist, create folder
    if not os.path.exists(folder):
        os.makedirs(folder)


def check_newspaper_exist(paper_save_folder, paper_pdf_filename, newspaper_cover_url):

    creat_folder_if_not_exist(paper_save_folder)

    filelist = os.listdir(paper_save_folder)

    if paper_pdf_filename in filelist:
        print("该日期已经下载过了!")
        exit(0)

    # check web newspaper exist
    response = requests.get(newspaper_cover_url, headers=headers)
    if response.status_code == 403:
        print("您选择的日期太久远，网站不提供")
        exit(0)
    if response.status_code == 404:
        print("未找到指定日期的报纸，请尝试其他日期")
        exit(0)


def download_newspaper(newspaper_cover_url, newspaper_download_url_format, temp_folder):

    creat_folder_if_not_exist(temp_folder)

    print("下载中……")
    print(newspaper_cover_url)

    # 获取报纸页数
    response = requests.get(newspaper_cover_url, headers=headers)
    page_count = len(re.findall("nbs", response.text))

    print("本期总共{}版".format(str(page_count)))
    print("开始分片下载:")
    for page in range(1, page_count + 1):
        format_page = f"%02d" % page
        file_url = newspaper_download_url_format.format(path_format_date, date, format_page)
        print("第" + str(page) + "版 download url: " + file_url)
        download_file(file_url, temp_folder)

    print("分片下载结束")


def download_file(file_url, save_folder):

    file_name = os.path.basename(file_url)
    response = requests.get(file_url, headers=headers)
    file = response.content
    with open(save_folder + "/" + file_name, "wb") as fn:
        fn.write(file)


def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        # print(dir_list)
        return dir_list


def merge_pdf(source_folder,  filename, aimed_folder):
    source_file_list = get_file_list(source_folder)

    pdf_file_merger = PyPDF2.PdfFileMerger(strict=False)

    for file in source_file_list:
        pdf_file_merger.append(source_folder + '/' + file)

    pdf_file_merger.write(aimed_folder + "/" + filename)
    pdf_file_merger.close()


if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
    }
    temp_folder = "./part"  # 临时文件夹，存每一页的文件，每次运行会自动创建和删除
    newspaper_saver_folder = './newspaper'  # 报纸保存位置，没有就自动创建

    # newspaper config
    filename_prefix ="People's.Daily."
    newspaper_cover_url_format = "http://paper.people.com.cn/rmrb/html/{}/nbs.D110000renmrb_01.htm"

    # 解析输入参数
    parser = argparse.ArgumentParser(description='Manual to this script')
    today = datetime.date.today().strftime("%Y%m%d")
    parser.add_argument("--date", type=str, default=today, help='input date,format: 20220901')
    args = parser.parse_args()

    # 日期
    date = args.date

    path_format_date = date[0:4]+"-"+date[4:6]+"/"+date[6:8]
    newspaper_cover_url = newspaper_cover_url_format.format(path_format_date)
    newspaper_pdf_filename = filename_prefix + date + ".pdf"
    newspaper_download_url_format = "http://paper.people.com.cn/rmrb/images/{0}/{2}/rmrb{1}{2}.pdf"

    print("人民日报下载")

    # 日期 格式: 20220901
    print("日期:" + date)

    # 检测目标文件是否存在
    check_newspaper_exist(newspaper_saver_folder, newspaper_pdf_filename, newspaper_cover_url)

    # 清空临时文件缓存
    if os.path.exists(temp_folder):
        print('清空临时文件')
        shutil.rmtree(temp_folder)
        # 重建缓存目录
        os.makedirs(temp_folder)

    # 分片下载
    download_newspaper(newspaper_cover_url, newspaper_download_url_format, temp_folder)

    # 合并为整个pdf
    print('合并为单个PDF文件:' + newspaper_pdf_filename)
    merge_pdf(temp_folder, newspaper_pdf_filename, newspaper_saver_folder)

    # 删除临时文件夹
    shutil.rmtree(temp_folder)