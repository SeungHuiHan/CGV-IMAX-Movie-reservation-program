# CGV-IMAX-Movie-reservation-program
## 📚 셀레니움을 이용한 영화 자동 예매 프로그램 만들기

개발 기간: 1달 

개발 언어: <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">

## 🔍 미리 보기
- [프로젝트 소개](#프로젝트-소개)
- [실행 전 주의 사항](#실행-전-주의-사항)
- [실행 영상](#실행-영상)
- [주요 코드 설명](#주요-코드-설명)
- [프로젝트를 하며 느낀점](#프로젝트를-하며-느낀점)

## 💻 프로젝트 소개
- 학부 수업 때 만든 프로젝트를 2024.03.14일 업데이트한 버전입니다.
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

## 🎞 실행 영상
![video1909524590](https://github.com/SeungHuiHan/CGV-IMAX-Movie-reservation-program/assets/98226400/0745ff11-4c4d-499b-a18f-593352725bc0)

## 📝 주요 코드 설명
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
![cvg 영화 예먀 좌석선택전 팝업1](https://github.com/SeungHuiHan/CGV-IMAX-Movie-reservation-program/assets/98226400/232b5a66-bb68-49fa-8927-8cd9e494ce26)


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
![cvg 영화 예먀 좌석선택후 넘어가기 버튼](https://github.com/SeungHuiHan/CGV-IMAX-Movie-rese클론하기 등이 있다.

나는 실생활에서 나에게 도움이 되는 프로젝트를 하고 싶었다. 이 당시 나는 마블 영화를 '용아맥'='CGV용산 IMAX'로 영화 보는 것을 좋아했다.

한창 영화표 예매가 콘서트 티켓팅을 방불케 하는 상황이 있었다. 이때 나는 프로그램을 짜서 자동으로 티켓팅을 할 수 없을까 생각하다가 매크로를 직접 만들었다!

프로젝트하면서 HTML을 처음 접했다. 정말 맨땅에 헤딩 격으로 바닥부터 시작했다. 꼬박 한달동안 만들었다.(이땐 ChatGPT도 없어서 도움받을 곳은 오직 구글링뿐이었다)

가장 많이 본 에러는 NoSuchElementException -> "녱? 너가 찾는 그런 엘리먼트(태그) 없는데요?"라는 에러다. 진짜 돌아버릴 것 같았다. 왜 이런지 문제를 해결하지 못한 채 하루를 마무리 한적도 있었다.

하지만 한달 내내 매달린 결과 프로젝트를 완성했다^-^ 다음은 내가 가장 애먹은 부분과 해결방법이다.

- NoSuchElementException의 주된 원인은 iframe이었다. 쉽게 말하면 페이지 안에 페이지이다. ifrmae안에 속하는 요소를 찾고 싶으면 iframe 창으로 전환해야 한다.
```python
iframe1 = browser.find_element_by_id("ticket_iframe") 
browser.switch_to.frame(iframe1)
```
요소가 있는 iframe 창으로 변환해 줬다.

- 시야를 text, id나 class만 국한되어있지 말고 같은 태크 안에서 다른 방법을 찾을 것.
  
  browser.find_elements_by_link_text("IMAX")가 계속 못 찾아서 애를 먹었다. 분명 text는 눈에 보인다...
  
  같은 요소에  clss="imax" 있어서 browser.find_element_by_class_name("imax").click()로 작성했더니 성공했다. 이렇게 방법은 여러가지니 한가지에 매몰되지 말 것
  
- 무조건 명시적 대기, 암시적 대기가 답이 아니다. 상황에 따라 time.sleep, browser.implicitly_wait(10), WebDriverWait(browser, 10) 적절하게 사용하기
  
  코드를 짜면서 .implicitly_wait(10)이 페이지 로딩이 끝나면 10초 다 기다릴 필요 없이 다음 명령어를 수행하므로 10초 다 기다리는 time.sleep(10)보다 좋은 메서드라고 생각했었다.
  
  하지만 implicitly_wait를 사용하면 NoSuchElementException에러가 나는데 time.sleep를 사용하면 에러가 안나는 것을 보고 적절하게 사용하는 게 중요하다는 것을 알았다.
  

아쉬운 점이 있다면 자리 자동선택은 구현하기 힘들다는 점이었다. 사람마다 선호하는 자리와 잔여좌석 상황이 다르니까 힘든 것도 있다. 시간이 난다면 계속 구현을 시도해 볼 것이다.
