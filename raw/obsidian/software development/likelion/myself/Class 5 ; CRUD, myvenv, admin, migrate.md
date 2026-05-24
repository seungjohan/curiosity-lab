---
category:
  - study
type:
  - programming
  - software development
software:
  - crud
  - django
date: ""
tags:
  - likelion
  - programming
link:
---

#### related


# Topic
- Bootstrap
- CRUD
- myvenv
- admin
- migrate

## Body


Bootstrap
- Copy the css, jQuery and paste in the </head> tag

CRUD
- Creat + Read + Update + Delete
- 블로그 기본 요소, 스펙

MTY

- model까지 활용하여 CRUD를 구현해볼 예정

[Models.py](http://models.py) =/ 생산공장

- 데이터의 틀 // html은 화면구성의 틀
- Database를 다룸



```bash
class app_name(models.Model):
	user_id
	title
	pub_date
	body = (데이터의 형식 정하기)
```

- python 에서 class, import에 대한 선수 지식 필요

Admin

- 데이터를 관리할 수 있는 권한을 가진 유저
- [urls.py](http://urls.py) 맨 상단에 admin이 위치
- 아이디/비밀번호 typing → admin사이트에 접속

가상환경 설정

activate 실행하기

장고설치

migrate하기


``` bash
python manage.py makemigrations //manage.py 가 있는 폴더안으로

python manage.py migrate
```

[settings.py](http://settings.py) 설정 - dir 설정

vscode ! + tab 치면 기본양식 나옴

```bash
{% extends 'base.html' %}

{% block contents %}
{% endblock %}
```

[views.py](http://views.py)

```bash
def home(request):
	return render(request, )
```

Boot strape에서 가져오기

- CDN에서 가져와서 씀, 우리는 class를 만든 적은 없지만 url을 가져와서 외부개발자가 만들것들을 가져다 씀.
- </head>, </body>에 넣든 상관은 없지만 의미성

admin 계정 만들기

- urls.py의 admin

```bash
$ python manage.py createsuperuser
```

[models.py](http://models.py)

```bash
class Blog(models.Model):
    title = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
    post = models.TextField()
```

admin site에 등록을 해야 변화가 생김 in [admin.py](http://admin.py)

```bash
admin.site.register(Blog)
```

models.py를 수정해줄 때마다 makemigrations, migrate를 해줘야함

- django와 DB가 서로 상호호완되어 연동되어있는데 models.py를 수정해주게 되면 DB에 수정된 것을 연결해주기 위해 장고안에 makemigrations를 하고 migrate를 함으로써 서로 연동하게 된다.

blogpost의 title를 바꿔주기 위해

```bash
def __str__(self):
        return self.title
후

python manage.py makemigrations
python manage.py migrate

//no changes detected지만 제목변경됨
```

만든 post를 home.html에 표현

- home에 게시물을 만들고 가져올 것이다.

```bash
blogs = Blog.objects #쿼리셋, 메소드

//Blog는 models.py의 class명
```

models.py안에 blog생성

views.py안에 blogs임시 생성

tuple의 key, value 값을 지정 → html파일과 연결

```bash
return render(request, 'home.html', {'blogs' : blogs})
```

그리고 blog를 models.py에서 가져온다

```bash
from .models import Blog
```

쿼리셋과 메소드에 대해서 알아야 한다.

쿼리셋 = 모델(Blog)을 object(객체)의 목록 가져온다

home.html에서 for문을 돌리는이유

- blogs라는 key값을 가져오는데 models.py생성 , object생성 후 모두 가져옴.
- 처음부터 끝까지 반복문을 돌림
- object에는 title, date, body같은 것들이 있었음.

```bash
{% for blog in blogs.all %}
    {{blog.title}}
    {{blog.pub_date}}
    {{blog.body}}

    {% endfor %}
```

