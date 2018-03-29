# EB Docker deploy

Eb Docker  배포를 연습하는 프로젝트입니다.
`.secrets`폴더내의 파일로 비밀 키를 관리합니다.

DB로 PostgreSQL을 사용하며, `local`환경에서는 `localhost`의 DB, `dev`환경과 `production`환경에서는 `AWS RDS`의 DB를 사용합니다.

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
  "SECRET_KEY": "<Django settings SECRET_KEY value>"
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
  "AWS_DEFAULT_ACL":"private"
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
      "PORT": <Port number, default:5432>
    }
  }
}
```
**`.secrets/prodjction.json`**
#dev와 동일