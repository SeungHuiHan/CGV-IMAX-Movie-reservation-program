# CGV-IMAX-Movie-reservation-program
## 📚 셀레니움을 이용한 영화 자동 예매 프로그램 만들기

개발 기간: 1달 

개발 언어: <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">

## 💻 프로젝트 소개
- 학부 수업 때 만든 프로젝트를 2024.03.14일 업테이트한 버전입니다.
- CGV Imax 영화관 전용으로 만들었습니다.
- 좌석 선택을 제외한 cvg홈페이지 열기부터 카카오페이로 결제 QR코드가 나오기까지를 자동화시켰습니다.
- 안타깝게도 영화시간대 선택은 불가능합니다. 단, 저녁 시간대로 임의 지정하였습니다.

## ⚠ 실행 전 주의 사항
- https://chromedriver.chromium.org/downloads 에서 크롬 버전에 맞는 Chrome driver를 설치해야 합니다.
- 크롬 버전 확인하는 법: 크롬실행-> 브라우저 오른쪽 상단의 점 세개 클릭-> 도움말-> Chrome 정보
- 다운로드 받은 Chrome driver를 압축을 풀고 CGV IMAX Movie reservation program.py과 같은 디렉토리에 위치시켜야 합니다.
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
