---
category:
  - study
type:
  - programming
  - software development
software:
  - html
date: ""
tags:
  - likelion
  - programming
link:
---
#### related



# Topic
All the flow

## Body

(웹)프론트, 서버 (앱)ios,안드로이드

sopt, sw maestro // 넥스터즈, 프로그라피

html, css → 코드카데미(1~2주)

Django → 게시글, 댓글, 유저 회원가입 로그인, 공유, 좋아요, 조회수 등등... A 프로젝트

AWS ElasticBeanstalk 배포

A 프로젝트 개선하고, 리팩토링 등등의 수정사항을 반영해 재배포

프론트엔드 - React.js(어렵지만,대규모 어플리케이션에 좋음, React Native), Vue.js(스타트업, 쉽고 기능이 많고 빠르게 개발 가능), Angular

Vue.js → todo app(CRUD), Vuetify, Materalize

Vanilla JS → 순수 자바스크립트, 꼭 공부해야 함...!

서버 → Django Rest framework(서버 API 구성, REST API)

(유저 생성) [POST] 주소~/user/createUser

(유저 삭제) [POST] 주소~/user/deleteUser

⇒ REST API X

(유저 생성) [POST] 주소~/user

(유저 삭제) [DELETE] 주소~/user

(유저 갱신) [PUT, PATCH] 주소~/user/3

(유저 조회) [GET] 주소~/user

주소~~~/user/2

프론트 ↔ json(javascript obejct notation)

```python
{ "key" : "value }
```

(문서화 예시)

유저 생성

url : [http://~/user](http://~/user) [POST]

request data example

```python
{
	name: "승조",	
	age: "24",
	hobbies: [ { "1순위": "soccer"} , {"2순위" : "basketball" } ]
}

response success example

{
	responseMsg: "SUCCESS"
}
```