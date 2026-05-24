---
category:
  - study
type:
  - programming
  - software development
topic: 
software:
  - github
  - crud
date: ""
tags:
  - likelion
  - programming
link:
---

#### related



# Topic
- Github
- CRUD

## Body

Review all the Sessions

Github / commit message

- It's important to set the commit message rule
- like a title →

MTV(Model Template View) patterns

- Template ; 사용자에게 보여지는 부분
- Model ; 데이터를 담당하는 부분 (DB)
- View ; 로직, 처리, 연산

client → url "/" request: → View →←(1) Model ~ DB →(2) Template

CRUD (Create Read Update Delete)

1. 폴더 만들기
2. 가상환경 만들기
3. 가상환경 실행
4. python -m venv myvenv

source myvenv/Scripts/activate

pip install django

1. 프로젝트 생성

django admin startproject.blog

cd blog

ls

기능을 하는 앱 하나 생성

python [manage.py](http://manage.py) startapp blogpost(블로그명)

앱이 만들어졌다는 것을 등록

python [manage.py](http://manage.py) makemigrations

python [manage.py](http://manage.py) migrate

bloglist

(파스칼 케이스) BlogList

(카멜 케이스) blogList

(스네이크 케이스) blog_list

(케밥 케이스) blog-list

= 서로 약속을 지켜서 짤 것

get 과 post의 차이

- get → url을 통해 접근, url상에서 조회 가능
- post →