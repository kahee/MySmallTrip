# My Small Trip
<img src='./app/static/intro.png'>

사진 찍고 오는 여행 No! 발자국만 찍고 돌고 오는 여행 No! 진정한 여행이란? <br>
나의 여행 후기를 들려 주었을때, 듣는 사람으로 하여금 마치 그곳을 여행 다녀온듯한 느낌을 줄수 있는가? <br>
여러분의 영원히 기억될 여행추억 with My Small Trip 입니다. <br>

## 프로젝트 소개
 4개월 동안 웹 프로그래밍 스쿨에서 배운 기술과 IOS 협업을 통해 `My Small Trip` 앱 개발

## 프로젝트 소개 영상
- 영상 : 
    - 1배속 : https://www.youtube.com/watch?v=xA2IJ0NWzoo&t=8s
    - 2배속 : https://www.youtube.com/watch?v=bwWaEQzDF90
    
## 프로젝트 구성
- 프로젝트 팀구성 : 백엔드2명, IOS 앱개발 3명
- 기간 : 2018.04.02 ~ 04.25
- 역할 : 서버세팅 및 배포, API작성
- 사용 언어 및 프로그램
  - 공통 : Git, Postman, Slack, Zeplin
  - 백엔드 : Python , Django, PostgreSQL, Django-Rest-Framework, AWS EC2, S3, RDS, Elastic Beanstalk, Docker, Sentry,
- 주요내용:
  - 백엔드 ( local / dev / production ) 개발 환경 분리
  - 나라별, 도시별, 여행상품 리스트 보여주기
  - 상품예약, 취소하기,예약현황에 따른 예약가능 캘린더 보여주기 기능
  - 로그인/로그아웃/페이스북 로그인/비밀번호변경(문자인증)
  - 이용한 상품별 후기작성/수정/삭제 기능
  - 위시리스트, 상품별 검색 기능
  - `.secrets`폴더내의 파일로 비밀 키를 관리합니다.
  - DB로 PostgreSQL을 사용하며, `local`환경에서는 `localhost`의 DB, `dev`환경과 `production`환경에서는 `AWS RDS`의 DB를 사용합니다.

## 프로젝트 API
[API GIT BOOK](https://kahee.gitbooks.io/my-small-trip/)

## Requirements
- Python (3.6)
- PostgreSQL

## AWS 환경
- Python (3.6)
- S3 Bucket, 해당 Bucket을 사용할 수 있는 IAM User의 AWS AccessKey, SecretAccessKey
- RDS Database(보안그룹 허용 필요), 해당 database를 사용할 수 있는 RDS의 User, Password

## Installation(Django runserver)

```
pip install -r .requirements/dev.txt
```

### 로컬 환경 (local)

```
expose DJANGO_SETTINGS_MODULE=config.settings.dev
pip install -r .requirements/dev.txt
python manage.py runserver

```

### AWS환경 (dev)

```
expose DJANGO_SETTINGS_MODULE=config.settings.dev
pip install -r .requirements/dev.txt
python manage.py runserver

```

### 배포환경 (production)

```
expose DJANGO_SETTINGS_MODULE=config.settings.dev
pip install -r .requirements/dev.txt
python manage.py runserver

```

## Installation (Docker)

### 로컬환경 (local)
`localhost:8000`에서 확인

```
docker build -t eb-docker:base -f Dockerfile.local
docker run --rm -it 8000:80 eb-docker:local
```

### AWS환경 (dev)

```
docker build -t eb-docker:dev -f Dockerfile.dev
docker run --rm -it 8000:80 eb-docker:dev
```

### AWS환경 (production)

```
docker build -t eb-docker:production -f Dockerfile.production
docker run --rm -it 8000:80 eb-docker:production
```

## Dockerhub 관련

```
docker build -t eb-docker:base -f Dockerfile.base
docker tag eb-docker:base <자신의 사용자명>/<저장소명>:base
docker push <사용자명>/<저장소명>:base
```
이후 Elasticbeanstalk을 사용한 배포 시, 해당 이미지를 사용

```docker file
FROM    <사용자명>/<저장소명>:base
```

## Secrets

**`.secrets/base.json`**

```json
{
  "SECRET_KEY": "<Django settings SECRET_KEY value>",
  "RAVEN_CONFIG": {
    "dsn": "https://<sentry_Client_Keys>",
    "release": "raven.fetch_git_sha(os.path.abspath(os.pardir))"
  },
  "SUPERUSER_USERNAME":"<superuser username>",
  "SUPERUSER_PASSWORD":"<superuser user-password>",
  "SUPERUSER_EMAIL":"<superuser user-email>",

  "AWS_ACCESS_KEY_ID":"<AWS_ACCESS_KEY value> ",
  "AWS_SECRET_ACCESS_KEY":"<AWS_SECRET_ACCESS_KEY value>",
  "AWS_STORAGE_BUCKET_NAME":"<AWS_BUCKET_NAME>",
  "AWS_S3_REGION_NAME":"<region name>, default='ap-northeast-2'",
  "AWS_S3_SIGNATURE_VERSION":"<version>, default: s3v4",
  "AWS_DEFAULT_ACL":"private",
  "API_KEY": "COOLSMS API KEY",
  "API_SECRET": "COOLSMS API SECRET"
}

```

**`.secrets/local.json`**


**`.secrets/dev.json`**

```json
{
  "DATABASES": {
    "default": {
      "ENGINE": "django.db.backends.postgresql",
      "HOST": "<자신의 RDS주소. ex)instance-name.###.region.rds.amazonaws.com>",
      "NAME": "<DB name>",
      "USER": "<DB username>",
      "PASSWORD": "<DB user password>",
      "PORT": "<Port number, default:5432>"
    }
  }
}
```

**`.secrets/prodjction.json`**
- dev와 동일
