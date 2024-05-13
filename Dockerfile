FROM python:3.10-slim

# 设置时区
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

# 安装cron
RUN apt-get update && apt-get -y install cron

# 设置工作目录
WORKDIR /app

# 复制requirements.txt和项目代码到容器中
COPY requirements.txt /app/
COPY peoples_daily_download.py /app/
COPY newspaper_helper.py /app/

# 设置定时任务
COPY crontab /etc/cron.d/peoples_daily_download_cron
RUN chmod 0644 /etc/cron.d/peoples_daily_download_cron
RUN crontab /etc/cron.d/peoples_daily_download_cron
RUN touch /var/log/cron.log

# 安装依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 创建一个挂载点，用户可以映射一个文件夹到这个目录
VOLUME /app/newspaper

# 当容器启动时，先执行一次脚本，然后运行cron并保持前台进程活跃
CMD python /app/peoples_daily_download.py && cron && tail -f /var/log/cron.log
