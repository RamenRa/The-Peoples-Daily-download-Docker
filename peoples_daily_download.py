# encoding = UTF-8
import os
import re
import datetime
import requests
import logging
import sys
import newspaper_helper as helper

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("main")
logging.getLogger("chardet.charsetprober").disabled = True

def download_newspaper(newspaper_cover_url, newspaper_download_url_format, date, temp_folder):
    helper.init_or_clear_dir(temp_folder)

    # print("下载中……")
    logger.info("下载中……")

    path_format_date = date[0:4] + "-" + date[4:6] + "/" + date[6:8]

    # 获取报纸页数
    response = requests.get(newspaper_cover_url, headers=helper.headers)

    # 打印 页面内容
    # print(response.text)

    page_count = len(re.findall("nbs", response.text))
    # print("本期总共{}版".format(str(page_count)))
    logger.info("本期总共{}版".format(str(page_count)))
    # print("开始分片下载:")
    logger.info("开始分片下载:")
    for page in range(1, page_count + 1):
        format_page = f"%02d" % page
        file_url = newspaper_download_url_format.format(path_format_date, date, format_page)
        # print("第" + str(page) + "版 download url: " + file_url)
        logger.info("第" + str(page) + "版 download url: " + file_url)
        helper.download_file(file_url, temp_folder)

    # print("分片下载结束")
    logger.info("分片下载结束")


def download_newspaper_by_date(date):
    # print("下载日期:" + date)
    logger.info("下载日期:" + date)
    path_format_date = date[0:4] + "-" + date[4:6] + "/" + date[6:8]
    newspaper_cover_url = newspaper_cover_url_format.format(path_format_date)
    newspaper_pdf_filename = filename_prefix + date + ".pdf"
    # print("报纸封面链接:" + newspaper_cover_url)
    logger.info("报纸封面链接:" + newspaper_cover_url)

    if helper.check_local_newspaper_exist(helper.newspaper_saver_folder, newspaper_pdf_filename):
        # print("该日期已经下载过了! 每天早上07:30自动下载")
        logger.info("该日期已经下载过了! 每天早上07:30自动下载")
        return

    # 检测目标文件是否存在
    if helper.check_web_newspaper_exist(newspaper_cover_url):
        # 分片下载
        download_newspaper(newspaper_cover_url, newspaper_download_url_format, date, helper.temp_folder)
        # 获取排序后的分片文件名list
        filename_list = sorted(os.listdir(helper.temp_folder),
                               key=lambda x: os.path.getmtime(os.path.join(helper.temp_folder, x)))
        # print("本期总共{}版".format(str(len(filename_list))))
        logger.info("本期总共{}版".format(str(len(filename_list))))
        # 合并为整个pdf
        helper.merge_pdf(helper.temp_folder, filename_list, newspaper_pdf_filename, helper.newspaper_saver_folder)
        # 删除临时文件夹
        helper.clear_dir(helper.temp_folder)
        # print(date + " 获取完成: " + newspaper_pdf_filename)
        logger.info(date + " 获取完成: " + newspaper_pdf_filename)
        # print("\n")
        logger.info("\n")
    else:
        # print(date + "报纸不存在")
        logger.info(date + "报纸不存在")


if __name__ == '__main__':

    # newspaper config
    newspaper_name = f"==============={datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 人民日报自动下载合并================"
    filename_prefix = "PeoplesDaily_"
    newspaper_cover_url_format = "http://paper.people.com.cn/rmrb/html/{}/nbs.D110000renmrb_01.htm"
    newspaper_download_url_format = "http://paper.people.com.cn/rmrb/images/{0}/{2}/rmrb{1}{2}.pdf"

    # print(newspaper_name)
    logger.info(newspaper_name)

    # 获取输入参数
    input_args = helper.get_input_arg()

    # 开始日期
    start_date = input_args.start_date
    # 结束日期
    end_date = input_args.end_date
    if start_date:
        # print("--start_date:" + str(start_date))
        logger.info("--start_date:" + str(start_date))
    if end_date:
        # print("--end_date:" + str(end_date))
        logger.info("--end_date:" + str(end_date))

    if not helper.param_is_none(start_date):
        # 开始日期不为空 下载开始日期到结束日期的所有报纸
        end_date = helper.get_today_date() if helper.param_is_none(end_date) else end_date
        # print("final_start_date:" + start_date)
        logger.info("final_start_date:" + start_date)
        # print("final_end_date:" + end_date)
        logger.info("final_end_date:" + end_date)
        date_list = helper.get_date_list(start_date, end_date)
        for cur_date in date_list:
            download_newspaper_by_date(cur_date)
    else:
        # 只获一天报纸
        date = input_args.date
        if date:
            # print("--date:" + str(date))
            logger.info("--date:" + str(date))
        date = helper.get_today_date() if helper.param_is_none(date) else date
        # print("最新日期:" + date)
        logger.info("最新日期:" + date)
        download_newspaper_by_date(date)
    helper.limt_pdf_files(helper.newspaper_saver_folder)

