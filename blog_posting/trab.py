#!/usr/bin/env python3
from bs4 import BeautifulSoup
from selenium import webdriver


class TraceDailyComms:
    def __init__(self):
        pass

    def nate_pann(self, bp):  # 톡거들의 선택 명예의 전당   trab 776709
        result = '<strong><font color="blue">[Nate Pann] 톡커들의 선택 명예의 전당</font></strong>'
        url = 'http://pann.nate.com/talk/ranking/d?stdt=20180222&page=1'
        r = bp.request_and_get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        href, title = None, None
        for post_wrap in soup.find_all(bp.match_soup_class(['post_wrap'])):
            for idx1, dl in enumerate(post_wrap.find_all('dl')):
                if idx1 > 10:
                    return result
                for dt in dl.find_all('dt'):
                    href = dt.a['href']
                    title = dt.a['title']
                for idx2, dd in enumerate(dl.find_all('dd')):
                    if idx2 == 1:
                        count = dd.find('span', attrs={'class': 'count'})
                        rcm = dd.find('span', attrs={'class': 'rcm'})
                        result = '%s<br><strong><a href="%s" target="_blank">%s</a></strong>, %s, %s' % (
                                 result, href, title, count.text, rcm.text)
        return None
    '''
    http://pann.nate.com/talk/341024545 만만한 성격 바꾸는방법좀
    인상부터 순함  길은 나한테 다물어봄  모른다고하면 화냄  첨보는사람이 자기집안얘기 아픈얘기...
    조회 132,999 추천 711
    '''
    def today_humor(self, bp):  # 베오베
        result = '<strong><font color="blue">[오늘의 유머] 베스트 오브 베스트</font></strong>'
        url = 'http://www.todayhumor.co.kr/board/list.php?table=bestofbest'
        r = bp.request_and_get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        sessions = soup.select('body > div > div > div > table > tbody > tr > td')
        # sessions = soup.select('body > div > div > div > table > tbody > tr > td > a')
        # body > div.whole_box > div > div > table > tbody > tr:nth-child(2) > td.subject > a
        for idx, s in enumerate(sessions):
            # print([idx], s)
            if idx % 7 == 3:
                href = s.a['href']
                title = s.text
                # print(s.text, s.a['href'])
            elif idx % 7 == 4:
                user_id = s.text
            elif idx % 7 == 6:
                result = '%s<br><strong><a href="%s" target="_blank">%s</a></strong>, 작성자: %s, 조회수: %s' % (
                         result, href, title, user_id, s.text)

            if idx > 70:  # 7 * 10 (I need 10 posts)
                return result
        return None
    '''
    엄마 공부하면 뭐가 좋아? [26]    /board/view.php?table=bestofbest&no=387158&s_no=387158&page=1
    언니거긴안돼
    18/02/23 15:17
    7724
    '''

    def dcinside(self, bp):  # HIT 갤러리
        result = '<strong><font color="blue">[디씨인사이드] HIT 갤러리</font></strong>'
        url = 'http://gall.dcinside.com/board/lists/?id=hit'
        driver = webdriver.PhantomJS()
        driver.implicitly_wait(3)
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        base_url = 'http://gall.dcinside.com'
        for list_tbody in soup.find_all(bp.match_soup_class(['list_tbody'])):
            for idx1, tr in enumerate(list_tbody.find_all('tr')):
                if idx1 < 2:
                    continue
                if idx1 > 13:  # I need only 10 posts (3 ~ 12)
                    return result

                for idx2, td in enumerate(tr.find_all('td')):
                    if idx2 == 1:
                        href = '%s%s' % (base_url, td.a['href'])
                        title = td.text.strip()
                    elif idx2 == 2:
                        user_id = td.text
                    elif idx2 == 4:
                        count = td.text
                    elif idx2 == 5:
                        result = '%s<br><strong><a href="%s" target="_blank">%s</a></strong>, 작성자: %s, 조회수: %s, 추천수: %s' % (
                                 result, href, title, user_id, count, td.text)
        return None
    '''
    스압) 프암걸 흐레스벨그 클리어 도색,조립 해봤어.[155]
     http://gall.dcinside.com/board/view/?id=hit&no=14463&page=1
    빡시
    2018.02.23
    4103
    71
    '''

    def bobedream(self, bp):  # 베스트글
        result = '<strong><font color="blue">[보배드림] 베스트글</font></strong>'
        url = 'http://www.bobaedream.co.kr/list?code=best&vdate='
        driver = webdriver.PhantomJS()
        driver.implicitly_wait(3)
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        base_url = 'http://www.bobaedream.co.kr'
        for tbody in soup.find_all('tbody'):
            for idx1, tr in enumerate(tbody.find_all('tr')):
                if idx1 > 10:
                    return result
                for idx2, td in enumerate(tr.find_all('td')):
                    if idx2 == 1:
                        href = '%s%s' % (base_url, td.a['href'])
                        title = td.text.strip()
                    elif idx2 == 2:
                        user_id = td.find('span', attrs={'class': 'author'})
                    elif idx2 == 4:
                        recommand = td.text
                    elif idx2 == 5:
                        result = '%s<br><strong><a href="%s" target="_blank">%s</a></strong>, 작성자: %s, 조회수: %s, 추천수: %s' % (
                                 result, href, title, user_id, td.text, recommand)
        return None
    '''
    <속보>검찰, 신연희  구속영장 청구 (27) http://www.bobaedream.co.kr/view?code=best&No=154084&vdate=
    <span class="author" onclick="javascript:submenu_show('b3BocXFvcGhxZm9waHFsb3Boc2xvcGhzZm9waHNqb3Boc2w%3D','');" style="cursor:pointer;" title="무궁화의눈물">무궁화의눈..</span>
    95
    5399
    '''
    def clien(self, bp):
        result = '<strong><font color="blue">[클리앙] 모두의 공원 댓글순 인기글</font></strong>'
        url = 'https://www.clien.net/service/board/park?&od=T34'
        base_url = 'https://www.clien.net'
        r = bp.request_and_get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for idx1, list_title in enumerate(soup.find_all(bp.match_soup_class(['list_title']))):
            if idx1 == 0:
                continue
            if idx1 > 11:
                return result
            try:
                href = '%s%s' % (base_url, list_title.a['href'])
            except TypeError:
                continue

            temp = list_title.text.split()
            title = ' '.join(temp[0:-1])
            result = '%s<br><strong><a href="%s" target="_blank">%s</a></strong>, 댓글수: %s' % (
                     result, href, title, temp[-1])
        return None

    def ruriweb(self, bp):
        result = '<strong><font color="blue">[루리웹] 베스트</font></strong>'
        url = 'http://bbs.ruliweb.com/best?type=now&orderby=regdate&range=24h'
        r = bp.request_and_get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for tbody in soup.find_all('tbody'):
            for idx1, tr in enumerate(tbody.find_all('tr')):
                for idx2, td in enumerate(tbody.find_all('td')):
                    if idx2 > 50:
                        return result
                    if idx2 % 6 == 1:
                        href = td.a['href']
                        title = td.text.strip()
                    elif idx2 % 6 == 2:
                        user_id = td.text.strip()
                    elif idx2 % 6 == 3:
                        recommand = td.text.strip()
                    elif idx2 % 6 == 4:
                        # result = '%s<br><strong><a href="%s" target="_blank">%s</a></strong>, 댓글수: %s' % (
                        #          result, href, title, temp[-1])
                        result = '%s<br><strong><a href="%s" target="_blank">%s</a></strong>, 작성자: %s, 조회수: %s, 추천수: %s' % (
                                 result, href, title, user_id, td.text.strip(), recommand)

    def korea_community_best(self, bp):
        content = '''
<strong>주요 커뮤니티 현재 인기글 모음</strong>
<br><br>
<pre>
    <a href="http://gall.dcinside.com/board/lists/?id=hit" target="_blank">- 디씨인사이드</a>
    <a href="https://www.clien.net/service/board/park?&od=T34" target="_blank">- 클리앙</a>
    <a href="http://bbs.ruliweb.com/best?type=now&orderby=regdate&range=24h" target="_blank">- 루리웹</a>
    <a href="http://www.bobaedream.co.kr/list?code=best&vdate=" target="_blank">- 보배드림</a>
    <a href="http://www.todayhumor.co.kr/board/list.php?table=bestofbest" target="_blank">- 오늘의 유머</a>
    <a href="http://pann.nate.com/talk/ranking/d?stdt=20180222&page=1" target="_blank">- Nate 판</a>
</pre>
'''
        r = self.dcinside(bp)
        if r is not None:
            content = '%s<br><br>%s' % (content, r)
        r = self.ruriweb(bp)
        if r is not None:
            content = '%s<br><br>%s' % (content, r)
        r = self.clien(bp)
        if r is not None:
            content = '%s<br><br>%s' % (content, r)
        r = self.bobedream(bp)
        if r is not None:
            content = '%s<br><br>%s' % (content, r)
        r = self.today_humor(bp)
        if r is not None:
            content = '%s<br><br>%s' % (content, r)
        r = self.nate_pann(bp)
        if r is not None:
            content = '%s<br><br>%s<br><br><br>' % (content, r)
        title = '[%s] 커뮤니티 현재 인기글 모음(디씨인사이드, 클리앙, 루리웹, 보베드림, 오늘의 유머, 네이트판)', bp.today
        bp.tistory_post('trab', title, content, '776709')
        bp.naver_post(title, content, '9')
