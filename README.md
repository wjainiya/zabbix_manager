# Zabbix_manager(server)

> (原github地址)[https://github.com/BillWang139967/zabbix_manager.git]

## Zabbix_api version

* V1.4 基础上更新
    * v1.4，2019-2-22 [更新] 
        * 在 main.py 中 添加功能 week_report_image
        * 在 zabbix login()中添加 requests.session方式登陆,方便获graph图片等.
        * 添加方法 get_graph_images(),根据 hostname 获取对应的graph 图片并保存,思路：
          主机hostname-->hostid,graphid-->chart数字(详见self.Graph_Chart)-->拼接graph_image的url.例如
          http://localhost:8080/chart6.php?graphid=2125&period=604800&stime=20190213092511&isNow=1&profileIdx=web.graphs&profileIdx2=2125&sid=84c1098578a9c18c&screenid=&curtime=1550626245469
        * 添加库 image_merger.py,将获取的graph 图片合并成一张图片
        * 添加 zabbix logout()
        * 修改 urlib 库, 使用 requests 库

## 小额捐款

如果觉得 `zabbix_manager` 对您有帮助，可以请笔者喝杯咖啡

[Screenshot](images/5.jpg)

## 致谢

1. 感谢原作者 meetbill
