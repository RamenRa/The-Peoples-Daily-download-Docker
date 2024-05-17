# 关于人民日报自动下载的Dokcer项目
[当前页面的Docker](https://hub.docker.com/r/ramen31/peoples_daily_download)

## 简介
  人民日报电子版自动下载脚本

  可实现下载人民日报电子版并将某一天的人民日报多页PDF合并为一整个PDF文件，方便阅览。

  可下载指定日期的人民日报
  

## 自定义构建镜像

### 需要Docker环境，能正常拉取github文件和docker镜像

1. 拉取文件

   *群晖系统没有git命令，请手动下载zip自行解压或安装git*
   ```
   git clone https://github.com/RamenRa/The-Peoples-Daily-download-Docker.git && cd The-Peoples-Daily-download-Docker/
   ```


2. (可选操作)修改下载时间 ，默认07：30运行 ，官网04：00更新
   ```
    echo "30 07 * * * root /usr/local/bin/python /app/peoples_daily_download.py > /var/log/cron.log 2>&1" > crontab
   ```
   (可选操作)注释“peoples_daily_download.py”内最后一行代码解除pdf文件366个限制

3. 构建镜像并运行
   
   构建镜像
   
    ```
   docker build -t peoples_daily_download .
    ```
    
   运行镜像
   ```
   docker run -d --name peoples_daily_download -v [保存PDF的路径]:/app/newspaper peoples_daily_download
   ```
   查看日志，Ctrl + c退出
   
    ```
    docker logs -f peoples_daily_download
    ```
    

#### 下载指定日期的人民日报

 需要下载指定日期的人民日报，需要在脚本命令后面加上--date 参数，以下载指定日期的人民日报参数格式为yyyyMMdd，月日小于10时，需要前方0补位。
例如下载2022年9月1日的人民日报，执行如下命令：
   ```shell
   docker exec peoples_daily_download python /app/peoples_daily_download.py --date 20220901
   ```

--------------------------

## 版权说明
   因为报纸方要求不得将电子版应用于商业，故此脚本也不得用于商业，仅供学习与非盈利个人场合使用。


