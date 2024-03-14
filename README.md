# CGV-IMAX-Movie-reservation-program
## 📚 셀레니움을 이용한 영화 자동 예매 프로그램 만들기

개발 기간: 1달 

개발 언어: <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">

## 💻 프로젝트 소개
- 학부 수업 때 만든 프로젝트를 2024.03.14일 업이트한 버전입니다.
- CGV IMAX 특별관 전용으로 만들었습니다.->IMAX 특별관이 있는 영화관만을 선택할 수 있습니다.
- 좌석 선택을 제외한 cvg홈페이지 오픈부터 카카오페이로 결제 QR코드가 나오기까지를 자동화시켰습니다.
- 안타깝게도 영화시간대 선택은 불가능합니다. 단, 저녁 시간대로 임의 지정하였습니다.

## ⚠ 실행 전 주의 사항
- https://chromedriver.chromium.org/downloads 에서 크롬 버전에 맞는 Chrome driver를 설치해야 합니다.
- 크롬 버전 확인하는 법: 크롬실행-> 브라우저 오른쪽 상단의 점 세개 클릭-> 도움말-> Chrome 정보
- 다운로드한 Chrome driver 압축을 풀고 CGV IMAX Movie reservation program.py과 같은 디렉토리에 위치시켜야 합니다.
- Selenium과 Beautifulsoup4을 설치해야 합니다.
  
  prompt실행 후
  ```
  pip install selenium
  pip install bs4
  ```

## 결과 영상
![video1909524590](https://github.com/SeungHuiHan/CGV-IMAX-Movie-reservation-program/assets/98226400/0745ff11-4c4d-499b-a18f-593352725bc0)

## 주요 코드 설명
```python
theater='CGV영등포' #영화관 선택 (IMAX 전용)
date=datetime.strptime("20240314", "%Y%m%d") #예매 희망 날짜, 단 현재부터 2주 이내
title='듄-파트2'#영화 제목
#어른,청소년 포함최대 8명까지
adult_people=1 #일반 예매 인원(경로,우대 안됨) 
youth_people=1 #청소년 예매 인원
```
- IMAX 전용 예매 프로그램으로 IMAX 특별관이 있는 영화관만 선택가능합니다.
- 예매 희망날짜를 입력합니다. (ex. 2024년 3월 14일->20230314)
- 단 현재 날짜의 2주 이내 날짜만 가능합니다.
- 영화 제목은 CVG 홈페이지에 나와있는 제목 그대로 적어야 합니다.(ex. 네이버엔 듄: 파트 2라 나오지만 CVG 홈페이지에는 듄-파트 2라 나옴)
- 안원은 어른, 청소년 포함 최대 8명까지 가능합니다.
- 경로, 장애 우대는 불가능합니다.

```python
browser.find_element_by_name('txtUserId').send_keys('*****') #아이디 입력
browser.find_element_by_name('txtPassword').send_keys('****') #비밀번호 입력
```
- 첫번째 .send_keys('*****')의 *****에 아이디를 입력합니다.
- 두번쨰 .send_keys('*****')의 *****에 비밀번호를 입력합니다.

```python
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
```
- 현재 페이지에 희망 선택날짜가 없다면 next버튼을 눌러 날짜를 이동합니다.
![cvg 영화 예매 날짜 선택](https://github.com/SeungHuiHan/CGV-IMAX-Movie-reservation-program/assets/98226400/cb9bbaa2-4838-467a-b985-04147e82c647)

```python
while True:  #영화가 해당날짜에 없으면 나올때까지 무한 클릭
    title_one=soup.find(class_="sect-showtimes").text #영화 리스트
    
    if title in title_one:
        break
    else:
        browser.find_element_by_partial_link_text(date_1).click()
        browser.implicitly_wait(1)
```
- 희망날짜에 영화가 뜨지 않았다면 상영정보가 뜰 때까지 무한 클릭 합니다.
![cvg 영화 예매 날짜 무힌 클릭](https://github.com/SeungHuiHan/CGV-IMAX-Movie-reservation-program/assets/98226400/4bbe9d65-1581-4acd-b790-afc66267bc7b)

``` python
 if len(li)<=2: #영화 시간 임의 선택할 수 없음(대략 오후3시~7시 사이 상영작)
            li[len(li)-1].click()
        elif len(li)<=4:
            li[len(li)-2].click()
        elif len(li)>=5:
            li[len(li)-3].click()
        break
```
- 영화 시간을 선택할 수 없습니다.
- 대신 저녁 인기 있는 시간을 임의로 선택합니다. (오후 3~7시 사이)

```pyhton
popup_check1=WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.LINK_TEXT, "닫기")))
popup_button1=browser.find_elements_by_link_text('닫기')[0]
popup_button1.click()
```
- 영화 좌석을 선택하기 전에 팝업이 뜨면 팝업을 닫아줍니다.
- 상황에 따라 팝업이 여러 개 뜰 때가 있으므로 사전에 직접 홈페이지에 들어가 팝업 개수를 확인합니다.
- 팝업 개개수에 따라 위 코드를 추가하면 됩니다. (ex. 팝업 2개- 위 코드를 두번 적어줌)
![cvg 영화 예먀 좌석선택전 팝업](https://github.com/SeungHuiHan/CGV-IMAX-Movie-reservation-program/assets/98226400/562e8799-1c3a-497e-922e-6591df155d67)

  ```python
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
    print("버튼이 활성화되지 안됨"
  ```
  - 인원에 맞게 좌석을 선택했다면 바로 다음 결제방식 단계로 넘어갑니다.
![cvg 영화 예먀 좌석선택후 넘어가기 버튼](https://github.com/SeungHuiHan/CGV-IMAX-Movie-reservation-program/assets/98226400/fd21ca0e-be21-4caf-bb36-a834e7fbabc1)

  ```python
  #간편결제로 선택
  browser.find_element_by_id('last_pay_radio3').click()

  #대중적인 카카오페이로 선택
  browser.find_element_by_id('payKakao_btn').click()
  ```
  - 결제 방식은 간편하고 대중적인 카카오페이로 선택하였습니다.
  - 원하는 결제 방식을 바꿀 수 있습니다.
  - 결제 방식 바꾸는 방법: 개발자도구에서 원하는 결제 방식의 id가 뭔지 확인하고 .find_element_by_id('')에 집에 넣기
  - (ex. 네이버페이로 바꾸고 싶음->  browser.find_element_by_id('naverPay_btn') 바꿈
    ![cvg 영화 예매 최종결제수단](https://github.com/SeungHuiHan/CGV-IMAX-Movie-reservation-program/assets/98226400/dea2b3ee-95b1-4836-8b19-6b2798e035d7)
