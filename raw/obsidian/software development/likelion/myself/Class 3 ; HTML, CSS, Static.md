---
category:
  - study
type:
  - programming
  - software development
software:
  - html
  - css
  - markdown
date: ""
tags:
  - likelion
  - programming
link:
---

#### related



# Topic
- HTML
- CSS
- Bootstrap
- Overriding

## Body
Markdown

= Markup Language Library

[README.md](http://readme.md) (= markdown)

- 구글에 치면 다양함. h1, table 등 다양한 태그로 감싸져있음.

### HTML

<meta charset="UTF-8">

인코딩에 도움을 줌. 한글깨짐을 방지

<meta name="viewport">

핸드폰에서 봐도 웹페이지처럼 보여짐, 화면에 맞춰 조정하는 역할

### CSS

= Cascading Style Sheet

```html
<link rel = "stylesheet" type = "text/css" href="style.css">
```

npm

BootstrapCDN

### Bootstrap overriding

#### HTML - CSS

base.html

```html
STATIC_URL = '/static/'
STATICFILES_DIRS = {
	os.path.join(BASE_DIR, 'likelion', 'static'),
}
STATIC_ROOT = "/staticfiles/"
```

static들을 전부 한곳으로 모아주어야한다.

→ static/likelion/ css 폴더를 생성해주고 style.css를 만들어준다.

그리고 css 말고 /img폴더를 생성해주고 IMG파일을 넣어준다.

<base.html>

```html
<head>
{% load static %}

<link rel = "stylesheet" type = "text/css" href = "{% static 'likelion/css/style.css' %}" >

여기서 static을 써준건 settings.py 에서 static위치를 알 수 있기 때문에 거기서 가져온다는 의미

```

<index.html>

```html
<img src = "{% static 'likelion/img/img이름' %}">
```

```html
<div class = "nav"> // nav bar
	<div id = "logo">
		<img src="#" />
	</div>

	<ul class "right-nav">
	</ul>
	<ol>
		<li>HOME</li>
		<li>HISTORY</li>
		<li>WHAT</li>
	</ol>
</div>
```

reset CSS

- style.css 맨 위에 내가 먹이지 않은 css를 다 없앨 수 있다.

```html
@import url=("<https://fonts.google.com/specimen/Roboto>")

.nav {
	height: 50px;
	background : red;
	display: flex;
	justify-contents: center; //위치를 center에 조정
	
	
}

.nav.right-nav {
	background: yellow;
	color: black;
	display: flex;
}
```

display : flex; 개념을 알아보자

- right-nav를 nav에 flex해준다. 먹여주면 그거에 맞게 사이즈 조정이 된다.

글씨 먹여주려면

```html
<li class="classname">
```

```html
.nav.right-nav.nav-items {
	margin: 20px; //전체를 다 둘러싸주겠다.
	margin-top: 20px; //top, bottom 따로 설정하고 싶으면 이렇게
	margin-bottom: 30px;
}
```