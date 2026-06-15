---
category:
  - study
type:
  - programming
  - software development
software:
  - python
  - django
date: ""
tags:
  - likelion
  - programming
link:
---

#### related



# Topic
- ideat pitching
- Djangjo

## Body

Idea Pitching

- 올빼미 버스

막차 후 교통에 대한 서비스 특히, 귀가시간이 오래걸리는 사람들 대상

길 찾기 서비스 추가

수요예측의 어려움 -> 수요형 대중교통 서비스

- 자신의 피부타입, 나에게 맞는 성분 분석 등 안성맞춤 화장품 서비스 -> 화장품다이어리
- Youtube 운영할 때 배경음악의 선택폭이 굉장히 좁다. Milliwon kim
- 롱보드 플랫폼

롱보드에 대한 정보의 부족

롱보드 스팟 공유 기능

롱보드 구매 기능

스팟별, 태그 모아보기

---
<04.04>

- WEB(World Wide Web)

웹 프로젝트

- 큰 기능들을 하나씩 만들어나가기
- 계획이 없으면 우후죽순으로 생겨나가게 된다

Browser = not client, server but user, Web Client

->

Front-end

- HTML
- CSS
- JS

Back-end

- Python : programming language
- Django : Framework

Frame + Work; 일정한 뼈대를 가지고 일하다

-> 필요한 기능을 미리 모아서 만들어 놓은 툴

ex) Login, Logout, authentication , Blog, Shopping etc…

- Django_vscode
- Mkdir - open - cd LikeLion_Session_2

(Make Directory, commend

- Python --version // python version check
- Python -m venv (가상환경이름 myvenv) // 가상환경만들기
- Source myvenv//Scripts//activate (activate 주소)안에 있는 activate를 실행시키기
- Pip install django // 가상환경만들 때마다 django를 계속 만들어줘야함 But 버전관리하기가 힘들어서 매번 가상환경을 만들 때마다 장고를 다운받는 걸 추천
- Django-admin startproject (프로젝트명 seungjo) //프로젝트만들기
- Python (파일명).py runserver // 로켓이 보여야함
- Ls // 어떤 파일안으로 들어갈 수 있는지, manage.py파일이 있는지를 확인하는 작업
- Cd seungjo // change directory , 폴더로 이동

Cd seungjo // 가장 하위폴더로 이동, cd .. // 다시 원상복귀

- Ctrl + c // 돌리지 않게 됨.
- Python [manage.py](http://manage.py) startapp (filename session_2) //
- Make the ‘Templates’ folder
- And make the file ‘index.html
- “Session_2”
- [View.py](http://View.py) -> html파일을 보여줄거야, 장고에게 확인 ->

def index(request):

return render(request, 'index.html')

- Url 연결하기 , [urls.py](http://urls.py) -> url 설정(마지막부분)

from django.contrib import admin

from django.urls import path

import session_2.views

urlpatterns = [

path('admin/', admin.site.urls),

path('', session_2.views.index, name="index")

Admin페이지를 따로 만들필요 x // django의 장점

- Python [manage.py](http://manage.py) makemigrations // model 연결
- Python [mange.py](http://mange.py) migrate // update
- Source myvenv/scripts/activate // 가상환경접근
- Python [manage.py](http://manage.py) runserver // 로켓이 보이면 안됨

Python 은 하나의 버전만 다운가능

-> 웹을 만들 때 a는 a’ 버전으로 b는 b’버전으로 만들었다면

=>가상환경을 만드는 이유

- GitHub
- ‘...’ 있고 없고의 차이 // commit template을 적용한지 안한지
- pull request // 어떤 부분이 추가삭제되었는지 확인가능
- Reference
	- django 가상환경으로 장고시작
	  [https://siner308.github.io/2019/01/12/django-virtualenv-ko/](https://siner308.github.io/2019/01/12/django-virtualenv-ko/)
	- 깃허브 브랜치기초
	  [https://blog.yena.io/studynote/2017/12/08/GitHub-Branch.html](https://blog.yena.io/studynote/2017/12/08/GitHub-Branch.html)
	- Git: Merge Branch into Master
	  [https://stackabuse.com/git-merge-branch-into-master/](https://stackabuse.com/git-merge-branch-into-master/)
	- git project 에 [read.me](http://read.me) 작성하기
	  [https://ndb796.tistory.com/194](https://ndb796.tistory.com/194)
	  [https://velog.io/@hyeong412/Django-장고-프로젝트-만들기-1-장고란-프로젝트-만들기-전-알면-좋은-것들-skk42pj209](https://velog.io/@hyeong412/Django-%EC%9E%A5%EA%B3%A0-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EB%A7%8C%EB%93%A4%EA%B8%B0-1-%EC%9E%A5%EA%B3%A0%EB%9E%80-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EB%A7%8C%EB%93%A4%EA%B8%B0-%EC%A0%84-%EC%95%8C%EB%A9%B4-%EC%A2%8B%EC%9D%80-%EA%B2%83%EB%93%A4-skk42pj209)

-- <04.08> --

Django

활성화시키기 - activate

[Settings.py](http://Settings.py) - Add the ‘app_name’

- 장고의 작동흐름
- MTV //
- Sequence

Request ; 데이터요청

- Db가 할 일을 하면서 데이터를 넘겨줌
- Mtv사이에 View의 함수가 왔다갔다함.
- 앱은 myproject 밖에 만들어줘야
- [manage.py](http://manage.py)

Model을 건드릴 때마다 migration, add name 붙여주기 를 해줘야함.(이 부분에서 에러 자주 발생)

- [Settings.py](http://Settings.py)
- [View.py](http://View.py)

함수를 넣음.

- Templates

폴더를 하나 생성 / 대표적 : html

Url include

App들이 많아지게 되면