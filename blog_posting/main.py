#!/usr/bin/env python3
import asyncio

from blog_post import BlogPost
from dexa import DailyLifeAndPost
from scrapnpost import ScrapAndPost
from trab import TraceDailyComms


async def async_main(loop):
    bp = BlogPost()
    tap = TraceDailyComms()
    sap = ScrapAndPost()
    dap = DailyLifeAndPost()

    if bp.week_num == 0:  # monday
        await dap.post_event_n_exhibit(loop, bp)
        sap.aladin_book(bp, 'ItemNewSpecial', 20)
    elif bp.week_num == 1:
        dap.hyundai_curture_center(bp)
        dap.realstate_trade(bp)
        sap.aladin_book(bp, 'Bestseller', 20)
    elif bp.week_num == 2:
        dap.lotte_curture_center(bp)
        sap.aladin_book(bp, 'ItemNewAll', 20)
    elif bp.week_num == 3:
        dap.savings(bp)  # 적금
        sap.aladin_book(bp, 'BlogBest', 20)
    elif bp.week_num == 4:
        dap.fixed_deposit(bp)  # 예금

    # everyday
    tap.korea_community_best(bp)
    dap.popular_twit(bp)
    await sap.post_reddit(loop, bp)
    await sap.post_realestate(loop, bp)
    await sap.post_opinion(loop, bp)

def main():
    loop = asyncio.get_event_loop()            # 이벤트 루프를 얻음
    loop.run_until_complete(async_main(loop))  # async_main이 끝날 때까지 기다림
    loop.close()                               # 이벤트 루프를 닫음


if __name__ == '__main__':
    main()
