#!/usr/bin/env python3
import asyncio
import json
import re
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver

from define import ADSENSE_MIDDLE, BANK_CODE, LOAN_CODE, SAVINGS_BANK_CODE, INSURANCE_CODE, INVESTMENT_CODE


class DailyLifeAndPost:
    def __init__(self):
        pass

    def hyundai_curture_center(self, bp):
        result = '<strong><font color="blue">[현대백화점 문화센터 추천강좌]</font></strong><br><br>'
        base_url = 'https://www.ehyundai.com'
        lcode = {'압구정본점': '210',
                 '무역센터점': '220',
                 '천호점': '260',
                 '신촌점': '270',
                 '미아점': '410',
                 '목동점': '420',
                 '부천중동점': '430',
                 '킨텍스점': '450',
                 '부산점': '240',
                 '울산동구점': '250',
                 '울산점': '290',
                 '대구점': '460',
                 '충청점': '470',
                 '판교점': '480',
                 '디큐브시티(신도림)점': '490',
                 '가든파이브(송파)점': '750', }
        result = '%s<pre>' % result
        cnt = 1
        for location, code in lcode.items():
            part_url = 'http://www.ehyundai.com/newCulture/CT/CT010200_L.do?stCd=%s' % code
            result = '%s<a href="%s" target="_blank">%d. %s</a><br>' % (result, part_url, cnt, location)
            cnt += 1
        result = '%s</pre>' % result
        result = '%s<br>%s<br>' % (result, ADSENSE_MIDDLE)

        for location, code in lcode.items():
            result = '%s<br><br><font color="red">[%s]</font><br>' % (result, location)
            url = 'http://www.ehyundai.com/newCulture/CT/CT010200_L.do?stCd=%s' % code
            r = bp.request_and_get(url)
            if r is None:
                return False
            soup = BeautifulSoup(r.text, 'html.parser')
            for best in soup.find_all(bp.match_soup_class(['best_lecturelist'])):
                for li in best.find_all('li'):
                    href = '%s%s' % (base_url, li.a['href'])
                    date = li.find('span', attrs={'class': 'date'})
                    fee = li.find('span', attrs={'class': 'fee'})
                    result = '%s<br><strong><a href="%s" target="_blank">%s</a></strong><br>%s<br>[%s]<br>' % (
                             result, href, li.a.text.strip(), date.text, fee.text)
        title = '[%s] 현대백화점 각 지점별 문화센터 추천강좌 일정' % bp.today
        bp.tistory_post('dexa', title, result, '730606')
        return True

    def lotte_curture_center(self, bp):
        result = '<strong><font color="blue">[롯데백화점 문화센터 추천강좌]</font></strong><br><br>'
        lcode = {'본점(명동)': '0001', '잠실점': '0002', '청량리점': '0004',
                 '부산본점': '0005', '관악점': '0006', '광주점': '0007',
                 '분당점': '0008', '부평점': '0009', '영등포점': '0010',
                 '일산점': '0011', '대전점': '0012', '강남점': '0013',
                 '포항점': '0014', '울산점': '0015', '동례점': '0016',
                 '창원점': '0017', '안양점': '0018', '인천점': '0020',
                 '노원점': '0022', '대구점': '0023', '상인점': '0024',
                 '전주점': '0025', '미아점': '0026', '센텀시티점': '0027',
                 '건대스타시티점': '0028',
                 '광복점': '0333', '중동점': '0334', '구리점': '0335',
                 '안산점': '0336', '김포공항점': '0340', '평촌점': '0341',
                 '수원점': '0349', '마산점': '0354', }

        result = '%s<pre>' % result
        cnt = 1
        for location, code in lcode.items():
            part_url = 'https://culture.lotteshopping.com/CLSS_list.do?taskID=L&pageNo=1&vpStrCd=&vpKisuNo=&vpClassCd=&vpTechNo=&pStrCd=%s&pLarGbn=&pMidGbn=&pClsFee=&pDayGbnAll=&pDayTime=&pStatus=&pKisuValue=C&pClsNm=&pClsNmTemp=&pTechNm=&pTechNmTemp=' % code
            result = '%s<a href="%s" target="_blank">%d. %s</a><br>' % (result, part_url, cnt, location)
            cnt += 1

        result = '%s</pre>' % result
        result = '%s<br>%s<br>' % (result, ADSENSE_MIDDLE)
        for location, code in lcode.items():
            result = '%s<br><br><font color="red">[%s]</font><br>' % (result, location)
            url = 'https://culture.lotteshopping.com/CLSS_list.do?taskID=L&pageNo=1&vpStrCd=&vpKisuNo=&vpClassCd=&vpTechNo=&pStrCd=%s&pLarGbn=&pMidGbn=&pClsFee=&pDayGbnAll=&pDayTime=&pStatus=&pKisuValue=C&pClsNm=&pClsNmTemp=&pTechNm=&pTechNmTemp=' % code
            r = bp.request_and_get(url)
            if r is None:
                return False
            soup = BeautifulSoup(r.text, 'html.parser')
            for i1, article in enumerate(soup.find_all(bp.match_soup_class(['article']))):
                if i1 == 0:  # side menu
                    continue
                for i2, tr in enumerate(article.find_all('tr')):
                    if i2 == 0:  # category
                        continue
                    try:
                        onclick = tr.find('input', {'name': 'chk'}).get('onclick')
                    except AttributeError:
                        continue
                    on_split = onclick.split("'")
                    href = 'https://culture.lotteshopping.com/CLSS_view.do?taskID=L&pageNo=1&vpStrCd=%s&vpKisuNo=%s&vpClassCd=%s' % (on_split[1], on_split[3], on_split[5])

                    for i3, td in enumerate(tr.find_all('td')):
                        info = td.text.strip().split()
                        if i3 == 2:
                            title = ' '.join(info)
                        elif i3 == 3:
                            author = ' '.join(info)
                        elif i3 == 4:
                            date = ' '.join(info)
                        elif i3 == 5:
                            price = ' '.join(info)
                    result = '%s<br><strong><a href="%s" target="_blank">%s(%s)</a></strong><br>%s<br>[%s]<br>' % (
                             result, href, title, author, date, price)
        title = '[%s] 롯데백화점 각 지점별 문화센터 일정' % bp.today
        bp.tistory_post('dexa', title, result, '730606')
        return True

    def vic_market(self, bp):
        result = '<br>'
        base_url = 'http://company.lottemart.com'
        r = bp.request_and_get('http://company.lottemart.com/vc/info/branch.do?SITELOC=DK013', '빅마켓')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        for i1, vic in enumerate(soup.find_all(bp.match_soup_class(['vicmarket_normal_box']))):
            if i1 != 1:
                continue
            for i2, li in enumerate(vic.find_all('li')):
                if i2 % 5 != 0:
                    continue
                for img in li.find_all('img'):
                    thumbnail = '%s%s' % (base_url, img['src'])
                    break
                button = str(li.button).split("'")
                href = '%s%s' % (base_url, button[1])
                result = '%s<strong><a href="%s" target="_blank">%s<font color="red"></font></a></strong><br>' % (
                         result, href, li.h3.text)
                for ul in li.find_all('ul'):
                    for li2 in ul.find_all('li'):
                        temp = li2.text.strip().replace('\t', '').replace('\r', '')
                        temp_info = temp.split('\n')
                        infos = [t for t in temp_info if len(t) != 0]
                        result = '%s<br>%s: %s' % (result, infos[0], ' '.join(infos[1:]))
                result = '%s<br><center><a href="%s" target="_blank"> <img border="0" src="%s" width="150" height="150"></a></center><br><br>' % (result, href, thumbnail)
        return result

    def join_deny(self, num):
        if num == '1':
            return '가입 제한없음'
        elif num == '2':
            return '서민전용 가입'
        elif num == '3':
            return '가입 일부제한'
        else:
            return 'Unknown'

    def dcls_end_day(self, day):  # 공시종료일
        if day is None:
            return '공시 종료일 미정'
        else:
            return '공시 종료일 ' + day

    def max_limit(self, money):  # 공시종료일
        if money is None:
            return '한도정보 없음'
        else:
            m = str(money)
            ret = m.endswith('00000000')
            if ret is True:
                return m[0:-8] + '억원'

            ret = m.endswith('0000000')
            if ret is True:
                return m[0:-7] + '천만원'

            ret = m.endswith('000000')
            if ret is True:
                return m[0:-6] + '백만원'

            ret = m.endswith('00000')
            if ret is True:
                return m[0:-5] + '십만원'
            else:
                return m + '원'

    def get_fixed_deposit(self, bp, gcode, group):
        if group == '은행':
            code_info = BANK_CODE
        elif group == '저축은행':
            code_info = SAVINGS_BANK_CODE
        else:
            bp.logger.error('Invalid group %s', group)
            return None

        result = '금융감독원의 금융상품통합 비교공시 정보를 바탕으로 작성된 글입니다.<br><br><br>'
        cnt = 0
        for bank, code in code_info.items():
            url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth=%s&topFinGrpNo=%s&pageNo=1&financeCd=%s' % (bp.finlife_key, gcode, code)
            r = bp.request_and_get(url)
            if r is None:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            js = json.loads(str(soup))
            if len(js['result']['baseList']) == 0:
                continue
            result = '%s<h3>%s</h3><br><table border="1" cellspacing="0" cellpadding="3" bordercolor="#  999999" style="border-collapse:collapse">' % (result, bank)
            result = '''%s<tr>
            <th>금융상품,가입방법</th>
            <th>우대조건</th>
            <th>가입대상</th>
            <th>최고한도</th>
            </tr>''' % (result)
            for banks in js['result']['baseList']:
                result = '%s<tr>' % result
                result = '%s<td><font color="red">%s</font><br><br>➡ %s 가입<br>➡ %s<br>➡ %s</td>' % (result, banks["fin_prdt_nm"], banks['join_way'], self.join_deny(banks['join_deny']), self.dcls_end_day(banks['dcls_end_day']))
                # result = '%s<td>%s</td>' % (result, banks["join_way"])
                result = '%s<td>%s</td>' % (result, banks["spcl_cnd"].replace('\n', '<br>'))
                # result = '%s<td>%s</td>' % (result, banks['join_member'])
                result = '%s<td>%s</td>' % (result, banks['etc_note'].replace('\n', '<br>'))
                result = '%s<td>%s</td>' % (result, self.max_limit(banks['max_limit']))
                result = '%s</tr>' % result
            result = '%s</table><br><br><br>' % result
            cnt += 1
            if cnt % 10 == 0:
                result = '%s<br>%s<br><br><br>' % (result, ADSENSE_MIDDLE)
        return result

    def get_specipic_mortgage_loan(self, bp, gcode, group):
        if group == '은행':
            code_info = BANK_CODE
        elif group == '저축은행':
            code_info = SAVINGS_BANK_CODE
        elif group == '보험사':
            code_info = INSURANCE_CODE
        else:
            bp.logger.error('Invalid group %s', group)
            return None

        result = '금융감독원의 금융상품통합 비교공시 정보를 바탕으로 작성된 글입니다.<br><br><br>'

        for bank, code in code_info.items():
            url = 'http://finlife.fss.or.kr/finlifeapi/mortgageLoanProductsSearch.json?auth=%s&topFinGrpNo=%s&pageNo=1&financeCd=%s' % (bp.finlife_key, gcode, code)
            r = bp.request_and_get(url)
            if r is None:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            js = json.loads(str(soup))
            if len(js['result']['baseList']) == 0:
                continue
            option_list_len = (len(js['result']['optionList']))
            result = '%s<h3>%s</h3><br><table border="1" cellspacing="0" cellpadding="3" bordercolor="#  999999" style="border-collapse:collapse">' % (result, bank)
            result = '''%s<tr>
             <th>대출상품</th>
             <th>부대비용</th>
             <th>중도상환수수료</th>
             <th>연채 이자율</th>
             <th>금리</th>
             </tr>''' % (result)
            for banks in js['result']['baseList']:
                result = '%s<tr>' % result
                result = '%s<td><font color="red">%s</font><br><br>➡ %s으로 가입<br>➡ %s<br>➡ %s</td>' % (result, banks["fin_prdt_nm"], banks['join_way'], self.dcls_end_day(banks['dcls_end_day']), banks['loan_lmt'])
                result = '%s<td>%s</td>' % (result, banks["loan_inci_expn"].replace('\n', '<br>'))
                result = '%s<td>%s</td>' % (result, banks["erly_rpay_fee"].replace('\n', '<br>'))
                result = '%s<td>%s</td>' % (result, banks["dly_rate"].replace('\n', '<br>'))
                result = '%s<td>' % result
                for i in range(option_list_len):
                    result = '%s<br>[%s]<br> 담보:%s, %s<br><br>➡ 최저: %s<br>➡ 최대: %s<br>➡ 평균: %s<br>' % (
                             result,
                             js['result']['optionList'][i]['lend_rate_type_nm'],
                             js['result']['optionList'][i]['mrtg_type_nm'],
                             js['result']['optionList'][i]['rpay_type_nm'],
                             js['result']['optionList'][i]['lend_rate_min'],
                             js['result']['optionList'][i]['lend_rate_max'],
                             js['result']['optionList'][i]['lend_rate_avg'])
                result = '%s</td></tr>' % result
            result = '%s</table><br><br><br>' % result
        return result

    def get_specipic_private_loan(self, bp, gcode, group):
        if group == '은행':
            code_info = BANK_CODE
        elif group == '여신전문':
            code_info = LOAN_CODE
        elif group == '저축은행':
            code_info = SAVINGS_BANK_CODE
        elif group == '보험사':
            code_info = INSURANCE_CODE
        elif group == '금융투자사':
            code_info = INVESTMENT_CODE
        else:
            bp.logger.error('Invalid group %s', group)
            return None

        result = '금융감독원의 금융상품통합 비교공시 정보를 바탕으로 작성된 글입니다.<br><br><br>'
        cnt = 0
        for bank, code in code_info.items():
            url = 'http://finlife.fss.or.kr/finlifeapi/creditLoanProductsSearch.json?auth=%s&topFinGrpNo=%s&pageNo=1&financeCd=%s' % (bp.finlife_key, gcode, code)
            r = bp.request_and_get(url)
            if r is None:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            js = json.loads(str(soup))
            if len(js['result']['baseList']) == 0:
                continue
            option_list_len = (len(js['result']['optionList']))
            result = '%s<h3>%s</h3><br><table border="1" cellspacing="0" cellpadding="3" bordercolor="#  999999" style="border-collapse:collapse">' % (result, bank)
            result = '''%s<tr>
             <th>대출상품</th>
             <th>금리</th>
             </tr>''' % (result)
            for banks in js['result']['baseList']:
                result = '%s<tr>' % result
                result = '%s<td><font color="red">%s</font><br><br>➡ %s으로 가입<br>➡ %s<br></td>' % (
                         result,
                         banks["crdt_prdt_type_nm"],
                         banks['join_way'],
                         self.dcls_end_day(banks['dcls_end_day']))
                fin_prdt_cd = banks['fin_prdt_cd']
                result = '%s<td>' % result
                for i in range(option_list_len):
                    if fin_prdt_cd == js['result']['optionList'][i]['fin_prdt_cd']:

                        result = '%s<br>[%s]<br>- 은행:1~2등급,비은행:1~3등급 ➡ %s<br>- 은행:3~4등급,비은행:4등급➡ %s<br>- 은행:5~6등급,비은행:5등급➡ %s<br>- 은행:7~8등급,비은행:6등급➡ %s<br>- 은행:9~10등급,비은행:7~10등급➡ %s<br>' % (
                                 result,
                                 js['result']['optionList'][i]['crdt_lend_rate_type_nm'],
                                 js['result']['optionList'][i]['crdt_grad_1'],
                                 js['result']['optionList'][i]['crdt_grad_4'],
                                 js['result']['optionList'][i]['crdt_grad_5'],
                                 js['result']['optionList'][i]['crdt_grad_6'],
                                 js['result']['optionList'][i]['crdt_grad_10'])
                result = '%s</td></tr>' % result
            result = '%s</table><br><br><br>' % result
            cnt += 1
            if cnt % 10 == 0:
                result = '%s<br>%s<br><br><br>' % (result, ADSENSE_MIDDLE)
        return result

    def get_specipic_rent_subsidy(self, bp, gcode, group):
        if group == '은행':
            code_info = BANK_CODE
        elif group == '여신전문':
            code_info = LOAN_CODE
        elif group == '저축은행':
            code_info = SAVINGS_BANK_CODE
        elif group == '보험사':
            code_info = INSURANCE_CODE
        elif group == '금융투자사':
            code_info = INVESTMENT_CODE
        else:
            bp.logger.error('Invalid group %s', group)
            return None

        result = '금융감독원의 금융상품통합 비교공시 정보를 바탕으로 작성된 글입니다.<br><br><br>'
        cnt = 0
        for bank, code in code_info.items():
            url = 'http://finlife.fss.or.kr/finlifeapi/rentHouseLoanProductsSearch.json?auth=%s&topFinGrpNo=%s&pageNo=1&financeCd=%s' % (bp.finlife_key, gcode, code)
            r = bp.request_and_get(url)
            if r is None:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            js = json.loads(str(soup))
            if len(js['result']['baseList']) == 0:
                continue
            option_list_len = (len(js['result']['optionList']))
            result = '%s<h3>%s</h3><br><table border="1" cellspacing="0" cellpadding="3" bordercolor="#  999999" style="border-collapse:collapse">' % (result, bank)
            result = '''%s<tr>
             <th>대출상품</th>
             <th>대출부대비용</th>
             <th>그외 수수료</th>
             <th>금리</th>
             </tr>''' % (result)
            for banks in js['result']['baseList']:
                result = '%s<tr>' % result
                result = '%s<td><font color="red">%s</font><br><br>➡ %s으로 가입<br>➡ 제한: <strong>%s</strong><br>➡ %s<br></td>' % (
                         result,
                         banks["fin_prdt_nm"],
                         banks['join_way'],
                         banks['loan_lmt'],
                         self.dcls_end_day(banks['dcls_end_day']))
                result = '%s<td>%s</td>' % (result, banks["loan_inci_expn"].replace('\n', '<br>'))
                result = '%s<td>[중도상환수수료]<br>%s<br><br>[연체 이자율]%s<br></td>' % (
                         result,
                         banks["loan_inci_expn"].replace('\n', '<br>'),
                         banks["erly_rpay_fee"].replace('\n', '<br>'))
                fin_prdt_cd = banks['fin_prdt_cd']
                result = '%s<td>' % result
                for i in range(option_list_len):
                    if fin_prdt_cd == js['result']['optionList'][i]['fin_prdt_cd']:
                        result = '%s<br>[%s]<br>%s<br><br>최저: %s<br>최고: %s<br> ' % (
                                 result,
                                 js['result']['optionList'][i]['rpay_type_nm'],
                                 js['result']['optionList'][i]['lend_rate_type_nm'],
                                 js['result']['optionList'][i]['lend_rate_min'],
                                 js['result']['optionList'][i]['lend_rate_max'])
                result = '%s</td></tr>' % result
            result = '%s</table><br><br><br>' % result
            cnt += 1
            if cnt % 10 == 0:
                result = '%s<br>%s<br><br><br>' % (result, ADSENSE_MIDDLE)
        return result

    def mortgage_loan(self, bp):
        grp_code = {'020000': '은행',
                    '030300': '저축은행',
                    '050000': '보험사', }
        # 030200(여신전문),  060000(금융투자)
        for gcode, group in grp_code.items():

            title = '[%s] %s 주택담보대출 금리 정보' % (bp.today, group)
            content = self.get_specipic_mortgage_loan(bp, gcode, group)
            if content is None:
                continue
            bp.tistory_post('dexa', title, content, '731649')

    def private_loan(self, bp):
        grp_code = {'020000': '은행',
                    '030200': '여신전문',
                    '030300': '저축은행',
                    '050000': '보험사', }
        for gcode, group in grp_code.items():

            title = '[%s] %s 개인신용대출 금리 정보' % (bp.today, group)
            content = self.get_specipic_private_loan(bp, gcode, group)
            if content is None:
                continue
            bp.tistory_post('dexa', title, content, '731649')

    def rent_subsidy(self, bp):
        grp_code = {'020000': '은행',
                    '030300': '저축은행',
                    '050000': '보험사', }

        for gcode, group in grp_code.items():

            title = '[%s] %s 전세자금대출 금리 정보' % (bp.today, group)
            content = self.get_specipic_rent_subsidy(bp, gcode, group)
            if content is None:
                continue
            bp.tistory_post('dexa', title, content, '731649')

    def get_specipic_savings(self, bp, gcode, group):
        if group == '은행':
            code_info = BANK_CODE
        elif group == '여신전문':
            code_info = LOAN_CODE
        elif group == '저축은행':
            code_info = SAVINGS_BANK_CODE
        elif group == '보험사':
            code_info = INSURANCE_CODE
        elif group == '금융투자사':
            code_info = INVESTMENT_CODE
        else:
            bp.logger.error('Invalid group %s', group)
            return None

        result = '금융감독원의 금융상품통합 비교공시 정보를 바탕으로 작성된 글입니다.<br><br><br>'
        cnt = 0
        for bank, code in code_info.items():
            url = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth=%s&topFinGrpNo=%s&pageNo=1&financeCd=%s' % (bp.finlife_key, gcode, code)
            r = bp.request_and_get(url)
            if r is None:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            js = json.loads(str(soup))
            if len(js['result']['baseList']) == 0:
                continue
            option_list_len = (len(js['result']['optionList']))
            result = '%s<h3>%s</h3><br><table border="1" cellspacing="0" cellpadding="3" bordercolor="#999999" style="  border-collapse:collapse">' % (result, bank)
            result = '''%s<tr>
                       <th width="150">적금상품</th>
                       <th>우대조건</th>
                       <th width="120">이자</th>
                       </tr>''' % (result)
            for banks in js['result']['baseList']:
                result = '%s<tr>' % result
                result = '%s<td><font color="red">%s</font><br><br>➡ %s으로 가입<br>➡ %s<br>➡ %s<br>➡ %s<br><br>➡ <strong>한도: 월 %s</strong></td>' % (
                         result,
                         banks["fin_prdt_nm"],
                         banks['join_way'],
                         banks['join_member'],
                         self.join_deny(banks['join_deny']),
                         self.dcls_end_day(banks['dcls_end_day']),
                         self.max_limit(banks['max_limit']))

                result = '%s<td>%s</td>' % (result, banks["spcl_cnd"].replace('\n', '<br>'))

                fin_prdt_cd = banks['fin_prdt_cd']
                result = '%s<td>' % result
                for i in range(option_list_len):
                    if fin_prdt_cd == js['result']['optionList'][i]['fin_prdt_cd']:
                        result = '%s<br><strong>[%s, %s]</strong><br>납입기간: %s개월<br><font color="red">저축금리: %s</font><br>최고우대금리: %s<br>' % (
                                 result,
                                 js['result']['optionList'][i]['intr_rate_type_nm'],
                                 js['result']['optionList'][i]['rsrv_type_nm'],
                                 js['result']['optionList'][i]['save_trm'],
                                 js['result']['optionList'][i]['intr_rate'],
                                 js['result']['optionList'][i]['intr_rate2'])
                result = '%s</td>' % result

            result = '%s</table><br><br><br>' % result
            cnt += 1
            if cnt % 10 == 0:
                result = '%s<br>%s<br><br><br>' % (result, ADSENSE_MIDDLE)
        return result

    def savings(self, bp, vendor='tistory'):
        grp_code = {'020000': '은행',
                    '030300': '저축은행', }
        for gcode, group in grp_code.items():

            title = '[%s] %s 적금 금리 정보' % (bp.today, group)
            content = self.get_specipic_savings(bp, gcode, group)
            if content is None:
                continue
            if vendor == 'tistory':
                bp.tistory_post('dexa', title, content, '731649')
            else:
                bp.naver_post(title, content, '9')

    def fixed_deposit(self, bp, vendor='tistory'):

        grp_code = {'020000': '은행',
                    '030300': '저축은행', }
        for gcode, group in grp_code.items():

            title = '[%s] %s 예금 금리 정보' % (bp.today, group)
            content = self.get_fixed_deposit(bp, gcode, group)
            if content is None:
                continue
            if vendor == 'tistory':
                bp.tistory_post('dexa', title, content, '731649')
            else:
                bp.naver_post(title, content, '9')

    def dividend_income(self, bp, rankTpcd, stkTpcd='1'):  # 주식 배당 관련 조회
        stkTpcd = '1'  # [1]보통주, [2]우선주
        listTpcd = { '11': '유가증권시장', '12': '코스닥시장',
                     '13': 'K-OTC',  '14': '코넥스시장', '50': '기타비상장', }
        result = ''
        for tcode, tname in listTpcd.items():
            if rankTpcd == '1':  # [1]시가배당율, [2]액면가배당율
                result = '%s<br><br><br><h3>%s 보통주 (시가배당율 순위)</h3><br><table border="1" cellspacing="0" cellpadding="3" bordercolor="#999999" style="  border-collapse:collapse">' % (result, tname)
                result = '''%s<tr>
                 <th>배당순위</th>
                 <th>주식코드</th>
                 <th>주식회사</th>
                 <th>주당배당금</th>
                 <th><font color="red">시가배당율</font></th>
                 <th>액면가배당율</th>
                 </tr>''' % (result)
            else:
                result = '%s<br><br><br><h3>%s 보통주 (액면가배당율 순위)</h3><br><table border="1" cellspacing="0" cellpadding="3" bordercolor="#999999" style="  border-collapse:collapse">' % (result, tname)
                result = '''%s<tr>
                 <th>배당순위</th>
                 <th>주식코드</th>
                 <th>주식회사</th>
                 <th>주당배당금</th>
                 <th>시가배당율</th>
                 <th><font color="red">액면가배당율</font></th>
                 </tr>''' % (result)
            for i in range(1, 3):
                url = 'http://api.seibro.or.kr/openapi/service/StockSvc/getDividendRankN1?year=2017&rankTpcd=' + rankTpcd + '&stkTpcd=' + stkTpcd + '&listTpcd=' + tcode + '&pageNo=' + str(i) + '&ServiceKey=' + bp.korea_data_key
                r = bp.request_and_get(url)
                soup = BeautifulSoup(r.text, 'lxml')
                for item in soup.items.find_all('item'):
                    result = '%s<tr>' % result
                    # print(item.caltotmarttpcd.text)
                    result = '%s<td align="center">%s</td>' % (result, item.num.text)
                    result = '%s<td align="center">%s</td>' % (result, item.shotnisin.text)
                    result = '%s<td align="center">%s</td>' % (result, item.korsecnnm.text)
                    result = '%s<td align="right">%s</td>' % (result, item.divamtperstk.text)
                    result = '%s<td align="right">%s</td>' % (result, item.divratecpri.text)
                    result = '%s<td align="right">%s</td>' % (result, item.divratepval.text)
                    result = '%s</tr>' % result
            result = '%s</table>' % result
            result = '%s<br>%s<br>' % (result, ADSENSE_MIDDLE)

        return result

    def get_korea_tour(self, bp):  # 대한민국 구석구석 행복여행
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t2003" id="t2003" href="#t2003" class="invisible"> </a><font color="blue">[대한민국 구석구석 행복여행]</font><br>'
        r = bp.request_and_get('http://korean.visitkorea.or.kr/kor/bz15/where/festival/festival.jsp')
        if r is None:
            result = '%s<br>No article.' % result
            return result

        base_url = 'http://korean.visitkorea.or.kr/kor/bz15/where/festival'
        soup = BeautifulSoup(r.text, 'html.parser')
        for s in soup.find_all(bp.match_soup_class(['item'])):
            if s.h3 is None:
                continue
            result_url = '%s/%s' % (base_url, s.a['href'])
            desc = repr(s.h3)[4: -6]
            img = s.find('img')
            thumbnail = img['src']
            for info in s.find_all(bp.match_soup_class(['info2'])):
                for span in info.find_all('span', {'class': 'date'}):
                    result = '%s<br><strong><a href="%s" target="_blank"><font color="red">%s</font></a></strong><br>%s<br>' % (
                             result, result_url, desc, span.text)
                    result = '%s<center><a href="%s" target="_blank"> <img border="0" src="%s" width="150" height="150"></a></center>' % (
                             result, result_url, thumbnail)
                    break
        return result

    def get_exhibit_image(self, bp, href):
        try:
            page = urllib.request.urlopen(href)
        except UnicodeEncodeError:
            bp.logger.error('[get_exhibit_image] UnicodeEncodeError %s', href)
            return None
        except urllib.error.URLError:
            bp.logger.error('[get_exhibit_image] URLError %s', href)
            return None
        base_url = href.split('/')
        base_url = '%s//%s' % (base_url[0], base_url[2])

        soup = BeautifulSoup(page, 'html.parser')
        for img in soup.find_all('img', {'src': re.compile(r'(jpe?g)|(png)$')}):
            if img['src'].find('logo') != -1:
                if img['src'].find('http') != -1:
                    return img['src']
                else:
                    img_link = '%s/%s' % (base_url, img['src'])
                    return img_link
        else:
            icon_link = soup.find("link", rel="shortcut icon")
            try:
                icon_image_link = icon_link['href']
                return icon_image_link
            except TypeError:
                return None

    def get_oversea_exhibition(self, bp):
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t2004" id="t2004" href="#t2004" class="invisible"> </a><font color="blue">[국제 전시회 일정]</font><br>'
        request_url = 'http://www.gep.or.kr/rest/overseasExhibition?serviceKey=%s&from=%s&to=%s&pageRows=20&pageNumber=1&type=json' % (bp.korea_data_key, bp.yesterday, bp.today)
        req = urllib.request.Request(request_url)
        try:
            res = urllib.request.urlopen(req)
        except UnicodeEncodeError:
            bp.logger.error('[overseasExhibition] UnicodeEncodeError')
            return

        data = res.read().decode('utf-8')
        soup = BeautifulSoup(data, 'html.parser')
        js = json.loads(str(soup))
        for exhibit in js['overseasExhibitionListArray']:
            href = exhibit['homepage']
            if not href.startswith('http://'):
                href = 'http://%s' % href

            img_link = self.get_exhibit_image(bp, href)
            if img_link is None:
                img_link = '#'

            exitem = exhibit['exhibitionItem']
            exitem = exitem.replace(r'\r', '<br>').replace(r'\r\n', '<br>').replace('\\r\\n', '<br>')

            result = '%s<br><a href="%s" target="_blank"><font color="red">%s(%s)</font></a><br>전시항목: %s<br>일정: %s<br>스폰서: %s<br>주소: %s  ☎ :%s (%s %s)<br><a href="mailto:%s">Email: %s</a> (%s년 부터 %s 개최)<br><center><a href="%s" target="_blank"> <img border="0" src="%s" width="150" height="100"></a></center><br>' % (
                     result,
                     href, exhibit['exhibitionTitleKor'], exhibit['exhibitionTitleEng'],
                     exitem, exhibit['openingTerm'], exhibit['sponsor'],
                     exhibit['address'], exhibit['telephone'],
                     exhibit['openingCountry'], exhibit['openingCity'],
                     exhibit['email'], exhibit['email'],
                     exhibit['firstOpeningYear'], exhibit['openingCycle'],
                     href, img_link)
        return result

    def get_sacticket(self, bp):  # 예술의 전당
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t2002" id="t2002" href="#t2002" class="invisible"> </a><font color="blue">[예술의 전당 일정]</font><br>'
        driver = webdriver.PhantomJS()
        driver.implicitly_wait(3)
        url = 'https://www.sacticket.co.kr/SacHome/ticket/reservation'
        driver.get(url)
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        for p in soup.find_all(bp.match_soup_class(['ticket_list_con'])):
            for poster in p.find_all(bp.match_soup_class(['poster'])):
                for pa in poster.find_all('img'):
                    thumbnail = (pa['src'])
            if thumbnail.endswith('no_result.png'):
                continue
            for content in p.find_all(bp.match_soup_class(['content'])):
                try:
                    c_info = content.a['onclick'].split("'")
                    page_id = c_info[1]
                    page_type = c_info[3]
                    if page_type == 'E':
                        category = "[전시]"
                        link = 'https://www.sacticket.co.kr/SacHome/exhibit/detail?searchSeq=%s' % page_id
                    elif page_type == 'P':
                        category = "[공연]"
                        link = 'https://www.sacticket.co.kr/SacHome/perform/detail?searchSeq=%s' % page_id
                    else:
                        continue

                    for idx, ca in enumerate(content.find_all('a')):
                        if idx == 0:
                            title = ca.text
                        elif idx == 1:
                            if ca.text != '무료':
                                price = '유료'
                            else:
                                price = ca.text

                    result = '%s<br><font color="red">%s</font><br>%s %s<br><br><center><a href="%s" target="_blank"> <img border="0" src="%s" width="150" height="150"></a></center>' % (result, title, category, price, link, thumbnail)
                except TypeError:
                    continue
        driver.quit()
        return result

    def get_coex(self, bp):
        result = '<hr class="noprint" style="width: 96ex;" align="left"/><a name="t2001" id="t2001" href="#t2001" class="invisible"> </a><font color="blue">[COEX 행사 일정]</font><br>'
        r = bp.request_and_get('http://www.coex.co.kr/blog/event_exhibition?list_type=list')
        if r is None:
            result = '%s<br>No Information.' % result
            return result

        soup = BeautifulSoup(r.text, 'html.parser')
        exhibition_url = 'http://www.coex.co.kr/blog/event_exhibition'
        for a in soup.find_all('a', href=True):
            thumbnail = ''
            if a['href'].startswith(exhibition_url) is False:
                continue

            for img in a.find_all('img'):
                thumbnail = img['src']

            if len(thumbnail) == 0:
                continue

            for idx, li in enumerate(a.find_all('li')):
                if idx % 5 == 0:
                    category = li.text
                elif idx % 5 == 1:
                    spans = li.find_all('span', attrs={'class': 'subject'})
                    for span in spans:
                        subject = span.text
                    spans = li.find_all('span', attrs={'class': 'url'})
                    for span in spans:
                        url = span.text
                    url = 'http://%s' % url
                elif idx % 5 == 2:
                    period = li.text
                elif idx % 5 == 3:
                    price = li.text
                elif idx % 5 == 4:
                    location = li.text
                    result = '%s<br><a href="%s" target="_blank"><font color="red">%s (%s)</font></a><br>%s, %s, %s<br><br><center><a href="%s" target="_blank"> <img border="0" src="%s" width="150" height="150"></a></center>' % (result, url, subject, category, period, location, price, url, thumbnail)
        return result

    def event_n_exhibit(self, bp, subject):
        if subject == 'coex':
            return self.get_coex(bp)
        elif subject == 'sacticket':
            return self.get_sacticket(bp)
        elif subject == 'korea_tour':
            return self.get_korea_tour(bp)
        elif subject == 'oversea_exhibition':
            return self.get_oversea_exhibition(bp)

    async def fetch(self, subject, loop, bp, category):
        result = ''
        if category == 'event':
            result = await loop.run_in_executor(None, self.event_n_exhibit, bp, subject)
        return result

    async def post_event_n_exhibit(self, loop, bp):
        subjects = ['coex', 'sacticket', 'korea_tour', 'oversea_exhibition']
        futures = [asyncio.ensure_future(self.fetch(subject, loop, bp, 'event')) for subject in subjects]
        result = await asyncio.gather(*futures)  # 결과를 한꺼번에 가져옴

        content = '''<strong>행사/전시 목록</strong><br>
    <a href="#t2001">- COEX</a><br> <a href="#t2002">- 예술의전당</a><br>
    <a href="#t2003">- 대한민국 구석구석 행복여행</a><br> <a href="#t2004">- 해외전시</a><br>
        '''
        for r in result:
            content = '%s<br>%s<br><br>' % (content, r)

        title = '[%s] 각종 행사 및 전시일정(예술의 전당, 코엑스, Korea Tour, 국제 전시)' % bp.today
        bp.tistory_post('dexa', title, content, '736121')  # Dexa event
