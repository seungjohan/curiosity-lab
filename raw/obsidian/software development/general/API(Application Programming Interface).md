---
category:
  - study
type:
  - software development
topic:
  - api
about: 
date: 2025-04-24
tags:
  - software
  - study
---
#### reference
- API
	- [APIs Explained (in 4 Minutes) - Briefly](https://www.youtube.com/watch?v=bxuYDT-BWaI)
	- [API란? 개념 및 유용한 API들 소개, 날씨 API 자바스크립트 실전 활용 방법](https://youtu.be/pLBJgvC_ZUA?si=kgmxA7t25ZWP71I1)
		- [한시간만에 Node.js 백엔드 기초 끝내기 (ft. API 구축)](https://www.youtube.com/watch?v=Tt_tKhhhJqY)
	- [What is an API (application programming interface)? by IBM](https://www.ibm.com/think/topics/api)
- REST API
	- [REST API Crash Course - Introduction + Full Python API Tutorial](https://www.youtube.com/watch?v=qbLc5a9jdXo)
- [[MCP (Model Context Protocol)]]
	- [MCP vs API: Simplifying AI Agent Integration with External Data by IBM Tech](https://www.youtube.com/watch?v=7j1t3UZA1TY)
		- MCP is the modern API Platform
	- [MCP vs APIs: What’s the Difference?](https://apidog.com/blog/mcp-vs-api/)

# API(Application Programming Interface)
- API (Application Programming Interface)
- Open API
- [[REST API]] (REpresentational State Transfer)


말그래도 Interface역할을 해주는 기능, Application (Front-end) ~ Programming (Back-end)
어떠한 조건에 따라 요청이 들어오면 정보를 주고 받을 수 있다.
UI(User Interface)는 User와 Programming사이에 Interface하는 방식을 UI라고 한다. 이것이 "Interface".

API는 정의 및 프로토콜 집합을 사용하여 두 소프트웨어 구성 요소가 서로 통신할 수 있게 하는 메커니즘입니다. 예를 들어, 기상청의 소프트웨어 시스템에는 일일 기상 데이터가 들어 있습니다. 휴대폰의 날씨 앱은 API를 통해 이 시스템과 ‘대화’하여 휴대폰에 매일 최신 날씨 정보를 표시합니다.

API stands for Application Programming Interface. In the context of APIs, the word Application refers to any software with a distinct function. Interface can be thought of as a contract of service **between two applications**. This contract defines how the two communicate with each other **using requests and responses**. Their API documentation contains information on how developers are to structure those requests and responses.

API architecture is usually explained in terms of **client** and **server**. **The application sending the request is called the ==client==, and the application sending the response is called the ==server==**. So in the weather example, the bureau’s weather database is the server, and the mobile app is the client. 

There are four different ways that APIs can work depending on when and why they were created.


request
- GET
- POST
response
- JSON
	- AJAX
- [Fetch method](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

- Auth
- HTTPS
- CORS
	- Proxy Server



#### examples
- 차량 공유 앱에서 승차 거리와 시간을 계산하는 것 👉 API의 기능
- 차량 공유 앱에서 드라이버가 픽업 위치에 도착했음을 SMS로 알 수 있는 것 👉 API의 기능
- Apple Device Weather application ~ Data from Weather.io 