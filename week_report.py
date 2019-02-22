#!/usr/bin/python
#coding:utf-8

from __future__ import print_function
__version__ = "1.4.05"

import sys
import os
import time
import tarfile

root_path = os.path.split(os.path.realpath(__file__))[0]
os.chdir(root_path)
sys.path.insert(0, os.path.join(root_path, 'ZabbixTool/lib_zabbix'))
sys.path.insert(0, os.path.join(root_path, 'ZabbixTool/py_tool/my_lib'))
from zabbix_api import zabbix_api
import image_merge
import pyMail


reload(sys)
sys.setdefaultencoding("utf-8")

zabbix_servers = [
    {"profile": "aliyunzabbix",
      "hostnames": [
          "Zabbix server",
          "rds_vms3_cloud_user_manage",
          "rds_vidon_videos",
          "rds_vidonhome_new",
          "rds_pos_vidon",
          "rds_onlyread_pos_rds",
      ]
    },
    {"profile": "dvdfabzabbix",
      "hostnames": [
          "api3.dvdfab.cn-174.142.186.234",
          "cserv-236",
          "download-50.31.252.12-jp",
          "download-108.61.187.43-jp",
          "download-167.179.77.19",
          "download-167.179.87.195",
          "download-194.58.88.115",
          "download-194.58.115.17",
          "download-194.58.115.18",
          "download_iweb_207",
          "dvdfabstore-89.108.125.12",
          "dvdfab Zabbix server",
          "forum-194.58.115.8",
          "iweb-wgj-67.205.126.82",
          "mailru-194.58.115.15",
          "nginx-58",
          "pair_dedicated_server",
          "ru-wangguijun_176.99.3.117",
          "test-40",
          "test-235",
          "uhddiy-jp-150.95.216.41",
          "vmdb-237",
          "www.dvdfab.cn-jp",
          "www.dvdfab.cn-ru"
      ]
    },
    {"profile": "viduszabbix",
      "hostnames": [
          "Zabbix server",
          "blog-vidus-cn",
          "devops-vidus",
          "yds-vidus-cn"
      ]
    },
]

# date_from = "2019-01-10 00:00:00"
# date_till = "2019-01-17 00:00:00"

dateFormat = "%Y-%m-%d %H:%M:%S"
now = time.time()
one_week_before = now - 604800
date_from = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(one_week_before))
date_till = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))

filters = [
    "CPU load",
    "Disk space usage /",
    "Disk space usage /etc/hosts",
    "Memory usage",
    "Swap usage",
    "MySQL bandwidth",
    "MySQL operations",
    "MySQL Ping",
    "MySQL SIZE",
]


for server in zabbix_servers:
    if server['profile'] == "aliyunzabbix":
        continue
    #登陆
    zapi = zabbix_api(profile=server['profile'])
    # 抓图
    img_dir = "/code/png/" + server['profile']
    res = zapi.get_graph_images(host_names=server['hostnames'],filters=filters,date_from=date_from,date_till=date_till,img_dir=img_dir)

    # 注销
    zapi.logout()
    # 获取图片名称
    for item in res:
        img_list = []
        for name in item['hostimages']:
            print (name['image_name'])
            img_list.append(name['image_name'])

        # 合并图片
        output_dir = "/code/output/" + server['profile']
        image_merge.image_merge(img_list,output_dir=output_dir,output_name=item['hostname']+".jpg")


# #创建压缩包名
tar_file = "/code/tartest.tar.gz"
tar = tarfile.open(tar_file,"w:gz")
# #创建压缩包
for root,dir,files in os.walk("/code/output"):
    for file in files:
        fullpath = os.path.join(root,file)
        tar.add(fullpath)
tar.close()


# #发送邮件
usettls = False
sml = pyMail.SendMailDealer('buildbot@goland.cn','123456','mail.goland.cn','25',usettls = usettls)
# #2 设置邮件信息
# #参数包括("收件人","标题","正文","格式html/plain","附件路径1","附件路径2")
send_to = [
    "tao.wang@goland.cn",
    "shaofei.ma@goland.cn"
]
for user in send_to:
    sml.setMailInfo('zabbix数据图','zabbix 监控服务器数据图','plain',tar_file)
    # 3 发送邮件
    sml.sendMail(rec_user=user)

