import requests
from bs4 import BeautifulSoup
import urllib
import time
import csv
import codecs
from 豆瓣爬虫 import expand


categories = ['剧情', '喜剧', '动作', '爱情', '科幻', '动画', '悬疑', '惊悚', '恐怖', '犯罪',
             '同性', '音乐', '歌舞', '传记', '历史', '战争', '西部', '奇幻', '冒险', '灾难', '武侠', '情色']

locations = ['中国大陆', '美国', '香港', '台湾', '日本', '韩国', '英国', '法国', '德国', '意大利', '西班牙'
             '印度', '泰国', '俄罗斯', '伊朗', '加拿大', '澳大利亚', '爱尔兰', '瑞典', '巴西', '丹麦']


def getMovieUrl(cate, loca):
    """get a string corresponding to the URL of douban movie lists given category and location."""
    url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影, {},{}'.format(cate, loca)
    return url


class Movies(object):
    """create the instance of movies"""
    def __init__(self, name, rate, cate, loca, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.cate = cate
        self.loca = loca
        self.info_link = info_link
        self.cover_link = cover_link

    def OutPut(self):
        out = [self.name, self.rate, self.cate, self.rate, self.info_link, self.cover_link]
        return out

def getMovies(category, locations):
    movies = []
    for i in locations:
        Html = expand.getHtml(getMovies(category, i), loadmore=True, waittime=2)
        soup = BeautifulSoup(Html, 'html.parser')
        TargetPage = soup.find(id='content').find(class_='list_wp').find_all('a', recursive=False)
        for element in TargetPage:
            M_name = element.find(class_='title').string
            M_rate = element.find(class_='rate').string
            M_location = i
            M_category = category
            M_info_link = element.get('href')
            M_cover_link = element.get('img').get('src')
            movies.append(Movies(M_name, M_rate, M_location, M_category, M_info_link, M_cover_link).OutPut())

    return movies

category_list = categories[:3]
Total_list = []
for category in category_list:
    temp = getMovies(category, locations)
    Total_list.append(temp)

class Finaly_count():
    def __init__(self, _list):
        self._list = _list

    def TopThreeeLoc(self):
        Count = []
        result = []
        


if __name__ == '__main__':
    with codecs.open('movies.csv', 'wb', 'utf-8_sig') as f:
        writer = csv.writer(f)
        for i in Total_list:
            writer.writerow(i)

