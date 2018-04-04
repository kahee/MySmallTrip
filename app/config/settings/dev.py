from config import settings
from .base import *

secrets_base = json.loads(open(SECRETS_DEV, 'rt').read())

DATABASES = secrets_base['DATABASES']
DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.elasticbeanstalk.com',
    '.hongsj.kr',
    ]
WSGI_APPLICATION = 'config.wsgi.dev.application'

INSTALLED_APPS += [
    'django_extensions',
    'storages',
]

# S3대신 EC2에서 정적파일을 제공 (프리티어의 put사용량 절감을 위해 )
STATICFILES_STORAGE = 'config.storage.StaticFilesStorage'

DEFAULT_FILE_STORAGE = 'config.storage.DefaultFileStorage'


def is_ec2_linux():
    """Detect if we are running on an EC2 Linux Instance
       See http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/identify_ec2_instances.html
    """
    if os.path.isfile("/sys/hypervisor/uuid"):
        with open("/sys/hypervisor/uuid") as f:
            uuid = f.read()
            return uuid.startswith("ec2")
    return False


def get_linux_ec2_private_ip():
    """Get the private IP Address of the machine if running on an EC2 linux server"""
    from urllib.request import urlopen
    if not is_ec2_linux():
        return None
    try:
        response = urlopen('http://169.254.169.254/latest/meta-data/local-ipv4')
        ec2_ip = response.read().decode('utf-8')
        if response:
            response.close()
        return ec2_ip
    except Exception as e:
        print(e)
        return None


private_ip = get_linux_ec2_private_ip()
if private_ip:
    ALLOWED_HOSTS.append(private_ip)
