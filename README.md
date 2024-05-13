# The-Peoples-Daily-download

## 简介
人民日报电子版自动下载脚本

可实现下载人民日报电子版并将某一天的人民日报多页PDF合并为一整个PDF文件，方便阅览。

## 使用

### 需要Docker环境，能正常拉取github文件和docker镜像

拉取文件
```
git clone https://github.com/RamenRa/The-Peoples-Daily-download-Docker.git && cd The-Peoples-Daily-download-Docker/
```
现在你可以使用vi或者nano文本编辑器编辑crontab。用于自定义下载时间，默认07：30。官网04：00更新
构建镜像
```
docker build -t peoples_daily_download .

docker run -d --name peoples_daily_download -v [宿主机要保存PDF的路径]:/app/newspaper peoples_daily_download
```

#### 下载指定日期的人民日报

需要下载指定日期的人民日报，需要在脚本命令后面加上--date 参数，以下载指定日期的人民日报参数格式为yyyyMMdd，月日小于10时，需要前方0补位。
例如下载2022年9月1日的人民日报，执行如下命令：
```shell
python3 peoples_daily_download.py --date 20220901
```

--------------------------

## 版权说明
因为报纸方要求不得将电子版应用于商业，故此脚本也不得用于商业，仅供学习与非盈利个人场合使用。


