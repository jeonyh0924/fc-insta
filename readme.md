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

- Nested Router [라이브러리 문서](https://github.com/alanjds/drf-nested-routers), [참고 링크](https://lunacircle4.github.io/django/2019/09/05/Django-router/)

### 깃 전략 세우기 [링크](https://blog.naver.com/PostView.nhn?blogId=tmondev&logNo=220763012361&redirect=Dlog)

### 깃 라벨 커스텀 [링크](https://github.com/ManageIQ/guides/blob/master/labels.md)

### 깃 마일드스톤 [링크](https://cyberx.tistory.com/112)

### 깃 브랜치 네이밍 [링크](https://gist.github.com/digitaljhelms/4287848)

### F Expressions [링크](https://brownbears.tistory.com/367) [공식문서](https://docs.djangoproject.com/en/3.0/ref/models/expressions/#f-expressions)

####  피드백
> 전체적인 틀을 세우는게 제일 중요하다. 기능을 명세하고, API 문서를 만들어야 한다. 
> 전체적으로 프로젝트를 시작 할 때 코딩을 먼저 시작하면 안된다. 시야가 좁아지고 하나의 기능에 집착하며 프로젝트 중에 기존에 했던 코드를 자꾸 되돌아 가게 된다.
> 
>  크롤링 빠르게 --> 테라폼


### Agile 방법 개발론
- 소프트웨어 사용자가 일반 대중으로 변화되면서 (Bto B >> Bto C)
- 소프트웨어 개발의 불확실성이 높아지며 경량 방법론 주의자가 늘어남( 프로젝트가 시작 시 상용화를 빠르게 한 뒤 꾸준히 업데이트)
- 문서화를 시키는 것 보다 프로토 타입의 배포를 더 우선시
- 협력과 피드백 (핵심가치)

#### media
[링크](https://ssungkang.tistory.com/entry/Django-media-%ED%8C%8C%EC%9D%BC-%EC%97%85%EB%A1%9C%EB%93%9C%ED%95%98%EA%B8%B0)



### MTPP [튜토리얼](https://django-mptt.readthedocs.io/en/latest/tutorial.html)
> pip intall django-mtpp
> installed apps 추가 ( 'mtpp')



### 내가 팔로우를 한 유저가 생성한 블로그 게시글
```python
qs = User.objects.filter(to_users_relation__from_user=u1).values_list('id').distinct()

Post.objects.filter(user_id__in=qs)

출처 : https://stackoverflow.com/questions/27519326/making-a-complicated-query-in-django-all-my-follows-posts
```


### django - soft delete
데이터 삭제 시 크게 Soft Delete, Hard Delete로 나뉜다.

Hard Delete - 데이터를 테이블에서 완전 삭제한다.
Soft Delete - 논리적으로 삭제한다.
[출처](https://wave1994.tistory.com/111)



### 쿼리 최적화
[링크](https://blog.myungseokang.dev/posts/database-access-optimization/)

[링크2](https://docs.google.com/presentation/d/1hB8IaW1jGxBiCZRalMeAxsddZF_1Aovas0IbcHco-NQ/edit#slide=id.g8ced37de75_0_10)

[링크3](https://blog.doosikbae.com/123)

[링크4](https://www.whatap.io/ko/blog/6/)

[select, prefetch](https://medium.com/chrisjune-13837/%EB%8B%B9%EC%8B%A0%EC%9D%B4-%EB%AA%B0%EB%9E%90%EB%8D%98-django-prefetch-5d7dd0bd7e15)

[select, prefetch #2](https://velog.io/@rosewwross/Django-selectrelated-%EC%99%80-prefetchedrelated%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%9C-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%B0%B8%EC%A1%B0)

#### Optimizing - 내용 정리 
대부분의 최적화 내용은 Disk IO, network IO 최적화를 할 것 이다. DB 최적화만 하여도 기능적인 최적화가 마무리 될 것이다. 
DB에 접근하면 Dist와 네트워크에 접근을 한다. 
데이터베이스는 퍼모먼스 이슈의 90%는 데이터베이스에서 발생 한다. 

속도
-----------------
CPU>RAM >>>>>SSD >>>>>>>>>>>>>>>>HDD >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Nework

#### DJango Debug Toolbar
[적용](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html)
[Lazy Loading](https://docs.djangoproject.com/en/3.0/topics/db/queries/#querysets-are-lazy)

Eager Loading - selcet_related, prefetch_related

#### Caching
[drf cache](https://www.django-rest-framework.org/api-guide/caching/)

[Django Cache get, set](https://docs.djangoproject.com/en/3.0/topics/cache/)

[Django Redis](https://github.com/jazzband/django-redis)

[When QuerySets are evaluated](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#when-querysets-are-evaluated)

[Django Performance Optimizing](https://docs.djangoproject.com/en/3.0/topics/db/optimization/)

##### Django Explain()

- 쿼리 분석결과 확인
- 인덱스 사용 여부 확인
- 대상 row 갯수 확인
- qs.explain()

### CacheOps
[라이브러리](https://github.com/Suor/django-cacheops)
[참고자료1](https://americanopeople.tistory.com/318)
[참고자료2](https://medium.com/29cm/cacheops-orm%EC%97%90-redis-cache-%EC%89%BD%EA%B2%8C-%EC%A0%81%EC%9A%A9%ED%95%98%EA%B8%B0-966249a1c615)
#### CacheOps - 내용정리
Django에 Redis Cache를 쉽게 적용하고, 관리할 수 있도록 도와주는 라이브러리이다.

Cacheops의 가장 큰 장점은 ORM에 캐시를 간편하게 적용할 수 있단 점이다. 

모델에서 캐시를 바라보게 하고 싶다면, settings에 설정을 추가한다.

get, set과 달리 자신의 모델 필드 값이 변경이 될 경우에 해당 필드로 질의하여, 캐싱 하였던 데이터를 삭제합니다.  단, select_related로 모델을 조인 한 경우에는 캐시 삭제 대상에 해당하지 않으므로 prefetch_related로 변경을 해 주어야 한다. 


[출처](https://americanopeople.tistory.com/318)

##### cache ops 내용 정리 필요
- 잘 걸리는지 확인을 해야 한다. ops의 장점은 손 쉽게 캐시를 해준다는 것이 있는데, 확인을 제대로 하지 않고 서비스를 배포 하게 되고 캐시가 동작하지 않는다면 퍼포먼스적으로

 손해가 크다.

- 캐시를 언제 하느냐: 특정 모델이 헤비한경우
- 캐시를 하는 이유 : 빠르게 응답을 하기 위해, 디비에 연산을 줄이기 위해
- 사용자에게 빠른 응답을 해야 하는 의무가 있다. 사용자가 많아지면 많아질 수록 서비스는 느려진다. --> 캐시를 해야 이 문제점을 해결할 수 있다.
- 스태틱 서버는 전 세계에 엣지 서버가 있다. 
- 다이나믹 컨텐츠와 스태틱 컨텐츠는 캐싱에 차이가 있다 .
- 전 세계에서는 북미에 위치한 API서버에 콜을 보낸다. 
- 북미에는 api서버, 디비, 캐시 서버가 있다. 
- 스태틱 컨텐츠는 인벨리데이션을 하지 않는다. 
- cacheops는 장고에서 시그널을 받아서 하는데 bulk_create, bulk_update, bulk_delete는 시그널을 보내지 않아서 qs.invalidate_update등 직접 호출을 해야 한다. ***Mass Updates*** invalidation trigger가 호출이 되지 않는다. 
- 시그널에 대해서 공부. 


##### 망 중립성 [ 재미로 찾아 보기 ]
- 네트워크의 60% 가 넷플릭스가 가지고 있다. 
- kt와 페이스북 소송 (망 중립성)


##### in memorystorage
- cpu, ram의 속도를 이야기 하였었는데 지금까지는 데이터베이스 최적화를 하였는데 가장 느린 최적화를 정리하기 위해 디비 최적화를 한다.(네트워크 콜)
- 그 다음은 디스크 io를 줄이기 위한 최적화를 해야 한다. 
- 속도가 빨라지고
- 물리적인 파일을 생성하지 않는다.

- storage 정책
- test ->> inmemory(ram)
- local // inmemory로 하는것.(ram) or s3(버킷은 변경을 해야 한다.)
- staging (aws) //aws
- production (aws) // aws


### Extra optimizing

#### Centralization log
- 기존에 로그를 보는 방법은 콘솔을 통하여 보는 방식이다. (standard out, standard error)
- 배포 환경에서 서버를 띄웠을 때에는 
- 서버를 중앙화 하여야 한다. (서버에 들어가지 않고도 서버를 볼 수 있어야 한다. 로그를 남기는 것은 매우 중요하기 때문에)
- 배포한 서버에 접속이 불가한 경우도 있다.
- 크게 2가지 방식이 있다.(file log, stream transfer)
- file log : 로그 내용을 파일에 직접 작성 (파일 용량이 커지는 단점, rotatoin : 용량, 최대 저장 기간, 최대 저장 용량 등으로 걸기도 한다. 디도스 공격에 대비하기 위하여)
- stream log : 
	- file watch 
	- HTTP 전송 

	
#### LogDNA
- 과제


##### Async Worker
- 비 동기 task Queue
- networkio가 발생되지 않는 선에서 

### [celery](https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html)

#### Django lock
- [블로그 글1](https://medium.com/@chrisjune_13837/django-row-lock-%EB%8F%99%EC%9E%91%EB%B0%A9%EC%8B%9D-a2e05bb0eb90)
- [블로그 글2](https://fabl1106.github.io/django/2019/08/23/Django-33.-Django-Lock%EC%97%90-%EA%B4%80%ED%95%B4%EC%84%9C.html)

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
    },
}

# models.py
from datetime import datetime
from time import sleep

from django.core.cache import cache
from django.db import models


class Account(models.Model):
    balance = models.PositiveIntegerField(default=0)

    def log(self, *args):
        print(datetime.now(), *args)

    def update_balance(self, val):
        # 해당 함수 시작
        self.log('Update Balance:', val)
        # 캐시 키 값 초기화
        key = f'lock:account:{self.id}'
        # ttl 해당 캐시를 얼마나 지속할 지에 대하여
        ttl = 60

        for i in range(5):
            self.log('실행 ')
            lock = cache.get(key)
            if not lock:
                # 캐시가 없다면 반복문을 끝낸다.
                self.log('락이 없다.')
                break
            # 캐시가 있다면 대기
            self.log('Lock Exists and wait')
            # lock 이 존재하므로 대기
            sleep(2)

        else:
            # 브레이크가 걸리지 않았을 경우 표시.
            self.log('lock acquire failed')
            return False

        # value 값이 중요하지는 않고, 키가 존재하는 것이 중요!

        # 반복문이 끝났다면 ( 반복문이 끝난 경우는 캐시가 없는 경우 )
        cache.set(key, True, ttl)
        self.log('Lock Acquired')

        self.log('start logic')
        # 지금부터 해당 시간동안 락이 걸려 접근하는 동작에 대해서 접근을 막는다.

        # 어떤 로직이 돌아가는 시간.
        sleep(9)

        self.log('Finish logic:', val)
        cache.delete(key)
        self.log('Lock Released')



```

#### django smtp
- [블로그 글1](https://bum752.github.io/posts/django-mail/)


#### [Django Signal 공식문서](https://docs.djangoproject.com/en/3.0/topics/signals/)
-  **bulk를 사용하는 경우에는 시그널이 오지 않는다.**

- [블로그 글1](https://kimdoky.github.io/django/2018/09/06/django-taskbuster-9/)

- [블로그글 2](https://chohyeonkeun.github.io/2019/05/11/190511-django-Signal/)

- [블로그글 3](https://jisunglab.tistory.com/178)

- [블로그글 4](https://dgkim5360.tistory.com/entry/django-signal-example)
- [Django lifeCycle 라이브러리](https://github.com/rsinger86/django-lifecycle)

- 장고 시그널은 특정 이벤트가 발생할 때 응용 프로그램에 알릴 수 있는 전략입니다. 
- 시그널 시스템에는 senders와 receivers 두 가지 핵심 요소가 있습니다. sender는 신호를 전달하는 책임자, receiver는 신호를 수신 한 다음 무언가를 수행하는 객체 입니다. 
- Receivers 는 신호를 수신하는 함수 또는 인스턴스 메서드이어야 한다.
- Senders는 sender로 부터 이벤트를 받기 위해서는 python 개체이거나 None 이어야 한다. 
- sender : 사용자 모델 클래스
- created : 새로운 User가 생성되었는지 나타내는 bool
- instance : 저장 중인 사용자 인스턴스
	- pre_save : 저장 전, 실행
	- post_save : 저장 후, 실행
	- pre_delete : 삭제 전, 실행
	- post_save : 삭제 후, 실행



#### Locust
- Python으로 테스트 코드를 작성한다.
- 빠르게 테스트 환경을 구축하고 실행해볼 수 있다.

- [블로그 글1](https://medium.com/@jspark141515/locust%EB%A1%9C-%EC%84%9C%EB%B2%84-%EC%84%B1%EB%8A%A5-%ED%85%8C%EC%8A%A4%ED%8A%B8%ED%95%98%EA%B8%B0-7490d882015)




#### ElasticSearch

- Full Text 검색 지원 
	- 엄청나게 빠르다 이유는 reverse index를 쓰기 때문에
	- 자연어 검색이 가능하다. 
	- **데이터베이스는 B+ tree의 자료구조를 가지고 있다.** 
		- 정렬이 되어 있는 구조이다.

	- objects.filter에서 contain를 사용을 한다는 것은 엄청나게 느리다 n*n 서비스가 엄청 작을경우에만 사용해야 한다.


- ELK 
	- ES (DB 같은) : 1.로그 저장용 , 2.검색 사용에  많이 사용된다. 
	- Logstash
	- kibana ( ES를 보는 툴 djagno admin같은 )

	

#### [Django 검색](https://medium.com/@whj2013123218/%EC%9E%A5%EA%B3%A0-django-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%EC%97%90-%EA%B2%80%EC%83%89%EA%B8%B0%EB%8A%A5-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0-%EA%B8%B0%EB%B3%B8-%EA%B2%80%EC%83%89-%EC%9B%90%EB%A6%AC%EC%97%90-%EA%B4%80%ED%95%98%EC%97%AC-632516e6a14f)


##### [django elasticsearch dsl](https://django-elasticsearch-dsl.readthedocs.io/en/latest/quickstart.html)
```python
# settings.py
ELASTICSEARCH_DSL={
    'default': {
        'hosts': 'localhost:9200'
    },
}

# models.py
class Car(models.Model):
    name = models.CharField()
    color = models.CharField()
    description = models.TextField()
    type = models.IntegerField(choices=[
        (1, "Sedan"),
        (2, "Truck"),
        (4, "SUV"),
    ])
    
# documents.py
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Car


@registry.register_document
class CarDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'cars'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Car # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'name',
            'color',
            'description',
            'type',
        ]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True

        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        # queryset_pagination = 5000

```

```shell
# 선웅이 형님 도움 -- 해당 링크 https://soyoung-new-challenge.tistory.com/110
$ docker pull docker.elastic.co/elasticsearch/elasticsearch:7.7.1
$ docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.7.1

```

```python
$ ./manage.py search_index --rebuild

car = Car(
    name="Car one",
    color="red",
    type=1,
    description="A beautiful car"
)
car.save()

s = CarDocument.search().filter("term", color="red")

# or

s = CarDocument.search().query("match", description="beautiful")

for hit in s:
    print(
        "Car name : {}, description {}".format(hit.name, hit.description)
    )
    
# 또는 localhost:9200/cars
# 해당 인덱스 이름 
```

