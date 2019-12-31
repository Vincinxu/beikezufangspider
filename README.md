# 贝壳租房爬虫

## 主要使用技术：
requests ，beautifulsoup，MySQL，伪装请求头

## 流程：
首先分析爬取的url的组成元素和规律，提取出需要的变量和删掉可忽略的请求参数并重组url，然后使用requests请求页面获取源码， 再使用beautifulsoup解析源码并提取数据，最后将提取的数据保存到MySQL里，在运行该爬虫前， 先在MySQL中新建一个数据库并新建一张表用于存放数据。

新建数据库命令：
create database beike default character set utf8 collate utf8_general_ci;

新建表：
create table bk (image varchar(255) null, title varchar(255) null, description varchar(255) null, tag varchar(255) null, brand varchar(255), price varchar(255) null);
