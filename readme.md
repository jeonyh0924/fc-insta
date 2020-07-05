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

### 깃 전략 세우기 [링크](https://blog.naver.com/PostView.nhn?blogId=tmondev&logNo=220763012361&redirect=Dlog)

### 깃 라벨 커스텀 [링크](https://github.com/ManageIQ/guides/blob/master/labels.md)

### 깃 마일드스톤 [링크](https://cyberx.tistory.com/112)

### 깃 브랜치 네이밍 [링크](https://gist.github.com/digitaljhelms/4287848)


####  피드백
> 전체적인 틀을 세우는게 제일 중요하다. 기능을 명세하고, API 문서를 만들어야 한다. 
> 전체적으로 프로젝트를 시작 할 때 코딩을 먼저 시작하면 안된다. 시야가 좁아지고 하나의 기능에 집착하며 프로젝트 중에 기존에 했던 코드를 자꾸 되돌아 가게 된다.
