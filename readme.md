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

### 깃 전략 세우기 [링크](https://blog.naver.com/PostView.nhn?blogId=tmondev&logNo=220763012361&redirect=Dlog)

### 깃 라벨 커스텀 [링크](https://github.com/ManageIQ/guides/blob/master/labels.md)
