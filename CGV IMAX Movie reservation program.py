#pip install selenium 설치
#python -m pip install bs4 설치
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time

theater='CGV영등포' #영화관 선택 (IMAX 전용)
date=datetime.strptime("20240314", "%Y%m%d") #예매 희망 날짜, 단 현재부터 2주 이내
title='듄-파트2'#영화 제목
#어른,청소년 포함최대 8명까지
adult_people=1 #일반 예매 인원(경로,우대 안됨) 
youth_people=1 #청소년 예매 인원
#자기 chrome에 맞는 버전을https://chromedriver.chromium.org/downloads에서 설치 PM> Install-Package Selenium.WebDriver.ChromeDriver -Version 122.0.6261.11100
#압축을 풀고 파일 경로 설정
browser = webdriver.Chrome("./chromedriver.exe") #chromedriver가 있는 파일 경로 입력
browser.get('https://www.cgv.co.kr/')
browser.maximize_window()
browser.find_element_by_xpath('//*[@id="cgvwrap"]/div[2]/div[1]/div/ul/li[1]/a').click()

browser.implicitly_wait(2)
browser.find_element_by_name('txtUserId').send_keys('*****') #아이디 입력
browser.find_element_by_name('txtPassword').send_keys('****') #비밀번호 입력
browser.find_element_by_xpath('//*[@id="submit"]/span').click() #로그인

browser.implicitly_wait(2)
#비밀번호 변경하라고 뜬다면 if browser.find_element_by_class_name('sect-passwardchange'):
if browser.find_element_by_xpath('//*[@id="contents"]/div/div'):
    print('비밀번호 변경하는 창 나옴')
    browser.find_element_by_xpath('//*[@id="ctl00_PlaceHolderContent_btn_pw_chag_later"]').click()
else:
    print("비밀번호 변경하라는 창 안나옴")

#상단메뉴에서 극장선택하기
browser.find_element_by_xpath('//*[@id="cgvwrap"]/div[2]/div[2]/div/ul/li[2]/h2/a').click()
browser.implicitly_wait(2)

#극장 선택하기
browser.find_element_by_link_text(theater).click()
browser.implicitly_wait(5)
iframe = browser.find_element_by_id("ifrm_movie_time_table") 
browser.switch_to.frame(iframe) 


#상영시간표가 보이도록 스크롤 내리기
some_tag_1 = browser.find_element_by_class_name('sect-schedule') #스크롤 내리기
action = ActionChains(browser)
action.move_to_element(some_tag_1).perform()
browser.implicitly_wait(2)

soup=BeautifulSoup(browser.page_source)
now=datetime.now()
date_1=date.strftime("%d")

slider_1=soup.find(class_="item").text
if date_1 in slider_1:
    browser.find_element_by_partial_link_text(date_1).send_keys(Keys.ENTER)

else: #현재 페이지에 희망 날짜가 없으면 next버튼으로 날짜 이동
    browser.find_element_by_class_name('btn-next').click()
    browser.implicitly_wait(1)

try:
    browser.find_element_by_partial_link_text(date_1).click()
    browser.implicitly_wait(1)

except NoSuchElementException: #해당 날짜가 열리지 않았다면 브라우저 종료
    print("해당 날짜는 열리지 않았습니다.")
    browser.close()

soup=BeautifulSoup(browser.page_source)

browser.implicitly_wait(3)
while True:  #영화가 해당날짜에 없으면 나올때까지 무한 클릭
    title_one=soup.find(class_="sect-showtimes").text #영화 리스트
    
    if title in title_one:
        break
    else:
        browser.find_element_by_partial_link_text(date_1).click()
        browser.implicitly_wait(1)

elemt_1=browser.find_element_by_class_name('sect-showtimes').find_element_by_tag_name('ul')
li_2=elemt_1.find_elements_by_class_name('col-times')

time.sleep(1)
for i in range(len(li_2)):
    if title in li_2[i].text:
        browser.implicitly_wait(2)
        imax_element =li_2[i].find_element_by_class_name("imax") #imax class를 찾음
        imax_element.click()
        browser.implicitly_wait(2)
        parent_element = imax_element.find_element_by_xpath("./ancestor::*[contains(@class, 'type-hall')]") 
        info_timetable=parent_element.find_element_by_class_name('info-timetable').find_element_by_tag_name('ul') #IMAX관 스케줄 확인
        li=info_timetable.find_elements_by_tag_name('li')
        
        if len(li)<=2: #영화 시간 임의 선택할 수 없음(대략 오후3시~5시 사이 상영작)
            li[len(li)-1].click()
        elif len(li)<=4:
            li[len(li)-2].click()
        elif len(li)>=5:
            li[len(li)-3].click()
        break

time.sleep(5)
iframe1 = browser.find_element_by_id("ticket_iframe") 
browser.switch_to.frame(iframe1) 
browser.implicitly_wait(2)
browser.find_element_by_id('tnb_step_btn_right').click()
browser.implicitly_wait(3)

popup_check1=WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.LINK_TEXT, "닫기")))
popup_button1=browser.find_elements_by_link_text('닫기')[0]
popup_button1.click()
# popup_check2=WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.LINK_TEXT, "닫기")))
# popup_button2=browser.find_elements_by_link_text('닫기')[0]
# popup_button2.click()

browser.implicitly_wait(3)
#인원 선택
browser.find_element_by_xpath('//*[@id="nop_group_adult"]/ul/li[{0}]'.format(adult_people+1)).click()
browser.find_element_by_xpath('//*[@id="nop_group_youth"]/ul/li[{0}]'.format(youth_people+1)).click()

seats_list=browser.find_elements_by_xpath('//*[@id="seats_list"]/div[1]/div')

# 인원에 맞게 자리를 선택하면 결제로 넘어가는 버튼이 활성화된다.
# 활성화되면 바로 다음단계로 넘어가게 버튼을 클릭하도록 만든다.
button_element = browser.find_element_by_id("tnb_step_btn_right")

try:
    # btn-right 클래스에서 btn-right on 클래스로 변경될 때까지 대기
    button_on = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@id='tnb_step_btn_right' and contains(@class, 'btn-right on')]"))
    )
    # 버튼이 활성화되면 메시지를 출력.
    print("클릭 가능")
    button_element.click()
except:
    print("버튼이 활성화되지 않됨")

time.sleep(1)
browser.find_element_by_xpath('//*[@id="discCoupon"]/div[1]').click()

#cgv사용가능 쿠폰 확인
coupon=browser.find_element_by_id('cgvCoupon').find_element_by_class_name('content')
coupon_list=coupon.find_elements_by_tag_name('li')

if coupon_list:
    for i in range(adult_people+youth_people):
        coupon_list[i].click()
        browser.implicitly_wait(3)
        
        if (len(coupon_list)-(i+1))==0:
            break
try:
        WebDriverWait(browser,2).until(EC.alert_is_present())
        alert=browser.switch_to.alert

        alert.dismiss()
        alert.accept()       
except:
        "there is no alert"

browser.find_element_by_id('last_pay_radio3').click()

#대중적인 카카오페이로 선택
browser.find_element_by_id('payKakao_btn').click()
browser.implicitly_wait(1)
browser.find_element_by_id('tnb_step_btn_right').click()
time.sleep(1)

browser.find_element_by_id('agreementAll').click()
time.sleep(1)
browser.find_element_by_id('resvConfirm').click()
browser.implicitly_wait(1)
browser.find_element_by_class_name('reservation').click()

while(True):
    pass

