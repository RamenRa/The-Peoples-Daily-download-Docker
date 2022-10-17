# encoding = UTF-8
import os
import re
import requests

import newspaper_helper as helper


def download_newspaper(newspaper_cover_url, newspaper_download_url_format, temp_folder):
    helper.creat_folder_if_not_exist(temp_folder)

    print("下载中……")
    print(newspaper_cover_url)

    # 获取报纸页数
    response = requests.get(newspaper_cover_url, headers=helper.headers)

    # 打印 页面内容
    # print(response.text)

    page_count = len(re.findall("nbs", response.text))
    print("本期总共{}版".format(str(page_count)))
    print("开始分片下载:")
    for page in range(1, page_count + 1):
        format_page = f"%02d" % page
        file_url = newspaper_download_url_format.format(path_format_date, date, format_page)
        print("第" + str(page) + "版 download url: " + file_url)
        helper.download_file(file_url, temp_folder)

    print("分片下载结束")


if __name__ == '__main__':

    # newspaper config
    newspaper_name = "人民日报"
    filename_prefix = "PeoplesDaily_"
    newspaper_cover_url_format = "http://paper.people.com.cn/rmrb/html/{}/nbs.D110000renmrb_01.htm"
    newspaper_download_url_format = "http://paper.people.com.cn/rmrb/images/{0}/{2}/rmrb{1}{2}.pdf"

    # 获取输入参数
    input_args = helper.get_input_arg()

    # 日期
    date = input_args.date

    # 获取周报本周的出版日
    date = helper.get_this_monday() if (date is None or "none" == date) else helper.get_monday(date)

    path_format_date = date[0:4] + "-" + date[4:6] + "/" + date[6:8]
    newspaper_cover_url = newspaper_cover_url_format.format(path_format_date)
    newspaper_pdf_filename = filename_prefix + date + ".pdf"

    print(newspaper_name)

    # 日期 格式: 20220901
    print("日期:" + date)

    # 检测目标文件是否存在
    helper.check_newspaper_exist(helper.newspaper_saver_folder, newspaper_cover_url, newspaper_pdf_filename)

    # 分片下载
    download_newspaper(newspaper_cover_url, newspaper_download_url_format, helper.temp_folder)

    # 获取排序后的分片文件名list
    filename_list = sorted(os.listdir(helper.temp_folder),
                           key=lambda x: os.path.getmtime(os.path.join(helper.temp_folder, x)))
    print("本期总共{}版".format(str(len(filename_list))))

    # 合并为整个pdf
    helper.merge_pdf(helper.temp_folder, filename_list, newspaper_pdf_filename, helper.newspaper_saver_folder)

    # 删除临时文件夹
    helper.clear_dir(helper.temp_folder)

    print("获取完成: " + newspaper_pdf_filename)
    print("\n")
