from config import TargetConfig
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import quote
import ssl
from bs4 import BeautifulSoup
import html5lib

# python3 main.py --tg FINANCE_CRAWLING
# - 실시간 증시, 환율, 유가 시세정보 노출   
# ① 증시: 코스피, 코스닥, 다우, 나스닥  
# ② 환율: 미국, 일본, 유럽연합, 중국   
# ③ 유가: 두바이유, WTI, 휘발유, 고급휘발유 

def main():
    
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
    print(kospiNum1)
    print(kospiNum2)
    print(kospiTxt)

    print("~~~~~~~~~~~~~~~~")

    # 코스닥 kosdaq_area group_quot
    kosdaq0 = soup.find("div", class_="kosdaq_area group_quot")
    kosdaq1 = kosdaq0.find("span", class_="num_quot dn") or kosdaq0.find("span", class_="num_quot up")
    kosdaqNum1 = kosdaq1.find("span", class_="num").get_text()
    kosdaqNum2 = kosdaq1.find("span", class_="num2").get_text()
    kosdaqTxt = "하락" if kosdaq0.find("span", class_="num_quot dn") else "상승"
    print(kosdaqNum1)
    print(kosdaqNum2)
    print(kosdaqTxt)

    print("~~~~~~~~~~~~~~~~")

    # 다우
    # 나스닥
    h_stock = soup.find("div", class_="aside_area aside_stock").find("tbody")
    stocks = h_stock.find_all("tr")
    dow0 = stocks[0].find_all("td")
    dowNum1 = dow0[0].get_text()
    dow2 = dow0[1].get_text().split(" ")
    dowNum2 = dow2[1]
    dowTxt = dow2[0]
    print(dowNum1)
    print(dowNum2)
    print(dowTxt)

    print("~~~~~~~~~~~~~~~~")

    nasdaq0 = stocks[1].find_all("td")
    nasdaqNum1 = nasdaq0[0].get_text()
    nasdaq2 = nasdaq0[1].get_text().split(" ")
    nasdaqNum2 = nasdaq2[1]
    nasdaqTxt = nasdaq2[0]
    print(nasdaqNum1)
    print(nasdaqNum2)
    print(nasdaqTxt)

    print("~~~~~~~~~~~~~~~~")
    

if __name__ == '__main__':

    try:
        main()
    except:
        print("main error(1)")