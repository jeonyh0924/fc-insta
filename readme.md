# PBS 13 : 인스타그램 실습
----

## Technologies
- python 3.8.2
- django 3.0.7


## SetUp
```shell
pyenv virtualenv <python V> <VE name>
pyenv local <VE name>

pip install - requirement.txt

```

```python
# ROOT/.env
DB_HOST=localhost
DB_NAME=fc-insta
DB_USER=postgres
DB_PASSWORD=
DB_PORT=5432
```


### 기능 구현 내용

- 유저 CRUD ( ModelViewSet - CRUD, login, logout, follow, follower, block, create_delete_Relation)

- 유저 Model (AbstractBaseUser, BaseUserManager, property- follow, follower, block)

- 유저 OTO Relation Create

- 유저 testcode ( CRUD, login, logout, profile CU)

### 깃 전략 세우기 [링크](https://blog.naver.com/PostView.nhn?blogId=tmondev&logNo=220763012361&redirect=Dlog)

### 깃 라벨 커스텀 [링크](https://github.com/ManageIQ/guides/blob/master/labels.md)

### 깃 마일드스톤 [링크](https://cyberx.tistory.com/112)

### 깃 브랜치 네이밍 [링크](https://gist.github.com/digitaljhelms/4287848)


####  피드백
> 전체적인 틀을 세우는게 제일 중요하다. 기능을 명세하고, API 문서를 만들어야 한다. 
> 전체적으로 프로젝트를 시작 할 때 코딩을 먼저 시작하면 안된다. 시야가 좁아지고 하나의 기능에 집착하며 프로젝트 중에 기존에 했던 코드를 자꾸 되돌아 가게 된다.

> 크롤링 빠르게 --> 테라폼

### Agile 방법 개발론
- 소프트웨어 사용자가 일반 대중으로 변화되면서 (Bto B >> Bto C)
- 소프트웨어 개발의 불확실성이 높아지며 경량 방법론 주의자가 늘어남( 프로젝트가 시작 시 상용화를 빠르게 한 뒤 꾸준히 업데이트)
- 문서화를 시키는 것 보다 프로토 타입의 배포를 더 우선시
- 협력과 피드백 (핵심가치)

#### media
[링크](https://ssungkang.tistory.com/entry/Django-media-%ED%8C%8C%EC%9D%BC-%EC%97%85%EB%A1%9C%EB%93%9C%ED%95%98%EA%B8%B0)
