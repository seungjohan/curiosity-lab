---
category:
  - study
type:
  - programming
  - software development
software:
  - server
date: ""
tags:
  - likelion
  - programming
link:
---
#### related



# Topic
- Server

## Body
### Server

1. hardware

- component - HTML, css, js...

2. software

- IAAS
- PAAS

heroku

- 서비스를 배포해줄 때 도와줄 플랫폼
- python —version

→ heroku에서 사용하는 python버전을 확인해줘야함!!

```python
wev: gunicorn myproject.wsgi
```

→ 브라우저상에서 자동으로 runserver해줄 수 있는 역할

Heroku에서는 DB를 postgreSQL을 사용

```python
DEBUG = FALSE
```

해서 allowed-host에게만 보여질 수 있도록 설정하는 것

debug = True 가 되면 에러가 났을 때 웹상에서 공개가 된다. 배포된 웹을 배포할 때

지정해주지 않는 화면에서는 보이지 않도록!!

git에 모든 걸 굳이 올릴 필요는 없다

```python
touch .gitignore
```