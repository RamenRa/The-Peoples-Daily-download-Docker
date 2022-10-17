# The-Peoples-Daily-download

## 简介
人民日报电子版自动下载脚本

可实现下载人民日报电子版并将某一天的人民日报多页PDF合并为一整个PDF文件，方便阅览。

1. 下载当天人民日报
2. 下载指定日期人民日报电子版

## 使用准备工作

### 读写权限

权限：目录下允许读写，默认不需要配置，如执行过程中提示有权限问题，可以进行检查，配置为读写权限

### 依赖库安装

脚本依赖库模块：requests re PyPDF2 os shutil datetime

其中PyPDF2需要单独安装

#### 类Unix系统
类unix系统安装方式如下：

- 安装PyPDF2 用于合并PDF文件

```shell
pip3 install PyPDF2
```

- 安装pytz module 用于获取时区
- 
```shell
sudo pip3 install pytz
```

如果未安装pip3则需要先安装pip3
- 安装pip3

```shell
sudo apt install python3-pip
```

## 使用脚本

### 类Unix系统

#### 下载当天的人民日报

默认方式执行以下命令，会下载当天的人民日报。

```shell
python3 peoples_daily_download.py
```
#### 下载指定日期的人民日报

需要下载指定日期的人民日报，需要在脚本命令后面加上--date 参数，以下载指定日期的人民日报参数格式为yyyyMMdd，月日小于10时，需要前方0补位。
例如下载2022年9月1日的人民日报，执行如下命令：
```shell
python3 peoples_daily_download.py --date 20220901
```
### Windows

执行命令同类Unix系统，可以结合Windows系统的特性进行进一步配置。

推荐最佳使用姿势：
可以在windows建立一个计划任务，每天定时执行此脚本，报纸会自动出现在你的桌面。  

--------------------------

## 版权说明
因为报纸方要求不得将电子版应用于商业，故此脚本也不得用于商业，仅供学习与非盈利个人场合使用。


