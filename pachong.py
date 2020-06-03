import csv
import requests
from bs4 import BeautifulSoup  # 从bs4引入BeautifulSoup

#创建用于临时保存每页爬取的数据，分别为类型，名字，上传时间，更新时间，文件数量，大小，评论数
type = []
music_name = []
music_atime = []
music_btime = []
music_number = []
music_size = []
music_comment = []
#请求网页，解析数据并筛选目标信息
def download(pagenum):    #pagenum为当前爬取的网页页码
    #获取当前的网页链接
    url = "http://www.verycd.com/sto/music/~all/page" + str(pagenum)
    #请求网页
    response = requests.get(url)
    # 初始化BeautifulSoup：利用网页字符串自带的编码信息解析网页，我使用的是lxml解析器
    soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')


    #寻找“类型”信息，该信息位于标签<span, class_="left_topics_class_sort">下的标签<a>中
    for type_span in soup.find_all('span', class_="left_topics_class_sort"):  #寻找所有的标签<span, class_="left_topics_class_sort">
        music_type_span = type_span.find_all('a')      #寻找标签<a>
        music_type = music_type_span[0].string      #提取标签<a>内的信息
        print('类型: {}'.format(music_type))
        #保存到数组中
        type.append(music_type)


    #寻找“名字”信息，该信息位于标签<h3>下的标签<a>中
    for name_a in soup.find_all('h3'):           #寻找所有的标签<h3>
        music_name_a = name_a.find_all('a')          #寻找所有的标签<a>
        music_name.append( music_name_a[1].string)      #提取信息
        print('名字：{}'.format( music_name_a[1].string))
        #保存到数组中

    #寻找“上传时间”“更新日期”“文件数”“大小”“评论数”信息，这些信息位于标签<span, style="color:green;">中
    number = soup.find_all('span', style="color:green;")   #寻找标签<span, style="color:green;">
    for index in range(len(number)):
        all_dataspan = number[index].find_all('span')       #寻找所有<span>
        all_other_num = number[index].find_all('strong')    #寻找所有<strong>
        music_atime.append(all_dataspan[0].string)          #上传时间在第一个<span>中
        music_btime.append(all_dataspan[1].string)          #上传时间在第二个<span>中
        music_number.append(all_other_num[0].string)        #文件数在第一个<strong>中
        music_size.append(all_other_num[1].string)          #文件数在第二个<strong>中
        if(len(all_other_num)==2):                          #评论数在第三个<strong>中，并需要判断没有评论的情况
            music_comment.append("0")
        else:
            music_comment.append(all_other_num[2].string)

        print('上传日期：{}，更新日期：{}，文件数：{}，大小：{}， 评论数：{}'.format(
            all_dataspan[0].string,all_dataspan[1].string,all_other_num[0].string,all_other_num[1].string, "=="))

#爬到的数据存储到csv文件中
def save_to_file(i):
    filename = "musicdata.csv"  #文件名
    if (i == 1):
        csv_file = open(filename, 'w', encoding="utf-8", newline='')
        writer = csv.writer(csv_file)
        writer.writerow(["类型", "名字", "上传日期", "更新日期", "文件数", "大小", "评论数"])  # 写入标题
    csv_file = open(filename, 'a+', encoding="utf-8", newline='')
    writer = csv.writer(csv_file)
    for index in range(len(type)):
       writer.writerow([type[index], music_name[index], music_atime[index], music_btime[index],  music_number[index], music_size[index], music_comment[index]])
    csv_file.close()
    print("write_finished!")
#设置爬虫的开始和结束，start为开始的页码，end为结束的页码
def pa(start,end):
    i = start   #i初始值等于开始的页码
    while (i <= end):
        #每页网页开始前清空数组
        type.clear()
        music_name.clear()
        music_atime.clear()
        music_btime.clear()
        music_number.clear()
        music_size.clear()
        music_comment.clear()
        download(i)                        #请求网页，解析网页，筛选信息
        print("当前页数:  " + str(i))       #显示当前爬取的页码
        save_to_file(i)                    #存取当前页爬到的数据
        i = i + 1                           #获得下一页的页码

pa(1,3372)                                 #设置每次爬虫开始和结束的页码
