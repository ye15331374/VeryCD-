# VeryCD-
代码主要分为download、save_to_file、pa三个模块
download用来请求网页，解析网页和筛选目标信息
save_to_file用来存储数据，格式为csv文件
pa用于启动和结束爬虫，每爬一个页面前清空存储数据的数组，显示当前页码，和获取下一页页码
代码最后的pa（1,3372）表示从第一页开始，到3372页结束

代码使用python3.7编写，运行前需要安装Beautifulsoup第三方库
