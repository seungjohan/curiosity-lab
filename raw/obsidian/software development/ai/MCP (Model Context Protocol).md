---
category:
  - study
type:
  - software development
topic:
  - ai
  - mcp
about: 
date: 2025-05-01
tags:
  - software
  - ai
  - study
---
#### reference
- https://modelcontextprotocol.io/introduction
- https://docs.anthropic.com/en/docs/agents-and-tools/mcp

- [MCP써야 진짜 Claude다! 500% 활용 튜토리얼 (개념부터 활용까지)](https://www.youtube.com/watch?v=fkqXQOjj8cA)
	- [MCP로 진짜 비서 된 Claude! 로컬 정리 + 드라이브 자동화 (코드 무료 제공)](https://www.youtube.com/watch?v=Pt1tEBCLiCc)
- [MCP by JoCoding](https://youtu.be/46HxP7kO9oY?si=QTmY6u5GDj8ZtJlo)
- [피그마 MCP로 디자인 딸깍 가능?](https://youtu.be/H-yo6dzJ13g?si=QeFIv6FtJi8Vrzx5)
	- [프롬프트로 피그마 디자인 만드는 mcp(cursor-talk-to-figma-mcp)](https://www.figma.com/community/plugin/1485687494525374295/cursor-talk-to-figma-mcp-plugin)
	- [피그마 디자인을 실제 코드로 만드는 mcp(Figma-Context-MCP)](https://github.com/GLips/Figma-Context-MCP)
- [MCP vs API: Simplifying AI Agent Integration with External Data by IBM Technology](https://www.youtube.com/watch?v=7j1t3UZA1TY)
- [Why You Need To Learn About MCP Right Now (Urgent!)  by Nomad Coder](https://www.youtube.com/watch?v=EswVjHZMn74)


- [Task Master MCP](https://www.youtube.com/watch?v=ktr-4JjDsU0)


##### media
- [모르면 실시간 손해? MCP, 딥시크 속도로 빠르게 확산 | 무료 AI 앱 폭발하게 된 MCP, 클로드 커서ai 동반 폭등 | 진짜 에이전트AI 시대 | 샘알트먼 급하게 지원 약속  by 안될공학](https://www.youtube.com/watch?v=Qdu6Sv-NpeU)
- 

# Body
### Difference between [[API(Application Programming Interface)]] and MCP
- https://apidog.com/kr/blog/mcp-vs-api-kr/
- https://medium.com/archetypical-software/%EF%B8%8F-breaking-down-mcp-vs-api-a-friendly-guide-to-software-architecture-c4ad55df1fd5
- https://apidog.com/blog/mcp-vs-api/


```mermaid
sequenceDiagram
    participant User
    participant Host
    participant Client
    participant Server
    participant Resource

    User ->> Host: Open application
    Host ->> Client: Initialize client
    Client ->> Server: initialize request with capabilities
    Server ->> Client: initialize response with capabilities
    Client ->> Server: initialized notification
    User ->> Host: Make a request
    Host ->> Client: Forward request

    alt Resource Request (Application-controlled)
        Note right of Client: A Resource is context data from the server<br>Examples: file contents, code history, database schemas<br>Resources help LLMs understand context
        Client ->> Server: resources/list or resources/read
        Server ->> Resource: Fetch data (e.g., read files, query DB)
        Resource ->> Server: Return data
        Server ->> Client: Resource content
        Client ->> Host: Add context to LLM prompt
    else Tool Execution (Model-controlled)
        Note right of Client: A Tool is a function the LLM can call<br>Examples: web search, file writing, API calls<br>Tools let LLMs take actions
        Client ->> Server: tools/call
        Server ->> Resource: Execute operation
        Resource ->> Server: Return result
        Server ->> Client: Tool result
        Client ->> Host: Show result to LLM
    else Sampling Request (Server-initiated)
        Note right of Server: Sampling lets servers request LLM generations<br>Examples: analyzing data, making decisions<br>Enables agentic/recursive workflows
        Server ->> Client: sampling/createMessage
        Client ->> Host: Request LLM generation
        Host ->> User: Request approval (optional)
        User ->> Host: Approve request
        Host ->> Client: Return generation
        Client ->> Server: Generation result
    end

    Client ->> Host: Return response
    Host ->> User: Display result
    User ->> Host: Close application
    Host ->> Client: Terminate
    Client ->> Server: Disconnect
```




```mermaid
graph TD
    subgraph "Host Application"
        Host[Host Process]
        Client1[MCP Client 1]
        Client2[MCP Client 2]
        Client3[MCP Client 3]
        Host --> Client1
        Host --> Client2
        Host --> Client3
    end

    subgraph "External Processes"
        Server1[MCP Server 1  
Files & Git]
        Server2[MCP Server 2  
Database]
        Server3[MCP Server 3  
External APIs]
    end

    Client1 <--> Server1
    Client2 <--> Server2
    Client3 <--> Server3

```


#### Services that I set up 
- Slack
- Figma
- Firecrawl
- Notion
- Linear
- Puppeteer

- Github
- Cloudflare
- Superbase

- [Task Master](https://www.youtube.com/watch?v=ktr-4JjDsU0)

예전에 카톡에서 매일매일 오늘의 뉴스 뭐 이런거 뿌려주던게 이 기술이였구나 싶다. MCP 이전에, 이미 **Langchain**이라는 기술이 구현을 할 수 있도록 했다. 하지만 MCP는 그 허들을 낮추면서 대중화에 일조하게 되었다.