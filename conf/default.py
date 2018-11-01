# -*- coding: utf-8 -*-
"""
Django settings for app-framework project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/

"""

import os
import sys
# Import global settings to make it easier to extend settings.
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except:
    pass

# TOCHANGE 在蓝鲸智云平台上注册的应用的编码以及生成的应用对应的Token
APP_ID = os.environ.get('APP_ID', "test-0001")
APP_TOKEN = os.environ.get('APP_TOKEN') or "feb90e29-00aa-4df5-a5d6-667f01b9d6c1"
BK_PAAS_HOST = os.environ.get('BK_PAAS_HOST')\
    if os.environ.get('BK_PAAS_HOST') else "http://paas.bkopen.com:80"
# 数据库初始化 超级用户列表
ADMIN_USERNAME_LIST = ['admin']

# ==============================================================================
# 应用运行环境配置信息
# ==============================================================================
ENVIRONMENT = os.environ.get("BK_ENV", "development")
# 运行模式， DEVELOP(开发模式)， TEST(测试模式)， PRODUCT(正式模式)
RUN_MODE = 'DEVELOP'    # DEVELOP TEST PRODUCT
if ENVIRONMENT.endswith('production'):
    RUN_MODE = 'PRODUCT'
    DEBUG = False
elif ENVIRONMENT.endswith('testing'):
    RUN_MODE = 'TEST'
    DEBUG = False
else:
    RUN_MODE = 'DEVELOP'
    DEBUG = True
TEMPLATE_DEBUG = DEBUG

# ===============================================================================
# 应用基本信息
# ===============================================================================
# 应用密钥
SECRET_KEY = 'MQtd_0cw&AiY5jT&&#w7%9sCK=HW$O_e%ch4xDd*AaP(xU0s3X'
# 应用访问路径
SITE_URL = '/'
RUN_MODE = 'DEVELOP'
if ENVIRONMENT.endswith('production'):
    RUN_MODE = 'PRODUCT'
    DEBUG = False
    SITE_URL = '/o/%s/' % APP_ID
elif ENVIRONMENT.endswith('testing'):
    RUN_MODE = 'TEST'
    DEBUG = False
    SITE_URL = '/t/%s/' % APP_ID
else:
    RUN_MODE = 'DEVELOP'
    DEBUG = True
# CSRF的COOKIE域，默认使用当前域
# CSRF_COOKIE_DOMAIN =''
CSRF_COOKIE_PATH = SITE_URL
ALLOWED_HOSTS = ['*']
# ==============================================================================
# Middleware and apps
# ==============================================================================
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'account.middlewares.LoginMiddleware',   # 登录鉴权中间件
    'common.middlewares.CheckXssMiddleware',  # Xss攻击处理中间件
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # OTHER 3rd Party App
    'app_control',
    'account',
    'task_center',
    # 'manager',
    # 'channels',
)

# ==============================================================================
# Django 项目配置
# ==============================================================================
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-CN'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

# 项目路径
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT, PROJECT_MODULE_NAME = os.path.split(PROJECT_PATH)
BASE_DIR = os.path.dirname(os.path.dirname(PROJECT_PATH))
PYTHON_BIN = os.path.dirname(sys.executable)

# ===============================================================================
# 静态资源设置
# ===============================================================================
# 静态资源文件(js,css等）在应用上线更新后, 由于浏览器有缓存, 可能会造成没更新的情况.
# 所以在引用静态资源的地方，都需要加上这个版本号，如：<script src="/a.js?v=${STATIC_VERSION}"></script>；
# 如果静态资源修改了以后，上线前修改这个版本号即可
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
STATIC_VERSION = 0.1
# 应用本地静态资源目录
STATIC_URL = '%sstatic/' % SITE_URL

ROOT_URLCONF = 'urls'
# ==============================================================================
# Templates
# ==============================================================================
# mako template dir
MAKO_TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'templates')
MAKO_TEMPLATE_MODULE_DIR = os.path.join(BASE_DIR, 'templates_module', APP_ID)
if RUN_MODE not in ['DEVELOP']:
    MAKO_TEMPLATE_MODULE_DIR = os.path.join(PROJECT_ROOT, 'templates_module', APP_ID)
# Django TEMPLATES配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # the context to the templates
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.csrf',
                'common.context_processors.mysetting',   # 自定义模版context，可在页面中使用STATIC_URL等变量
                'django.template.context_processors.i18n',
            ],
        },
    },
]
# ==============================================================================
# session and cache
# ==============================================================================
SESSION_EXPIRE_AT_BROWSER_CLOSE = True       # 默认为false,为true时SESSION_COOKIE_AGE无效
SESSION_COOKIE_PATH = SITE_URL               # NOTE 不要改动，否则，可能会改成和其他app的一样，这样会影响登录

# ===============================================================================
# Authentication
# ===============================================================================
AUTH_USER_MODEL = 'account.BkUser'
AUTHENTICATION_BACKENDS = ('account.backends.BkBackend', 'django.contrib.auth.backends.ModelBackend')
LOGIN_URL = "%s/login/?app_id=%s" % (BK_PAAS_HOST, APP_ID)
LOGOUT_URL = '%saccount/logout/' % SITE_URL
LOGIN_REDIRECT_URL = SITE_URL
REDIRECT_FIELD_NAME = "c_url"
# 验证登录的cookie名
BK_COOKIE_NAME = 'bk_token'

# ==============================================================================
# logging
# ==============================================================================
# 应用日志配置
BK_LOG_DIR = os.environ.get('BK_LOG_DIR', '/data/paas/apps/logs/')
LOGGING_DIR = os.path.join(BASE_DIR, 'logs', APP_ID)
LOG_CLASS = 'logging.handlers.RotatingFileHandler'
if RUN_MODE == 'DEVELOP':
    LOG_LEVEL = 'DEBUG'
elif RUN_MODE == 'TEST':
    LOGGING_DIR = os.path.join(BK_LOG_DIR, APP_ID)
    LOG_LEVEL = 'INFO'
elif RUN_MODE == 'PRODUCT':
    LOGGING_DIR = os.path.join(BK_LOG_DIR, APP_ID)
    LOG_LEVEL = 'ERROR'

# 自动建立日志目录
if not os.path.exists(LOGGING_DIR):
    try:
        os.makedirs(LOGGING_DIR)
    except:
        pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s [%(asctime)s] %(pathname)s %(lineno)d %(funcName)s %(process)d %(thread)d \n \t %(message)s \n',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s \n'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'root': {
            'class': LOG_CLASS,
            'formatter': 'verbose',
            'filename': os.path.join(LOGGING_DIR, '%s.log' % APP_ID),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5
        },
        'component': {
            'class': LOG_CLASS,
            'formatter': 'verbose',
            'filename': os.path.join(LOGGING_DIR, 'component.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5
        },
        'wb_mysql': {
            'class': LOG_CLASS,
            'formatter': 'verbose',
            'filename': os.path.join(LOGGING_DIR, 'wb_mysql.log'),
            'maxBytes': 1024 * 1024 * 4,
            'backupCount': 5
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        # the root logger ,用于整个project的logger
        'root': {
            'handlers': ['root'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        # 组件调用日志
        'component': {
            'handlers': ['component'],
            'level': 'WARN',
            'propagate': True,
        },
        # other loggers...
        'django.db.backends': {
            'handlers': ['wb_mysql'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
