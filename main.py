from config import TargetConfig
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import quote
import ssl
from bs4 import BeautifulSoup
import html5lib
import logging
import argparse
import pymysql
from time import sleep

# python3 main.py --tg FINANCE_CRAWLING
# - 실시간 증시, 환율, 유가 시세정보 노출   
# ① 증시: 코스피, 코스닥, 다우, 나스닥  
# ② 환율: 미국, 일본, 유럽연합, 중국   
# ③ 유가: 두바이유, WTI, 휘발유, 고급휘발유 

def dbInsert(sec1, sec2, num1, num2, txt):

    conn = pymysql.connect(host=TargetConfig.DB_HOST, user=TargetConfig.DB_USER, password=TargetConfig.DB_PW, db=TargetConfig.DB_NAME, charset='utf8')
    curs = conn.cursor()

    sql = 'INSERT INTO FINANCE (STOCK_TYPE, STOCK_SUBTYPE, STOCK_SCORE, STOCK_CHG_SCORE, STOCK_SCORE_TEXT) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE STOCK_SCORE = %s, STOCK_CHG_SCORE = %s, STOCK_SCORE_TEXT = %s'
    data = (sec1, sec2, num1, num2, txt, num1, num2, txt)
    curs.execute(sql, data)
    conn.commit()
    print("@@데이터입력@@")

def main(args, logger):

    for target in args.tg:
        if target == 'FINANCE_CRAWLING':
            try:
                loop = True
                while loop == True:

                    print("-- 크롤링 시작")

                    url = TargetConfig.FINANCE

                    try:
                        context = ssl._create_unverified_context()
                        html = urlopen(url, context=context)
                        source = html.read().decode('euc-kr')
                        html.close()
                        soup = BeautifulSoup(source, "html5lib")
                    except HTTPError as e:
                        err = e.read()   
                        errCode = e.getcode()
                        print("HTTP ERROR : " + errCode)

                    # ① 증시: 코스피, 코스닥, 다우, 나스닥
                    # 하락 : num_quot dn, 상승 : num_quot up

                    # 코스피
                    kospi0 = soup.find("div", class_="kospi_area group_quot quot_opn")
                    kospi1 = kospi0.find("span", class_="num_quot dn") or kospi0.find("span", class_="num_quot up")
                    kospiNum1 = kospi1.find("span", class_="num").get_text()
                    kospiNum2 = kospi1.find("span", class_="num2").get_text()
                    kospiTxt = "하락" if kospi0.find("span", class_="num_quot dn") else "상승"
                    print("코스피")
                    print(kospiNum1)
                    print(kospiNum2)
                    print(kospiTxt)

                    dbInsert("증시", "코스피", kospiNum1, kospiNum2, kospiTxt)

                    print("~~~~~~~~~~~~~~~~")

                    # 코스닥
                    kosdaq0 = soup.find("div", class_="kosdaq_area group_quot")
                    kosdaq1 = kosdaq0.find("span", class_="num_quot dn") or kosdaq0.find("span", class_="num_quot up")
                    kosdaqNum1 = kosdaq1.find("span", class_="num").get_text()
                    kosdaqNum2 = kosdaq1.find("span", class_="num2").get_text()
                    kosdaqTxt = "하락" if kosdaq0.find("span", class_="num_quot dn") else "상승"
                    print("코스닥")
                    print(kosdaqNum1)
                    print(kosdaqNum2)
                    print(kosdaqTxt)

                    dbInsert("증시", "코스닥", kosdaqNum1, kosdaqNum2, kosdaqTxt)

                    print("~~~~~~~~~~~~~~~~")

                    # 다우
                    h_stock = soup.find("div", class_="aside_area aside_stock").find("tbody")
                    stocks = h_stock.find_all("tr")
                    dow0 = stocks[0].find_all("td")
                    dowNum1 = dow0[0].get_text()
                    dow2 = dow0[1].get_text().split(" ")
                    dowNum2 = dow2[1]
                    dowTxt = dow2[0]
                    print("다우")
                    print(dowNum1)
                    print(dowNum2)
                    print(dowTxt)

                    dbInsert("증시", "다우", dowNum1, dowNum2, dowTxt)

                    print("~~~~~~~~~~~~~~~~")

                    # 나스닥
                    nasdaq0 = stocks[1].find_all("td")
                    nasdaqNum1 = nasdaq0[0].get_text()
                    nasdaq2 = nasdaq0[1].get_text().split(" ")
                    nasdaqNum2 = nasdaq2[1]
                    nasdaqTxt = nasdaq2[0]
                    print("나스닥")
                    print(nasdaqNum1)
                    print(nasdaqNum2)
                    print(nasdaqTxt)

                    dbInsert("증시", "나스닥", nasdaqNum1, nasdaqNum2, nasdaqTxt)

                    print("~~~~~~~~~~~~~~~~")

                    # ② 환율: 미국, 일본, 유럽연합, 중국   
                    exchange0 = soup.find("div", class_="article2").find("tbody")
                    for ex in exchange0.find_all("tr"):
                        exCountry = ex.find("th").find("a").get_text()
                        print("환율")
                        print(exCountry)
                        tds =  ex.find_all("td")
                        exNum1 = tds[0].get_text()
                        exchange1 = tds[1].get_text().split(" ")
                        exNum2 = exchange1[1]
                        exTxt = exchange1[0]
                        print(exNum1)
                        print(exNum2)
                        print(exTxt)

                        dbInsert("환율", exCountry, exNum1, exNum2, exTxt)

                        print("~~~~~~~~~~~~~~~~")
                    
                    # ③ 유가: 두바이유, WTI, 휘발유, 고급휘발유 
                    oil0 = soup.find("h2", class_="h_oil").find_all_next()
                    oil1 = oil0[1].find("tbody")
                    for o in oil1.find_all("tr"):
                        oilName = o.find("th").find("a").get_text().split("(")[0].strip()
                        print("유가")
                        print(oilName)
                        tds = o.find_all("td")
                        oilNum1 = tds[0].get_text()
                        oil2 = tds[1].get_text().split(" ")
                        oilNum2 = oil2[1]
                        oilTxt = oil2[0]
                        print(oilNum1)
                        print(oilNum2)
                        print(oilTxt)

                        dbInsert("유가", oilName, oilNum1, oilNum2, oilTxt)

                        print("~~~~~~~~~~~~~~~~")

                    print("-- SLEEP!!!")
                    sleep(10)
                    
            except Exception as ex:
                logger.error("main error(2)" + str(ex))


if __name__ == '__main__':

    logging.basicConfig(format='[%(lineno)d]%(asctime)s||%(message)s')
    logger = logging.getLogger(name="myLogger")

    parser = argparse.ArgumentParser()
    parser.add_argument('--tg', nargs='+', help='start crawling')
    args = parser.parse_args()

    try:
        main(args, logger)
    except:
        logger.error("main error(1)")
        raise