#!/usr/bin/env python3
import asyncio
import json
import praw

from bs4 import BeautifulSoup
from collections import Counter
from itertools import count
from selenium import webdriver
# from define import ADSENSE_MIDDLE


class ScrapAndPost:
    def __init__(self):
        pass

    def economy_hankyung(self, bp, keywords_list):
        result = ''
        cnt = 0
        urls = ['http://news.hankyung.com/economy/0401',
                'http://news.hankyung.com/economy/0402',
                'http://news.hankyung.com/economy/0403',
                'http://news.hankyung.com/economy/0404-0405',
                'http://news.hankyung.com/economy/0408',
                'http://news.hankyung.com/economy/0409',
                'http://news.hankyung.com/economy/0400']
        for url in urls:
            r = bp.request_and_get(url)
            if r is None:
                continue
            today = '%4d%02d%02d' % (bp.now.year, bp.now.month, bp.now.day)
            soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
            sessions = soup.select('div > h2 > a')
            for s in sessions:
                if s['href'] == 'http://www.hankyung.com/news/kisarank/':
                    continue
                href = s['href']
                title = bp.check_valid_string(s.text)
                article_date = href.split('/')[-1]
                if not article_date.startswith(today):
                    continue
                if cnt == 0:
                    result = '%s<br>📰 한국경제<br>' % result
                cnt += 1
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
                keywords = bp.get_news_article_info(href)
                keywords_list.extend(keywords)
        return result

    def economy_chosun(self, bp, keywords_list):
        result = ''
        cnt = 0
        r = bp.request_and_get('http://biz.chosun.com/svc/list_in/list.html?catid=2&gnb_marketlist')
        if r is None:
            return
        today = '%4d%02d%02d' % (bp.now.year, bp.now.month, bp.now.day)

        base_url = 'http://biz.chosun.com'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for f in soup.find_all(bp.match_soup_class(['list_vt'])):
            for li in f.find_all('li'):
                dt = li.find('dt')
                href = '%s%s' % (base_url, li.a['href'])
                title = bp.check_valid_string(dt.a.text)
                article_date = li.a['href'].split('/')[-1]
                if not article_date.startswith(today):
                    continue
                if cnt == 0:
                    result = '%s<br>📰 조선일보<br>' % result
                cnt += 1
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
                keywords = bp.get_news_article_info(href)
                keywords_list.extend(keywords)
        return result

    def economy_joins(self, bp, keywords_list):
        result = ''
        cnt = 0
        urls = ['https://news.joins.com/money/economy/list?cloc=joongang|article|subsection',
                'https://news.joins.com/money/finance/list?cloc=joongang|section|subsection',
                'https://news.joins.com/money/stock/list?cloc=joongang|section|subsection']
        for url in urls:
            r = bp.request_and_get(url)
            if r is None:
                continue
            today = '%4d.%02d.%02d' % (bp.now.year, bp.now.month, bp.now.day)

            base_url = 'http://realestate.joins.com'
            soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
            for list_basic in soup.find_all(bp.match_soup_class(['list_basic'])):
                for ul in list_basic.find_all('ul'):
                    for li in ul.find_all('li'):
                        title = li.find('span', attrs={'class': 'thumb'})
                        try:
                            temp_date = li.find('span', attrs={'class': 'byline'})
                            temp_date = temp_date.find_all('em')
                            article_date = temp_date[1].text.split()[0]
                            if article_date != today:
                                continue
                        except AttributeError:
                            continue
                        try:
                            title = title.img['alt']
                        except AttributeError:
                            continue
                        try:
                            temp = li.a['href']
                        except KeyError:
                            continue
                        href = '%s%s' % (base_url, temp)
                        if cnt == 0:
                            result = '%s<br>📰 중앙일보<br>' % result
                        cnt += 1
                        result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
                        keywords = bp.get_news_article_info(href)
                        keywords_list.extend(keywords)
        return result

    def economy_mbn(self, bp, keywords_list):
        result = ''
        cnt = 0
        urls = ['http://news.mk.co.kr/newsList.php?sc=30100033',
                'http://news.mk.co.kr/newsList.php?sc=30100034',
                'http://news.mk.co.kr/newsList.php?sc=30100035',
                'http://news.mk.co.kr/newsList.php?sc=30100036',
                'http://news.mk.co.kr/newsList.php?sc=30100037',
                'http://news.mk.co.kr/newsList.php?sc=30100038',
                'http://news.mk.co.kr/newsList.php?sc=30100039',
                'http://news.mk.co.kr/newsList.php?sc=30100040']
        for url in urls:
            r = bp.request_and_get(url)
            if r is None:
                continue
            today = '%4d.%02d.%02d' % (bp.now.year, bp.now.month, bp.now.day)

            soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
            for list_area in soup.find_all(bp.match_soup_class(['list_area'])):
                for dl in list_area.find_all('dl'):
                    dt = dl.find('dt')
                    href = dt.a['href']
                    title = bp.check_valid_string(dt.text)
                    article_date = dl.find('span', attrs={'class': 'date'}).text
                    if not article_date.startswith(today):
                        continue
                    if cnt == 0:
                        result = '%s<br>📰 매일경제<br>' % result
                    result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
                    cnt += 1
                    keywords = bp.get_news_article_info(href)
                    try:
                        keywords_list.extend(keywords)
                    except TypeError:
                        continue
        return result

    def economy_gyunghyang(self, bp, keywords_list):
        result = ''
        cnt = 0
        urls = ['http://biz.khan.co.kr/khan_art_list.html?category=economy',
                'http://biz.khan.co.kr/khan_art_list.html?category=finance',
                'http://biz.khan.co.kr/khan_art_list.html?category=industry',
                'http://biz.khan.co.kr/khan_art_list.html?category=company']
        for url in urls:
            r = bp.request_and_get(url)
            if r is None:
                continue
            today = '%4d. %02d. %02d' % (bp.now.year, bp.now.month, bp.now.day)

            soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
            for news_list in soup.find_all(bp.match_soup_class(['news_list'])):
                for li in news_list.find_all('li'):
                    try:
                        article_date = li.find('em', attrs={'class': 'letter'}).text
                        if not article_date.startswith(today):
                            continue
                        if cnt == 0:
                            result = '%s<br>📰 경향신문<br>' % result
                        cnt += 1
                        title = li.find('strong', attrs={'class': 'hd_title'})
                        result = '%s<br><a href="%s" target="_blank">%s</a>' % (
                                 result, title.a['href'], title.text)
                        keywords = bp.get_news_article_info(title.a['href'])
                        keywords_list.extend(keywords)
                    except TypeError:
                        continue
            return result

    def economy_thebell(self, bp, keywords_list):
        result = ''
        driver = webdriver.Chrome(bp.chromedriver_path)
        base_url = 'https://www.thebell.co.kr/free/content'
        cnt = 0
        today = '%4d-%02d-%02d' % (bp.now.year, bp.now.month, bp.now.day)
        for i in range(1, 15):  # 무한으로 돌리니 한도끝도 없이 돌아서
            driver.implicitly_wait(3)
            url = 'https://www.thebell.co.kr/free/content/article.asp?page=%d&svccode=00' % i
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            for list_box in soup.find_all(bp.match_soup_class(['listBox'])):
                for dl in list_box.find_all('dl'):
                    for idx, dd in enumerate(dl.find_all('dd')):
                        if idx == 1:
                            article_date = dd.find('span', attrs={'class': 'date'}).text
                            break
                    if article_date is None:
                        continue
                    if not article_date.startswith(today):
                        continue
                    dt = dl.find('dt')
                    title = dt.text
                    if cnt == 0:
                        result = '%s<br>📰 the bell<br>' % result
                    cnt += 1
                    href = '%s/%s' % (base_url, dl.a['href'])
                    result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
                    keywords = bp.get_news_article_info(href)
                    keywords_list.extend(keywords)
        driver.quit()
        return result

    def economy_thescoop(self, bp, keywords_list):
        result = ''
        cnt = 0
        base_url = 'http://www.thescoop.co.kr'
        urls = ['S1N7', 'S2N10', 'S2N29', 'S2N30', 'S2N52', 'S2N59', 'S2N69',
                'S2N78', 'S2N70', 'S2N72', 'S2N75', 'S2N76', 'S2N77',
                'S2N98', 'S2N99', 'S2N101', 'S2N110', ]
        today = '%4d-%02d-%02d' % (bp.now.year, bp.now.month, bp.now.day)
        driver = webdriver.Chrome(bp.chromedriver_path)
        for u in urls:
            url = 'http://www.thescoop.co.kr/news/articleList.html?page=1&total=221&sc_section_code=&sc_sub_section_code=%s&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&view_type=sm' % u
            driver.implicitly_wait(3)
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            for article_list in soup.find_all(bp.match_soup_class(['article-list-content'])):
                for blocks in article_list.find_all(bp.match_soup_class(['list-block'])):
                    for dated in blocks.find_all(bp.match_soup_class(['list-dated'])):
                        article_date = dated.text.split('|')[2].strip()
                        break
                    if not article_date.startswith(today):
                        continue
                    for titles in blocks.find_all(bp.match_soup_class(['list-titles'])):
                        if cnt == 0:
                            result = '%s<br>📰 the belscoop<br>' % result
                        cnt += 1
                        href = '%s%s' % (base_url, titles.a['href'])
                        result = '%s<br><a href="%s" target="_blank">%s</a>' % (
                                 result, href, titles.a.text)
                        keywords = bp.get_news_article_info(href)
                        keywords_list.extend(keywords)
        driver.quit()
        return result

    def economy_sedaily(self, bp, keywords_list):
        result = ''
        urls = ['http://www.sedaily.com/NewsList/GC01',   # 경제 동향
                'http://www.sedaily.com/NewsList/GC02',
                'http://www.sedaily.com/NewsList/GC03',
                'http://www.sedaily.com/NewsList/GC04',
                'http://www.sedaily.com/NewsList/GC05',
                'http://www.sedaily.com/NewsList/GC06',
                'http://www.sedaily.com/NewsList/GC07',
                'http://www.sedaily.com/NewsList/GC08',
                'http://www.sedaily.com/NewsList/GC09',
                'http://www.sedaily.com/NewsList/GC10',
                'http://www.sedaily.com/NewsList/GC11',
                'http://www.sedaily.com/NewsList/GC12',
                'http://www.sedaily.com/NewsList/GC13',
                ]

        base_url = 'http://www.sedaily.com'
        today = '%4d-%02d-%02d' % (bp.now.year, bp.now.month, bp.now.day)
        cnt = 0
        for url in urls:
            r = bp.request_and_get(url)
            soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
            for news_list in soup.find_all(bp.match_soup_class(['news_list'])):
                for li in news_list.find_all('li'):
                    dt = li.find('dt')
                    href = '%s%s' % (base_url, dt.a['href'])
                    dd = li.find('dd')
                    article_date = dd.find('span', attrs={'class': 'letter'}).text
                    if not article_date.startswith(today):
                        continue
                    if cnt == 0:
                        result = '%s<br>📰 서울경제<br>' % result
                    cnt += 1
                    result = '%s<br><a href="%s" target="_blank">%s</a>' % (
                             result, href, dt.text)
                    keywords = bp.get_news_article_info(href)
                    keywords_list.extend(keywords)
        return result

    def economy_cnews(self, bp, keywords_list):
        result = ''
        base_url = 'http://www.cnews.co.kr/uhtml/read.jsp?idxno='
        today = '%4d%02d%02d' % (bp.now.year, bp.now.month, bp.now.day)
        cnt = 0
        urls = ['http://www.cnews.co.kr/uhtml/autosec/S1N2_S2N17_1.html',  # 경제정책
                'http://www.cnews.co.kr/uhtml/autosec/S1N2_S2N18_1.html',  # 금융
                'http://www.cnews.co.kr/uhtml/autosec/S1N2_S2N19_1.html',  # 기업
                'http://www.cnews.co.kr/uhtml/autosec/S1N2_S2N20_1.html',  # 증권
                'http://www.cnews.co.kr/uhtml/autosec/S1N2_S2N21_1.html',  # 비즈
                ]
        for url in urls:
            r = bp.request_and_get(url)
            soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
            for sub_list in soup.find_all(bp.match_soup_class(['sub_main_news_list_2'])):
                for li in sub_list.find_all('li'):
                    title = li.find('div', {'class': 'title'})
                    article_date = li.a['href'].split("'")[1]
                    if not article_date.startswith(today):
                        continue
                    if cnt == 0:
                        result = '%s<br>📰 건설경제<br>' % result
                    cnt += 1
                    href = '%s%s' % (base_url, article_date)
                    result = '%s<br><a href="%s" target="_blank">%s</a>' % (
                             result, href, title.text)
                    keywords = bp.get_news_article_info(href)
                    keywords_list.extend(keywords)
        return result

    def economy_yonhapnews(self, bp, keywords_list):
        result = ''
        cnt = 0
        urls = ['http://www.yonhapnews.co.kr/economy/0301000001.html',
                'http://www.yonhapnews.co.kr/economy/0302000001.html']
        for url in urls:
            r = bp.request_and_get(url)
            if r is None:
                continue
            today = '%4d/%02d/%02d' % (bp.now.year, bp.now.month, bp.now.day)

            soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
            for sect02 in soup.find_all(bp.match_soup_class(['section02'])):
                for div in sect02.find_all('div'):
                    href = div.a['href']
                    urls = div.a['href'].split('/')
                    article_date = '/'.join(urls[4:7])
                    if not article_date.startswith(today):
                        continue
                    if cnt == 0:
                        result = '%s<br>📰 연합뉴스<br>' % result
                    cnt += 1
                    result = '%s<br><a href="%s" target="_blank">%s</a>' % (
                             result, href, div.a.text)
                    keywords = bp.get_news_article_info(href)
                    keywords_list.extend(keywords)
        return result

    def realestate_molit(self, bp, keywords_list):
        result = ''
        cnt = 0
        r = bp.request_and_get('http://www.molit.go.kr/USR/NEWS/m_71/lst.jsp')
        if r is None:
            return
        today = '%4d-%02d-%02d' % (bp.now.year, bp.now.month, bp.now.day)
        soup = BeautifulSoup(r.text, 'html.parser')
        for tbody in soup.find_all('tbody'):
            for tr in tbody.find_all('tr'):
                for idx, td in enumerate(tr.find_all('td')):
                    if idx == 3:
                        article_date = td.text
                        break
                try:
                    tr.a['href']
                except TypeError:
                    continue

                if not article_date.startswith(today):
                    continue
                if cnt == 0:
                    result = '%s<br>📰 국토교통부 보도자료<br>' % result
                cnt += 1
                href = 'http://www.molit.go.kr/USR/NEWS/m_71/%s' % tr.a['href']
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (
                         result, href, tr.a.text.strip())
                keywords = bp.get_news_article_info(href)
                keywords_list.extend(keywords)
        return result

    def realestate_yonhapnews(self, bp, keywords_list):
        result = ''
        cnt = 0
        r = bp.request_and_get('http://www.yonhapnews.co.kr/economy/0304000001.html')
        if r is None:
            return
        today = '%4d/%02d/%02d' % (bp.now.year, bp.now.month, bp.now.day)

        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for sect02 in soup.find_all(bp.match_soup_class(['section02'])):
            for div in sect02.find_all('div'):
                href = div.a['href']
                urls = div.a['href'].split('/')
                article_date = '/'.join(urls[4:7])
                if not article_date.startswith(today):
                    continue
                if cnt == 0:
                    result = '%s<br>📰 연합뉴스<br>' % result
                cnt += 1
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (
                         result, href, div.a.text)
                keywords = bp.get_news_article_info(href)
                keywords_list.extend(keywords)
        return result

    def realestate_cnews(self, bp, keywords_list):
        result = ''
        base_url = 'http://www.cnews.co.kr/uhtml/read.jsp?idxno='
        today = '%4d%02d%02d' % (bp.now.year, bp.now.month, bp.now.day)
        cnt = 0
        urls = ['http://www.cnews.co.kr/uhtml/autosec/S1N1_S2N12_1.html',  # 분양
                'http://www.cnews.co.kr/uhtml/autosec/S1N1_S2N13_1.html',  # 도시정비
                'http://www.cnews.co.kr/uhtml/autosec/S1N1_S2N14_1.html',  # 개발
                'http://www.cnews.co.kr/uhtml/autosec/S1N1_S2N15_1.html',  # 재태크
                'http://www.cnews.co.kr/uhtml/autosec/S1N1_S2N16_1.html',  # 부동산시장
                ]
        for url in urls:
            r = bp.request_and_get(url)
            soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
            for sub_list in soup.find_all(bp.match_soup_class(['sub_main_news_list_2'])):
                for li in sub_list.find_all('li'):
                    title = li.find('div', {'class': 'title'})
                    article_date = li.a['href'].split("'")[1]
                    if not article_date.startswith(today):
                        continue
                    if cnt == 0:
                        result = '%s<br>📰 건설경제<br>' % result
                    cnt += 1
                    href = '%s%s' % (base_url, article_date)
                    result = '%s<br><a href="%s" target="_blank">%s</a>' % (
                             result, href, title.text)
                    keywords = bp.get_news_article_info(href)
                    keywords_list.extend(keywords)
        return result

    def realestate_sedaily(self, bp, keywords_list):
        result = ''
        urls = ['http://www.sedaily.com/NewsList/GB01',   # 정책, 제도
                'http://www.sedaily.com/NewsList/GB02',   # 분양, 청약
                'http://www.sedaily.com/NewsList/GB03',   # 아파트, 주택
                'http://www.sedaily.com/NewsList/GB04',   # 오피스, 상가, 토지
                'http://www.sedaily.com/NewsList/GB05',   # 건설업계
                'http://www.sedaily.com/NewsList/GB06',   # 간접투자
                'http://www.sedaily.com/NewsList/GB07',   # 기획연재
                ]

        base_url = 'http://www.sedaily.com'
        today = '%4d-%02d-%02d' % (bp.now.year, bp.now.month, bp.now.day)
        cnt = 0
        for url in urls:
            r = bp.request_and_get(url)
            soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
            for news_list in soup.find_all(bp.match_soup_class(['news_list'])):
                for li in news_list.find_all('li'):
                    dt = li.find('dt')
                    href = '%s%s' % (base_url, dt.a['href'])
                    dd = li.find('dd')
                    article_date = dd.find('span', attrs={'class': 'letter'}).text
                    if not article_date.startswith(today):
                        continue
                    if cnt == 0:
                        result = '%s<br>📰 서울경제<br>' % result
                    cnt += 1
                    result = '%s<br><a href="%s" target="_blank">%s</a>' % (
                             result, href, dt.text)
                    keywords = bp.get_news_article_info(href)
                    keywords_list.extend(keywords)
        return result

    def realestate_gyunghyang(self, bp, keywords_list):
        result = ''
        cnt = 0
        r = bp.request_and_get('http://biz.khan.co.kr/khan_art_list.html?category=realty')
        if r is None:
            return
        today = '%4d. %02d. %02d' % (bp.now.year, bp.now.month, bp.now.day)

        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        for news_list in soup.find_all(bp.match_soup_class(['news_list'])):
            for li in news_list.find_all('li'):
                try:
                    article_date = li.find('em', attrs={'class': 'letter'}).text
                    if not article_date.startswith(today):
                        continue
                    if cnt == 0:
                        result = '%s<br>📰 경향신문<br>' % result
                    cnt += 1
                    title = li.find('strong', attrs={'class': 'hd_title'})
                    result = '%s<br><a href="%s" target="_blank">%s</a>' % (
                             result, title.a['href'], title.text)
                    keywords = bp.get_news_article_info(title.a['href'])
                    keywords_list.extend(keywords)
                except TypeError:
                    continue
        return result

    def realestate_kookmin(self, bp, keywords_list):
        result = ''
        cnt = 0
        r = bp.request_and_get('http://news.kmib.co.kr/article/list.asp?sid1=eco')
        if r is None:
            return
        today = '%4d-%02d-%02d' % (bp.now.year, bp.now.month, bp.now.day)

        base_url = 'http://news.kmib.co.kr/article'
        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        cnt = 0
        for nws_list in soup.find_all(bp.match_soup_class(['nws_list'])):
            for dl in nws_list.find_all('dl'):
                article_date = dl.find('dd', attrs={'class': 'date'}).text
                if not article_date.startswith(today):
                    continue
                if dl.text == '등록된 기사가 없습니다.':
                    return
                dt = dl.find('dt')
                href = '%s/%s' % (base_url, dt.a['href'])
                title = bp.check_valid_string(dt.a.text)
                if (title.find('아파트') != -1 or
                   title.find('국토부') != -1 or title.find('국토교통부') != -1 or
                   title.find('전세') != -1 or title.find('전월세') != -1 or
                   title.find('청약') != -1 or title.find('분양') != -1 or
                   title.find('부동산') != -1):

                    if cnt == 0:
                        result = '%s<br>📰 국민일보<br>' % result
                    result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
                    keywords = bp.get_news_article_info(href)
                    keywords_list.extend(keywords)
                    cnt += 1
        return result

    def realestate_nocut(self, bp, keywords_list):
        result = ''
        cnt = 0
        r = bp.request_and_get('http://www.nocutnews.co.kr/news/list?c1=203&c2=204&ltype=1')
        if r is None:
            return
        today = '%4d-%02d-%02d' % (bp.now.year, bp.now.month, bp.now.day)

        base_url = 'http://www.nocutnews.co.kr'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        news = soup.find(bp.match_soup_class(['newslist']))
        for dl in news.find_all('dl'):
            dt = dl.find('dt')
            href = '%s%s' % (base_url, dt.a['href'])
            title = bp.check_valid_string(dt.text)
            temp = (dl.find('dd', attrs={'class': 'txt'}).text).split(' ')
            article_date = ''.join(temp[-3:])
            if not article_date.startswith(today):
                continue
            if cnt == 0:
                result = '%s<br>📰 노컷뉴스<br>' % result
            cnt += 1
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
            keywords = bp.get_news_article_info(href)
            keywords_list.extend(keywords)
        return result

    def realestate_donga(self, bp, keywords_list):
        result = ''
        cnt = 0
        r = bp.request_and_get('http://news.donga.com/List/Economy/RE')
        if r is None:
            return
        today = '%4d%02d%02d' % (bp.now.year, bp.now.month, bp.now.day)

        soup = BeautifulSoup(r.text, 'html.parser')
        for alist in soup.find_all(bp.match_soup_class(['articleList'])):
            tit = alist.find('span', attrs={'class': 'tit'})
            title = bp.check_valid_string(tit.text)
            temp = (alist.a['href']).split('/')
            article_date = temp[-3]
            if not article_date.startswith(today):
                continue
            if cnt == 0:
                result = '%s<br>📰 동아일보<br>' % result
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, alist.a['href'], title)
            keywords = bp.get_news_article_info(alist.a['href'])
            keywords_list.extend(keywords)
            cnt += 1
        return result

    def realestate_mbn(self, bp, keywords_list):
        result = ''
        cnt = 0
        r = bp.request_and_get('http://news.mk.co.kr/newsList.php?sc=30000020')
        if r is None:
            return
        today = '%4d.%02d.%02d' % (bp.now.year, bp.now.month, bp.now.day)

        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        for list_area in soup.find_all(bp.match_soup_class(['list_area'])):
            for dl in list_area.find_all('dl'):
                dt = dl.find('dt')
                href = dt.a['href']
                title = bp.check_valid_string(dt.text)
                article_date = dl.find('span', attrs={'class': 'date'}).text
                if not article_date.startswith(today):
                    continue
                if cnt == 0:
                    result = '%s<br>📰 매일경제<br>' % result
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
                cnt += 1
                keywords = bp.get_news_article_info(href)
                try:
                    keywords_list.extend(keywords)
                except TypeError:
                    continue
        return result

    def realestate_moonhwa(self, bp, keywords_list):
        result = ''
        cnt = 0
        r = bp.request_and_get('http://www.munhwa.com/news/section_list.html?sec=economy&class=5')
        if r is None:
            return
        today = '%4d.%02d.%02d' % (bp.now.year, bp.now.month, bp.now.day)
        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        for td in soup.find_all('td', attrs={'style': 'padding:4 0 0 3'}):
            articles = td.text.split()
            article_date = articles[-1].replace(']', '').replace('[', '')
            if not article_date.startswith(today):
                continue
            if cnt == 0:
                result = '%s<br>📰 문화일보<br>' % result
            cnt += 1
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (
                     result, td.a['href'], ' '.join(articles[:-1]))
            keywords = bp.get_news_article_info(td.a['href'])
            keywords_list.extend(keywords)
        return result

    def realestate_segye(self, bp, keywords_list):
        result = ''
        cnt = 0
        r = bp.request_and_get('http://www.segye.com/newsList/0101030700000')
        if r is None:
            return
        today = '%4d%02d%02d' % (bp.now.year, bp.now.month, bp.now.day)
        base_url = 'http://www.segye.com'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for r_txt in soup.find_all(bp.match_soup_class(['r_txt'])):
            for dt in r_txt.find_all('dt'):
                href = '%s%s' % (base_url, dt.a['href'])
                title = dt.text
                article_date = dt.a['href'].split('/')[-1]
                if not article_date.startswith(today):
                    continue
                if cnt == 0:
                    result = '%s<br>📰 세계일보<br>' % result
                cnt += 1
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
                keywords = bp.get_news_article_info(href)
                keywords_list.extend(keywords)
        return result

    def realestate_joins(self, bp, keywords_list):
        result = ''
        cnt = 0
        r = bp.request_and_get('http://realestate.joins.com/article/')
        if r is None:
            return
        today = '%4d.%02d.%02d' % (bp.now.year, bp.now.month, bp.now.day)

        base_url = 'http://realestate.joins.com'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for list_basic in soup.find_all(bp.match_soup_class(['list_basic'])):
            for ul in list_basic.find_all('ul'):
                for li in ul.find_all('li'):
                    title = li.find('span', attrs={'class': 'thumb'})
                    try:
                        temp_date = li.find('span', attrs={'class': 'byline'})
                        temp_date = temp_date.find_all('em')
                        article_date = temp_date[1].text.split()[0]
                        if article_date != today:
                            continue
                    except AttributeError:
                        continue
                    try:
                        title = title.img['alt']
                    except AttributeError:
                        continue
                    try:
                        temp = li.a['href']
                    except KeyError:
                        continue
                    href = '%s%s' % (base_url, temp)
                    if cnt == 0:
                        result = '%s<br>📰 중앙일보<br>' % result
                    cnt += 1
                    result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
                    keywords = bp.get_news_article_info(href)
                    keywords_list.extend(keywords)
        return result

    def realestate_chosun(self, bp, keywords_list):
        result = ''
        cnt = 0
        r = bp.request_and_get('http://biz.chosun.com/svc/list_in/list.html?catid=4&gnb_global')
        if r is None:
            return
        today = '%4d%02d%02d' % (bp.now.year, bp.now.month, bp.now.day)

        base_url = 'http://biz.chosun.com'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for f in soup.find_all(bp.match_soup_class(['list_vt'])):
            for li in f.find_all('li'):
                dt = li.find('dt')
                href = '%s%s' % (base_url, li.a['href'])
                title = bp.check_valid_string(dt.a.text)
                article_date = li.a['href'].split('/')[-1]
                if not article_date.startswith(today):
                    continue
                if cnt == 0:
                    result = '%s<br>📰 조선일보<br>' % result
                cnt += 1
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
                keywords = bp.get_news_article_info(href)
                keywords_list.extend(keywords)
        return result

    def realestate_hani(self, bp, keywords_list):
        result = ''
        cnt = 0
        r = bp.request_and_get(' http://www.hani.co.kr/arti/economy/property/home01.html')
        if r is None:
            return
        today = '%4d-%02d-%02d' % (bp.now.year, bp.now.month, bp.now.day)

        base_url = 'http://www.hani.co.kr'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for article in soup.find_all(bp.match_soup_class(['article-area'])):
            article_date = article.find('span', attrs={'class': 'date'}).text
            href = '%s%s' % (base_url, article.a['href'])
            article = article.text.strip().split('\n')
            title = bp.check_valid_string(article[0])
            if not article_date.startswith(today):
                continue
            if cnt == 0:
                result = '%s<br>📰 한겨례신문<br>' % result
            cnt += 1
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
            keywords = bp.get_news_article_info(href)
            keywords_list.extend(keywords)
        return result

    def realestate_hankyung(self, bp, keywords_list):
        result = ''
        cnt = 0
        r = bp.request_and_get('http://land.hankyung.com/')
        if r is None:
            return
        today = '%4d%02d%02d' % (bp.now.year, bp.now.month, bp.now.day)
        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        sessions = soup.select('div > h2 > a')
        for s in sessions:
            if s['href'] == 'http://www.hankyung.com/news/kisarank/':
                continue
            href = s['href']
            title = bp.check_valid_string(s.text)
            article_date = href.split('/')[-1]
            if not article_date.startswith(today):
                continue
            if cnt == 0:
                result = '%s<br>📰 한국경제<br>' % result
            cnt += 1
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
            keywords = bp.get_news_article_info(href)
            keywords_list.extend(keywords)
        return result

    def realestate_naver(self, bp, keywords_list):
        result = ''
        r = bp.request_and_get('http://land.naver.com/news/headline.nhn')
        if r is None:
            return
        result = '%s<br>📰 Naver<br>' % result

        base_url = 'http://land.naver.com'
        soup = BeautifulSoup(r.text, 'html.parser')
        sessions = soup.select('div > div > div > div > div > dl > dt > a')
        for s in sessions:
            href = '%s%s' % (base_url, s['href'])
            title = bp.check_valid_string(s.text)
            keywords = bp.get_news_article_info(href)
            keywords_list.extend(keywords)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)

        sessions = soup.select('div > ul > li > dl > dt > a')
        for s in sessions:
            if len(s.text) == 0:
                continue
            href = '%s%s' % (base_url, s['href'])
            title = bp.check_valid_string(s.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
            keywords = bp.get_news_article_info(href)
            keywords_list.extend(keywords)
        return result

    def realestate_nate(self, bp, keywords_list):
        result = ''
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t0014" id="t0014" href="#t0014" class="invisible"> </a><font color="blue">[네이트 부동산 뉴스]</font><br>'
        url = 'http://news.nate.com/subsection?cate=eco03&mid=n0303&type=c&date=%s&page=1' % bp.today
        r = bp.request_and_get(url)
        if r is None:
            result = '%s<br>No article.' % result
            return result

        soup = BeautifulSoup(r.text, 'html.parser')
        for news in soup.find_all(bp.match_soup_class(['mlt01'])):
            span = news.find('span', attrs={'class': 'tb'})
            tit = span.find('strong', attrs={'class': 'tit'})
            title = bp.check_valid_string(tit.text)
            keywords = bp.get_news_article_info(news.a['href'])
            keywords_list.extend(keywords)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, news.a['href'], title)
        return result

    def realestate_daum(self, bp, keywords_list):
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t0015" id="t0015" href="#t0015" class="invisible"> </a><font color="blue">[Daum 부동산 뉴스]</font><br>'
        r = bp.request_and_get('http://realestate.daum.net/news')
        soup = BeautifulSoup(r.text, 'html.parser')
        for f in soup.find_all(bp.match_soup_class(['link_news'])):
            try:
                href = f['href']
            except TypeError:
                continue
            title = bp.check_valid_string(f.text)
            keywords = bp.get_news_article_info(href)
            keywords_list.extend(keywords)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def koreagov_news(self, bp):
        news_cnt = 0
        base_url1 = 'http://www.korea.kr/policy/mainView.do?'
        base_url2 = 'http://www.korea.kr/policy/policyPhotoView.do?'
        result = '<font color="blue">[한국 정책 뉴스]</font><br>'
        for i in range(1, 5):  # maybe 1~3 pages per a day
            url = 'http://www.korea.kr/policy/mainList.do?pageIndex=%d&srchRepCodeType=&repCodeType=&repCode=&startDate=%4d-%02d-%02d&endDate=%4d-%02d-%02d&srchWord=#goView' % (
                  i,
                  bp.now.year, bp.now.month, bp.now.day,
                  bp.now.year, bp.now.month, bp.now.day)
            r = bp.request_and_get(url)
            if r is None:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            for thumb in soup.find_all(bp.match_soup_class(['thumb'])):
                try:
                    conn_url = thumb.a['onclick'].split("'")[1]
                except TypeError:
                    continue
                except KeyError:
                    continue

                if conn_url.startswith('newsId='):
                    href = '%s%s' % (base_url1, conn_url)
                else:
                    href = '%s%s' % (base_url2, conn_url)

                img = thumb.find('img')
                title = bp.check_valid_string(img['alt'])
                result = '%s<br><a href="%s" target="_blank">- %s</a>' % (result, href, title)
                news_cnt += 1
        if news_cnt == 0:
            result = '%s<br>No article.' % result
        return result

    def financial_einfomax(self, bp):
        result = '<font color="blue">[연합인포맥스 경제 뉴스]</font><br>'
        r = bp.request_and_get('http://news.einfomax.co.kr/news/articleList.html?sc_section_code=S1N16&view_type=sm')
        if r is None:
            result = '%s<br>No article.' % result
            return result

        base_url = 'http://news.einfomax.co.kr/news'
        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        for f in soup.find_all(bp.match_soup_class(['ArtList_Title'])):
            try:
                href = '%s/%s' % (base_url, f.a['href'])
            except TypeError:
                continue
            title = bp.check_valid_string(f.a.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def financial_chosun(self, bp):
        result = '<font color="blue">[조선일보 경제 뉴스]</font><br>'
        r = bp.request_and_get('http://biz.chosun.com/index.html')
        if r is None:
            result = '%s<br>No article.' % result
            return result

        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for f in soup.find_all(bp.match_soup_class(['mc_art_lst'])):
            for li in f.find_all('li'):
                if li.a['href'].endswith('main_hot3'):  # 경제, 금융: main_hot1, main_hot2
                    break
                try:
                    href = li.a['href']
                except TypeError:
                    continue
                title = bp.check_valid_string(li.a.text)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def realestate_thebell(self, bp, keywords_list):
        result = ''
        driver = webdriver.Chrome(bp.chromedriver_path)
        base_url = 'https://www.thebell.co.kr/free/content'
        cnt = 0
        today = '%4d-%02d-%02d' % (bp.now.year, bp.now.month, bp.now.day)
        for i in count(1):
            driver.implicitly_wait(3)
            url = 'https://www.thebell.co.kr/free/content/article.asp?page=%d&svccode=00' % i
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            for list_box in soup.find_all(bp.match_soup_class(['listBox'])):
                for dl in list_box.find_all('dl'):
                    for idx, dd in enumerate(dl.find_all('dd')):
                        if idx == 1:
                            article_date = dd.find('span', attrs={'class': 'date'}).text
                            break
                    if article_date is None:
                        continue
                    if not article_date.startswith(today):
                        driver.quit()
                        return
                    dt = dl.find('dt')
                    title = dt.text
                    if (title.find('부동산') == -1 and
                       title.find('청약') == -1 and
                       title.find('재건축') == -1 and
                       title.find('집값') == -1 and
                       title.find('아파트') == -1):
                        # ignore not realestate title
                        continue
                    if cnt == 0:
                        result = '%s<br>📰 the bell<br>' % result
                    cnt += 1
                    href = '%s/%s' % (base_url, dl.a['href'])
                    result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
                    keywords = bp.get_news_article_info(href)
                    keywords_list.extend(keywords)
        driver.quit()
        return result

    def financial_joins(self, bp):
        result = '<font color="blue">[중앙일보 경제 뉴스]</font><br>'
        r = bp.request_and_get('http://news.joins.com/money?cloc=joongang|home|section3')
        if r is None:
            result = '%s<br>No article.' % result
            return result

        base_url = 'http://news.joins.com'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for f in soup.find_all(bp.match_soup_class(['default_realtime'])):
            for li in f.find_all('li'):
                try:
                    href = '%s%s' % (base_url, li.a['href'])
                except TypeError:
                    continue
                title = bp.check_valid_string(' '.join(li.text.strip().split()[1:-2]))
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def reddit_news(self, bp, category):
        reddit = praw.Reddit(client_id=bp.reddit_cid,
                             client_secret=bp.reddit_csec, password=bp.reddit_pw,
                             user_agent='USERAGENT', username=bp.reddit_id)

        if category == 'programming':
            result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t1001" id="t1001" href="#t1001" class="invisible"> </a><font color="red">[레딧(Reddit) Programming]</font><br>'
        elif category == 'todayilearned':
            result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t1002" id="t1002" href="#t1002" class="invisible"> </a><font color="red">[레딧(Reddit) 오늘 배운거]</font><br>'
        elif category == 'worldnews':
            result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t1003" id="t1003" href="#t1003" class="invisible"> </a><font color="red">[레딧(Reddit) 세계뉴스]</font><br>'
        elif category == 'Futurology':
            result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t1004" id="t1004" href="#t1004" class="invisible"> </a><font color="red">[레딧(Reddit) 미래기술]</font><br>'
        elif category == 'announcements':
            result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t1005" id="t1005" href="#t1005" class="invisible"> </a><font color="red">[레딧(Reddit) 발표, 소식]</font><br>'
        else:
            result = 'Unknown category<br>'
            return result

        temp = []
        for idx, sub in enumerate(reddit.subreddit(category).hot(limit=20)):
            result = '%s<br>[%d](⬆ %s)  <a href="%s" target="_blank">%s</a><br>' % (result, idx + 1, sub.score, sub.url, sub.title)
            # title = bp.translate_text(sub.title)
            title = sub.title
            if title is None:
                title = sub.title
            ko_text = '[%d] <a href="%s" target="_blank">%s</a><br>' % (idx + 1, sub.url, title)
            temp.append(ko_text)
        result = '%s<br><br><pre>%s</pre>' % (result, ''.join(temp))
        return result

    def hacker_news(self, bp):
        result = ''
        # p=1, rank 1~30, p=2, rank 30~60 ...
        for i in range(1, 2):
            url = 'https://news.ycombinator.com/news?p=%d' % i
            r = bp.request_and_get(url)
            if r is None:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            for f in soup.find_all(bp.match_soup_class(['athing'])):
                title = bp.check_valid_string(f.text)
                for s in f.find_all(bp.match_soup_class(['storylink'])):
                    href = s['href']
                    temp = '<a href="%s" target="_blank">%s</a><br><pre>%s</pre><br>' % (href, title, bp.naver_papago_nmt(title))
                    result = '%s<br>%s' % (result, temp)
        content = '<font color="red">[해커뉴스(Hacker News)]</font>%s<br>' % result
        return content

    def financial_news(self, bp):  # Pending
        result = ''

        content = self.financial_donga(bp, '경제')  # 동아일보
        result = '%s<br><br><br>%s' % (result, content)
        content = self.financial_einfomax(bp)
        result = '%s<br><br><br>%s' % (result, content)
        content = self.financial_chosun(bp)
        result = '%s<br><br><br>%s' % (result, content)
        content = self.financial_joins(bp)
        result = '%s<br><br><br>%s' % (result, content)

        return result

    def aladin_book(self, bp, query_type='ItemNewAll', max_result=30):  # max 50
        url = 'http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey=%s&QueryType=%s&MaxResults=%d&start=1&SearchTarget=Book&output=js&Cover=big&Version=20131101' % (bp.aladin_key, query_type, max_result)

        r = bp.request_and_get(url)
        if r is None:
            return
        content = ''
        soup = BeautifulSoup(r.text, 'html.parser')
        books = json.loads(str(soup))

        for book in books['item']:
            title = book['title']
            link = book['link']
            desc = book['description']
            img_link = book['cover']
            publisher = book['publisher']
            priceSales = book['priceSales']
            # priceStandard = book['priceStandard']
            categoryName = book['categoryName']
            author = book['author']

            temp = '<a href="%s" target="_blank"><font color="red">%s</font></a><br>%s, %s, %s 원<br>%s<br><br>%s<br><br><center><a href="%s" target="_blank"> <img border="0" align="middle" src="%s" width="200" height="250"></a></center>' % (link, title, author, publisher, priceSales, categoryName, desc, link, img_link)
            content = '%s<br><br>%s' % (content, temp)

        if query_type == 'ItemNewSpecial':
            title = '[%s] 주목할 만한 신간 리스트 - 국내도서 20권(알라딘)' % bp.today
        elif query_type == 'Bestseller':
            title = '[%s] 베스트셀러 - 20권(알라딘)' % bp.today
        elif query_type == 'ItemNewAll':
            title = '[%s] 전체 신간 리스트 20권(알라딘)' % bp.today
        elif query_type == 'BlogBest':
            title = '[%s] 서재 블로그 이용자의 북플 베스트 20권(알라딘)' % bp.today

        bp.tistory_post('scrapnpost', title, content, '765395')
        return

    def kdi_research(self, bp):  # 한국개발연구원
        thema = {'A': '거시/금융',
                 'B': '재정/복지',
                 'C': '노동/교육',
                 'D': '국제/무역',
                 'E': '산업조직',
                 'F': '경제발전/성장',
                 'G': '북한경제/경제체계',
                 'H': '농업/환경/자원',
                 'I': '지역경제',
                 'J': '기타'}

        result = ''
        base_url = 'http://www.kdi.re.kr'
        for t, value in thema.items():
            result = '%s<br><br><strong><font color="red">[%s]</font></strong>' % (result, value)
            url = 'http://www.kdi.re.kr/research/subjects_list.jsp?tema=%s' % t
            r = bp.request_and_get(url)
            if r is None:
                return
            soup = BeautifulSoup(r.text, 'html.parser')
            sessions = soup.select('li > div > a')
            for s in sessions:
                result_url = '%s%s' % (base_url, s['href'])
                title = bp.check_valid_string(s.text)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, result_url, title)
        return result

    def domestic_exhibition(self, bp):
        result = ''

        content = self.coex_exhibition(bp)
        result = '%s<br><br><br>%s' % (result, content)
        content = self.sacticket(bp)
        result = '%s<br><br><br>%s' % (result, content)

        return result

    def opinion_hani(self, bp, keywords_list):
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t0010" id="t0010" href="#t0010" class="invisible"> </a><font color="blue">[한겨례 사설, 칼럼]</font>'
        r = bp.request_and_get('http://www.hani.co.kr/arti/opinion/home01.html?_fr=mt0')
        if r is None:
            result = '%s<br>No article.' % result
            return result

        base_url = 'http://www.hani.co.kr'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for article in soup.find_all(bp.match_soup_class(['article'])):
            for li in article.find_all('li'):
                li_href = '%s%s' % (base_url, li.a['href'])
                li_text = li.text.strip().split('\n')
                title = bp.check_valid_string(li_text[0])
                keywords = bp.get_news_article_info(li_href)
                keywords_list.extend(keywords)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, li_href, title)
            href = '%s%s' % (base_url, article.a['href'])
            article = article.text.strip().split('\n')
            title = bp.check_valid_string(article[0])
            keywords = bp.get_news_article_info(href)
            keywords_list.extend(keywords)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def opinion_donga(self, bp, keywords_list):
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t0004" id="t0004" href="#t0004" class="invisible"> </a><font color="blue">[동아일보 오피니언]</font>'
        r = bp.request_and_get('http://news.donga.com/Column/')
        if r is None:
            result = '%s<br>No article.' % result
            return result

        soup = BeautifulSoup(r.text, 'html.parser')
        for alist in soup.find_all(bp.match_soup_class(['articleList'])):
            tit = alist.find('span', attrs={'class': 'tit'})
            title = bp.check_valid_string(tit.text)
            keywords = bp.get_news_article_info(alist.a['href'])
            keywords_list.extend(keywords)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, alist.a['href'], title)
        return result

    def financial_donga(self, bp, category):
        result = '<font color="blue">[동아일보 %s]</font>' % category
        r = bp.request_and_get('http://news.donga.com/Economy')  # 동아일보
        if r is None:
            result = '%s<br>No article.' % result
            return result

        soup = BeautifulSoup(r.text, 'html.parser')
        for alist in soup.find_all(bp.match_soup_class(['articleList'])):
            tit = alist.find('span', attrs={'class': 'tit'})
            title = bp.check_valid_string(tit.text)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, alist.a['href'], title)
        return result

    def opinion_mbn(self, bp, keywords_list):
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t0005" id="t0005" href="#t0005" class="invisible"> </a><font color="blue">[매일경제 사설, 칼럼]</font>'
        r = bp.request_and_get('http://opinion.mk.co.kr/list.php?sc=30500003')
        if r is None:
            result = '%s<br>No article.' % result
            return result

        base_url = 'http://opinion.mk.co.kr/'
        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        for f in soup.find_all(bp.match_soup_class(['article_list'])):
            for dt in f.find_all('dt'):
                href = '%s%s' % (base_url, dt.a['href'])
                title = bp.check_valid_string(dt.text)
                keywords = bp.get_news_article_info(href)
                keywords_list.extend(keywords)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def opinion_hankyung(self, bp, keywords_list):
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t0011" id="t0011" href="#t0011" class="invisible"> </a><font color="blue">[한국경제 사설, 칼럼]</font>'
        r = bp.request_and_get('http://news.hankyung.com/opinion')
        if r is None:
            result = '%s<br>No article.' % result
            return result
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for inner_list in soup.find_all(bp.match_soup_class(['inner_list'])):
            for li in inner_list.find_all('li'):
                li_title = li.find('strong', attrs={'class': 'tit'})
                if li_title is None:
                    break
                title = bp.check_valid_string(li_title.text)
                keywords = bp.get_news_article_info(li.a['href'])
                keywords_list.extend(keywords)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, li.a['href'], title)

            tit = inner_list.find('strong', attrs={'class': 'tit'})
            title = bp.check_valid_string(tit.text)
            keywords = bp.get_news_article_info(inner_list.a['href'])
            keywords_list.extend(keywords)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, inner_list.a['href'], title)
        return result

    def opinion_chosun(self, bp, keywords_list):
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t0009" id="t0009" href="#t0009" class="invisible"> </a><font color="blue">[조선일보 사설, 칼럼]</font>'
        r = bp.request_and_get('http://biz.chosun.com/svc/list_in/list.html?catid=1F&op_s')
        if r is None:
            result = '%s<br>No article.' % result
            return result

        base_url = 'http://biz.chosun.com'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for f in soup.find_all(bp.match_soup_class(['list_vt'])):
            for li in f.find_all('li'):
                dt = li.find('dt')
                href = '%s%s' % (base_url, li.a['href'])
                title = bp.check_valid_string(dt.a.text)
                keywords = bp.get_news_article_info(href)
                keywords_list.extend(keywords)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def opinion_joins(self, bp, keywords_list):
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t0008" id="t0008" href="#t0008" class="invisible"> </a><font color="blue">[중앙일보 사설, 칼럼]</font>'
        r = bp.request_and_get('http://news.joins.com/opinion?cloc=joongang|home|section1')
        if r is None:
            result = '%s<br>No article.' % result
            return result

        base_url = 'http://news.joins.com'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for head in soup.find_all(bp.match_soup_class(['opinion_home_headline'])):
            for li in head.find_all('li'):
                href = '%s%s' % (base_url, li.a['href'])
                title = bp.check_valid_string(li.a.text)
                keywords = bp.get_news_article_info(href)
                keywords_list.extend(keywords)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)

        for today in soup.find_all(bp.match_soup_class(['opinion_home_today'])):
            for li in today.find_all('li'):
                href = '%s%s' % (base_url, li.a['href'])
                mg = li.find('strong', attrs={'class': 'mg'})
                keywords = bp.get_news_article_info(href)
                keywords_list.extend(keywords)
                title = bp.check_valid_string(mg.text)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def opinion_hankook(self, bp, keywords_list):
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t0012" id="t0012" href="#t0012" class="invisible"> </a><font color="blue">[한국일보 사설, 칼럼]</font>'
        r = bp.request_and_get('http://www.hankookilbo.com/op.aspx')
        if r is None:
            result = '%s<br>No article.' % result
            return result
        base_url = 'http://www.hankookilbo.com'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for col in soup.find_all(bp.match_soup_class(['editorial_column'])):
            for li in col.find_all('li'):
                href = '%s%s' % (base_url, li.a['href'])
                title = bp.check_valid_string(li.a.text)
                keywords = bp.get_news_article_info(href)
                keywords_list.extend(keywords)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def opinion_gyunghyang(self, bp, keywords_list):
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t0001" id="t0001" href="#t0001" class="invisible"> </a><font color="blue">[경향신문 사설, 칼럼]</font>'
        r = bp.request_and_get('http://news.khan.co.kr/kh_news/khan_art_list.html?code=990000')
        if r is None:
            result = '%s<br>No article.' % result
            return result

        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        for news_list in soup.find_all(bp.match_soup_class(['news_list'])):
            for li in news_list.find_all('li'):
                try:
                    title = bp.check_valid_string(li.a['title'])
                    keywords = bp.get_news_article_info(li.a['href'])
                    keywords_list.extend(keywords)
                    result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, li.a['href'], title)
                except KeyError:
                    title = bp.check_valid_string(li.text.split('\n')[1])
                    keywords = bp.get_news_article_info(li.a['href'])
                    keywords_list.extend(keywords)
                    result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, li.a['href'], title)
        return result

    def opinion_kookmin(self, bp, keywords_list):
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t0002" id="t0002" href="#t0002" class="invisible"> </a><font color="blue">[국민일보 사설]</font>'
        url = 'http://news.kmib.co.kr/article/list.asp?sid1=opi&sid2=&sdate=%s' % bp.yesterday
        r = bp.request_and_get(url)
        if r is None:
            result = '%s<br>No article.' % result
            return result

        base_url = 'http://news.kmib.co.kr/article'
        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        for nws_list in soup.find_all(bp.match_soup_class(['nws_list'])):
            for dl in nws_list.find_all('dl'):
                if dl.text == '등록된 기사가 없습니다.':
                    result = '%s<br>현재 %s<br>' % (result, dl.text)
                    return result
                dt = dl.find('dt')
                href = '%s/%s' % (base_url, dt.a['href'])
                keywords = bp.get_news_article_info(href)
                keywords_list.extend(keywords)
                title = bp.check_valid_string(dt.a.text)
                result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def opinion_segye(self, bp, keywords_list):
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t0007" id="t0007" href="#t0007" class="invisible"> </a><font color="blue">[세계일보 사설, 칼럼]</font>'
        r = bp.request_and_get('http://www.segye.com/opinion')
        if r is None:
            result = '%s<br>No article.' % result
            return result

        base_url = 'http://www.segye.com'
        soup = BeautifulSoup(r.content.decode('utf-8', 'replace'), 'html.parser')
        for title_1 in soup.find_all(bp.match_soup_class(['title_1'])):
            href = '%s%s' % (base_url, title_1.a['href'])
            title = bp.check_valid_string(title_1.a.text)
            keywords = bp.get_news_article_info(href)
            keywords_list.extend(keywords)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        for title_2 in soup.find_all(bp.match_soup_class(['title_2'])):
            href = '%s%s' % (base_url, title_2.a['href'])
            title = bp.check_valid_string(title_2.a.text)
            keywords = bp.get_news_article_info(href)
            keywords_list.extend(keywords)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, href, title)
        return result

    def opinion_moonhwa(self, bp, keywords_list):
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t0006" id="t0006" href="#t0006" class="invisible"> </a><font color="blue">[문화일보 사설, 칼럼]</font>'
        r = bp.request_and_get('http://www.munhwa.com/news/section_list.html?sec=opinion&class=0')
        if r is None:
            result = '%s<br>No article.' % result
            return result

        soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
        for d14b_333 in soup.find_all(bp.match_soup_class(['d14b_333'])):
            title = bp.check_valid_string(d14b_333.text)
            keywords = bp.get_news_article_info(d14b_333['href'])
            keywords_list.extend(keywords)
            result = '%s<br><a href="%s" target="_blank">%s</a>' % (result, d14b_333['href'], title)
        return result

    def realestate_news(self, bp, press, keywords_list):
        if press == '국토교통부':
            return self.realestate_molit(bp, keywords_list)
        elif press == '연합뉴스':
            return self.realestate_yonhapnews(bp, keywords_list)
        elif press == '건설경제':
            return self.realestate_cnews(bp, keywords_list)
        elif press == '서울경제':
            return self.realestate_sedaily(bp, keywords_list)
        elif press == '더벨':
            return self.realestate_thebell(bp, keywords_list)
        elif press == '경향신문':
            return self.realestate_gyunghyang(bp, keywords_list)
        elif press == '국민일보':
            return self.realestate_kookmin(bp, keywords_list)
        elif press == '노컷뉴스':
            return self.realestate_nocut(bp, keywords_list)
        elif press == '동아일보':
            return self.realestate_donga(bp, keywords_list)
        elif press == '매일경제':
            return self.realestate_mbn(bp, keywords_list)
        elif press == '문화일보':
            return self.realestate_moonhwa(bp, keywords_list)
        elif press == '세계일보':
            return self.realestate_segye(bp, keywords_list)
        elif press == '중앙일보':
            return self.realestate_joins(bp, keywords_list)
        elif press == '조선일보':
            return self.realestate_chosun(bp, keywords_list)
        elif press == '한겨례':
            return self.realestate_hani(bp, keywords_list)
        elif press == '한국경제':
            return self.realestate_hankyung(bp, keywords_list)
        elif press == '네이버':
            return self.realestate_naver(bp, keywords_list)
        else:
            result = '[' + press + '] No article.'
            return result

    def economy_news(self, bp, press, keywords_list):
        if press == '연합뉴스':
            return self.economy_yonhapnews(bp, keywords_list)
        elif press == '건설경제':
            return self.economy_cnews(bp, keywords_list)
        elif press == '서울경제':
            return self.economy_sedaily(bp, keywords_list)
        elif press == '더벨':
            return self.economy_thebell(bp, keywords_list)
        elif press == '더스쿱':
            return self.economy_thescoop(bp, keywords_list)
        elif press == '경향신문':
            return self.economy_gyunghyang(bp, keywords_list)
        elif press == '매일경제':
            return self.economy_mbn(bp, keywords_list)
        elif press == '조선일보':
            return self.economy_chosun(bp, keywords_list)
        elif press == '한국경제':
            return self.economy_hankyung(bp, keywords_list)
        else:
            result = '[' + press + '] No article.'
            return result

    def opinion_news(self, bp, press, keywords_list):
        if press == '경향신문':
            return self.opinion_gyunghyang(bp, keywords_list)
        elif press == '국민일보':
            return self.opinion_kookmin(bp, keywords_list)
        elif press == '노컷뉴스':
            return '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t0003" id="t0003" href="#t0003" class="invisible"> </a><font color="blue">[노컷뉴스 오피니언]</font><br>Not support'
        elif press == '동아일보':
            return self.opinion_donga(bp, keywords_list)
        elif press == '매일경제':
            return self.opinion_mbn(bp, keywords_list)
        elif press == '문화일보':
            return self.opinion_moonhwa(bp, keywords_list)
        elif press == '세계신문':
            return self.opinion_segye(bp, keywords_list)
        elif press == '중앙일보':
            return self.opinion_joins(bp, keywords_list)
        elif press == '조선일보':
            return self.opinion_chosun(bp, keywords_list)
        elif press == '한겨례':
            return self.opinion_hani(bp, keywords_list)
        elif press == '한국경제':
            return self.opinion_hankyung(bp, keywords_list)
        elif press == '한국일보':
            return self.opinion_hankook(bp, keywords_list)
        else:
            result = '[' + press + '] No article.'
            return result

    async def fetch(self, subject, loop, bp, keywords_list, category):
        if category == 'realestate':
            result = await loop.run_in_executor(None, self.realestate_news, bp, subject, keywords_list)
        elif category == 'economy':
            result = await loop.run_in_executor(None, self.economy_news, bp, subject, keywords_list)
        elif category == 'opinion':
            result = await loop.run_in_executor(None, self.opinion_news, bp, subject, keywords_list)
        elif category == 'reddit':
            result = await loop.run_in_executor(None, self.reddit_news, bp, subject)
        return result

    def get_keywords(self, keywords_list):
        return [val for sublist in keywords_list for val in sublist
                if len(val) > 2 and
                not val.startswith('있') and not val.startswith('것') and
                val != '것이다' and val != '한다' and
                val != '했다' and val != '사설' and
                val != '칼럼' and val != '지난해' and
                val != '한겨레' and val != '네이버' and
                val != '안된다' and val != '부동산' and
                val != '팀장칼럼' and val != '한국의' and
                val != '하지만' and
                val != '기자수첩']

    async def post_economy(self, loop, bp):
        press_list = ['더벨', '더스쿱', '연합뉴스', '건설경제', '서울경제',
                      '경향신문', '매일경제', '조선일보', '한국경제']
        keywords_list = []
        futures = [asyncio.ensure_future(self.fetch(press, loop, bp, keywords_list, 'economy')) for press in press_list]
        result = await asyncio.gather(*futures)  # 결과를 한꺼번에 가져옴

        keywords = self.get_keywords(keywords_list)
        counter = Counter(keywords)
        common_keywords = [c[0] for c in counter.most_common(5)]
        print('경제쪽은 이게 왜 엉망이냐')
        print(common_keywords)
        content = ''
        for r in result:
            if r is None or len(r) == 0:
                continue
            content = '%s<br>%s<br><br>' % (content, r)
        title = '[%s] 국내 언론사 경제 뉴스 헤드라인' % bp.today
        bp.tistory_post('scrapnpost', title, content, '765357')
        # bp.naver_post(title, content)

    async def post_realestate(self, loop, bp):
        press_list = ['국토교통부', '연합뉴스', '매일경제', '건설경제',
                      '서울경제', '더벨',
                      '경향신문', '국민일보', '노컷뉴스', '동아일보',
                      '문화일보', '중앙일보', '조선일보', '한겨례',
                      '한국경제', '네이버']
        keywords_list = []
        futures = [asyncio.ensure_future(self.fetch(press, loop, bp, keywords_list, 'realestate')) for press in press_list]
        result = await asyncio.gather(*futures)  # 결과를 한꺼번에 가져옴

        keywords = self.get_keywords(keywords_list)
        counter = Counter(keywords)
        common_keywords = [c[0] for c in counter.most_common(5)]
        content = '''<strong>오늘의 주요 키워드</strong><br>
    %s<br>
        ''' % (', '.join(common_keywords))
        for r in result:
            if r is None or len(r) == 0:
                continue
            content = '%s<br>%s<br><br>' % (content, r)
            # content = '%s<br>%s<br><br>%s<br>' % (content, r, ADSENSE_MIDDLE)
        title = '[%s] 국내 언론사 부동산 뉴스 헤드라인' % bp.today
        bp.tistory_post('scrapnpost', title, content, '765348')
        # bp.naver_post(title, content)

    async def post_opinion(self, loop, bp):
        press_list = ['경향신문', '국민일보', '노컷뉴스', '동아일보', '매일경제',
                      '문화일보', '세계신문', '중앙일보', '조선일보', '한겨례',
                      '한국경제', '한국일보']
        keywords_list = []
        futures = [asyncio.ensure_future(self.fetch(press, loop, bp, keywords_list, 'opinion')) for press in press_list]
        result = await asyncio.gather(*futures)  # 결과를 한꺼번에 가져옴
        keywords = self.get_keywords(keywords_list)

        counter = Counter(keywords)
        common_keywords = [c[0] for c in counter.most_common(5)]
        content = '''<strong>언론사 목록</strong><br>
    <a href="#t0001">경향신문, </a> <a href="#t0002">국민일보, </a> <a href="#t0003">노컷뉴스, </a><br>
    <a href="#t0004">동아일보, </a> <a href="#t0005">매일경제, </a> <a href="#t0006">문화일보, </a><br>
    <a href="#t0007">세계일보, </a> <a href="#t0008">중앙일보, </a> <a href="#t0009">조선일보, </a><br>
    <a href="#t0010">한겨례, </a> <a href="#t0011">한국경제, </a> <a href="#t0012">한국일보, </a><br>
    <strong>오늘의 주요 키워드</strong><br>
    %s<br>
        ''' % (', '.join(common_keywords))
        for r in result:
            content = '%s<br>%s<br><br>' % (content, r)
            # content = '%s<br>%s<br><br>%s<br>' % (content, r, ADSENSE_MIDDLE)
        title = '[%s] 국내 주요언론사 사설, 칼럼 헤드라인(ㄱ,ㄴ순)' % bp.today
        bp.tistory_post('scrapnpost', title, content, '767067')  # 사설, 칼럼
        # bp.naver_post(title, content)

    async def post_reddit(self, loop, bp):
        # sub_reddits = ['programming', 'Futurology', 'worldnews', 'announcements', 'todayilearned', ]
        sub_reddits = ['programming', 'Futurology']
        futures = [asyncio.ensure_future(self.fetch(sub_reddit, loop, bp, None, 'reddit')) for sub_reddit in sub_reddits]
        result = await asyncio.gather(*futures)  # 결과를 한꺼번에 가져옴

        content = '''<strong>Reddit 서브 카테고리 목록</strong><br>
    <a href="#t1001">- programming</a><br>
    <a href="#t1004">- Futurology</a><br>
        '''
        for r in result:
            content = '%s<br>%s<br><br>' % (content, r)
        # title = '[%s] Reddit 오늘의 소식(프로그래밍, 미래기술, 세계뉴스, 선언/공표, TIL)' % bp.today
        title = '[%s] Reddit 오늘의 소식(프로그래밍, 미래기술)' % bp.today
        bp.tistory_post('scrapnpost', title, content, '765668')  # IT news
        # bp.naver_post(title, content)
