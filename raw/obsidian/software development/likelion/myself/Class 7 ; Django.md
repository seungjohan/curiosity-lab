---
category:
  - study
type:
  - programming
  - software development
software:
  - django
date: ""
tags:
  - likelion
  - programming
link:
---

#### related



# Topic

## Body

### 가상 환경 만들고 활성화 하기

```bash
python3 -m venv myvenv

source myvenv/bin/activatess
```

### 장고 설치

```bash
pip install django
```

### 새로운 프로젝트 시작하기

```bash
django-admin startproject 프로젝트 이름
```

ls : 현재 본인이 속한 폴더 내의 모든 하위 폴더의 이름을 보여줌

cd name : name이라는 이름의 하위 폴더로 이동

cd .. : 현재 속한 폴더의 한단계 상위 폴더로 이동

위의 커맨드를 익혀 현재 본인이 속한 폴더의 위치를 파악하는 것이 중요

[manage.py](http://manage.py) 파일이 있는 폴더 안에 본인이 속하도록 하자


### 새로운 앱 만들기

```bash
python3 manage.py startapp djangoStart
```


### 새로운 앱 등록하기

```bash
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'djangoStart.apps.StartDjangoConfig', #startapp 이후에 등록했던 앱 이름만 넣어도 됨 'myapp' 이렇게 넣기만 해도 됨
]
```

settings.py에 새롭게 만든 앱 추가 해주어야 함

```bash
python3 manage.py runserver # 서버 실행 시킬 때
```


### MTV 구현

1. apps 폴더에 templates 폴더 생성
2. 화면에 띄울 .html 파일 생성
3. views.py에 새로 만들 템플릿들 띄우는 함수 작성
    ```bash
def home(request):
	return render(request, 'home.html')

# 또다른 파일 추가 할 때 마다 생성
def profile(request):
	return render(request, 'profile.html')
    ```
   
4. urls.py에 경로 추가
    ```bash
 from django.contrib import admin
 from django.urls import path
 import djangoStart.views ## added code
 
 urlpatterns = [
	path('admin/', admin.site.urls),
	path('', djangoStart.view.home, name="home"), #added code
	path('profile/', djangoStart.view.profile, name="profile"), #added code
 ]
    ```
   
5. python3 [manage.py](http://manage.py) runserver 실행

    ```bash
 python3 manage.py runserver
    ```

// model 을 건들 때 마다 migrations 와 migrate 해줘야 함
// app을 두개이상 생생해도 urls.py에서 모두 받아줌
// base.html 은 template 상속을 위해서 생성 해준다

### base.html

```bash
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>두번째 실습</title>
    <h1>두번째 실습 사이트</h1>
</head>

<body> # 계속 변하는 부분.. 따라서 아래의 템플릿을 다른 화면에도 써 주어야 한다. 
    {% block contents %}
    {% endblock %}
</body>

<footer>
    <h5><a href="{% url 'home' %}">이걸 누르면 home으로 넘어갑니다.</a></h5>
</footer>
</html>
```

모든 페이지에 보여주기 위한 base.html이다

base.html 을 적용 시키기 위해 settings.py에서 'DIRS': [],에 'myproject/templates'를 추가 해준다 # DIRS: ['myproject/templates']

```bash
{% extends 'base.html' %} # base.html에서 설정된 것을 이 화면에도 적용시킬 것이다.

<body>
    {% block contents %} # base.html에서 설정한 템플릿을 이 화면에도 사용하였다.

    <h1>이곳은 home.html 입니다!</h1>
    <h3>hello</h3>
    <h5><a href="{% url 'profile' %}">이걸 누르면 profile로 넘어갑니다.</a></h5>

    {% endblock %}
</body>

```

terminal >> crl + C 하면 가상 환경 끌 수 있음

app 새로 추가 하면 건들것

[settings.p](http://settings.py)y 에서 installed apps 에서 추가 해주기

[urls.py](http://urls.py) 에서 해당 appname.views import 해주기

[urls.py](http://urls.py) 에서 해당 url path를 추가

[views.py](http://views.py) 에서 render 추가

1. 폴더 만들기
2. myvenv 생성하기
3. myvenv가 존재하는 폴더에 프로젝트 생성
4. myvenv가 존재하는 폴더에 프로젝트를 생성하면 내부에 [manage.py](http://manage.py) 파일이 생성되고, myproject 폴더도 같이 생성 된다.

urls.py에서 path 추가 할 때, 나중에 너무 많아져서 앱 별로 urls.py를 만들어서 그 urls.py를 가장 상위의 urls.py에 include 해준다.

urls import하는 작업 좀 더 깔끔하게 정리하기 위함... 반드시 필요한 작업은 아니고 깔끔하게 하기 위함

상위 [urls.py](http://urls.py) [//](//my) myproject 전체 [urls.py](http://urls.py)

```c
from django.contrib import admin
from django.urls import path, include
import myapp.views
import portfolio.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('portfolio/', portfolio.views.portfolio, name="portfolio"),
]
```

[myapp.urls.py](http://myapp.urls.py)

```c
from django.contrib import admin
from django.urls import path
import myapp.views 
#from .import views

urlpatterns = [
    path('', myapp.views.home, name="home"),
    path('profile/', myapp.views.profile, name="profile"),
]
```