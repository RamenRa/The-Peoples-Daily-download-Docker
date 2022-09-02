# -*- coding: UTF-8 -*-
import requests
import re
import PyPDF2
import os
import shutil
import datetime
import argparse

headers={
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
}

def download(date,partpath,newspaperpatch):
    date_simple=date
    date_path_format=date[0:4]+"-"+date[4:6]+"/"+date[6:8]
    print("date_simple: "+date_simple)
    print("date_path_format: "+date_path_format)
    
    try:
        os.mkdir(newspaperpatch)
    except:
        pass
    filelist=os.listdir(newspaperpatch)
    if "People's.Daily.{}.pdf".format(date_simple) in filelist:
        print("该日期已经下载过了!")
        print("You alreay download this newspaper!")
        exit(0)
    coverurl="http://paper.people.com.cn/rmrb/html/{}/nbs.D110000renmrb_01.htm".format(date_path_format)
    response=requests.get(coverurl,headers=headers)
    pagenum=re.findall("nbs",response.text)#get page number
    if response.status_code==403:
        print("你选择的日期太久远，网站不提供。只有两年之内的。")
        exit(0)
    try:
        os.mkdir('./part')
    except:
        shutil.rmtree(partpath)
    print("下载中……")
    #http://paper.people.com.cn/rmrb/images/2022-09/01/11/rmrb2022090111.pdf
    for page in range(1,len(pagenum)+1):
        downtplurl="http://paper.people.com.cn/rmrb/images/{0}/{2}/rmrb{1}{2}.pdf"
        formatpage=f"%02d" % page
        downurl=downtplurl.format(date_path_format,date_simple,formatpage)
        print("downloadurl=" + downurl)
        filename='rmrb{}.pdf'.format(date_simple+formatpage)
        print("filename=" + filename)
        response=requests.get(downurl,headers=headers)
        file=response.content
        with open(partpath+"/"+filename,"wb") as fn:
            fn.write(file)
def merge(partpath,newspaperpatch):
    filelist=os.listdir(partpath)
    #排序 保证拼接的顺序
    filelist.sort()
    pdfFM=PyPDF2.PdfFileMerger(strict=False)
    for file in filelist:
        pdfFM.append(partpath+'/'+file)
    pdfFM.write(newspaperpatch+"/People's.Daily."+filelist[0][4:12]+".pdf")     #保存新文件在newspaperpatch下
    pdfFM.close()

def delete(partpath):
    shutil.rmtree(partpath)
 


if __name__ == '__main__':

    partpath="./part" #临时文件夹，存每一页的文件，每次运行会自动创建和删除
    newspaperpatch='./newspaper' #报纸保存位置，没有就自动创建
    
    parser= argparse.ArgumentParser(description='manual to this script')
    today= datetime.date.today().strftime("%Y%m%d")
    parser.add_argument("--date", type=str, default= today, help='input date,format: 20220901')
    args = parser.parse_args()
    
    # 日期
    date=args.date
    #date="20220901"     #默认下载当天的，也可在此手动修改日期，去掉注释按格式设置日期
    print("date:"+date)
    download(date,partpath,newspaperpatch) #分片下载
    merge(partpath,newspaperpatch)#合并
    delete(partpath)#删除临时文件夹partpath






