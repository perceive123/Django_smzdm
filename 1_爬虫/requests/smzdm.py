import requests
import bs4
import pymysql
from time import sleep


def url_open(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
    res = requests.get(url, headers=headers)
    return res

def get_feedback(url,title):
    res=url_open(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    result=[]
    try:
        comment_lists = soup.find('div', id='commentTabBlockNew').find_all('div', class_='comment_conBox')
        for comment_list in comment_lists:
            #评论时间
            comment_time=comment_list.find('div',class_='time').text
            # 评论内容
            comment=comment_list.find('div',class_='comment_conWrap',recursive=False).find('div',class_='comment_con').text.strip()
            # 情感评分
            sentiment=SnowNLP(comment).sentiments
        return result
    except:
        return [[title,0,0]]

def get_pages(url):
    res=url_open(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    try:
        pages=int(soup.find('li',class_='pagedown').previous_sibling.text)
    except:
        pages=1
    return pages

def find_phone(res,num):
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    result_end = []
    url_title_list = soup.find_all('h5', class_='feed-block-title')
    for each in url_title_list[:num]:
        try:
            title = each.text#手机名称
            url_feedback=each.a.get('href')#评论网址
            pages=get_pages(url_feedback)#获取页面数量
            print(f'正在爬取{title} {url_feedback}')
            for page in range(pages):
                url_feedback_by_page=url_feedback+f'p{page+1}/#comments'
                result = get_feedback(url_feedback_by_page,title)#手机名称/评论内容/评论时间
                result_end.extend(result)
        except OSError as reason:  # raise错误信息试试
            print('出错的原因:' + str(reason))

    return result_end


def to_mysql(result):
    connection=pymysql.connect(
        host='192.168.0.253',
        port=3306,
        user='root',
        password='Cacs@0201',
        db='smzdm'
    )
    cursor=connection.cursor()
    cursor.executemany(
        'insert into phone values(%s,%s,%s)',result
    )
    connection.commit()



def main():
    result = []
    url = 'https://www.smzdm.com/fenlei/zhinengshouji/h5c4s0f0t0p1/#feed-main'
    try:
        res = url_open(url)
        result=find_phone(res,10)  # 提取排名前十的物品
    except ConnectionError as reason:
        print(f'连接失败')

    to_mysql(result)
    print('爬取完毕。。。')

if __name__ == '__main__':
    main()