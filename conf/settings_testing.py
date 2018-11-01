# -*- coding: utf-8 -*-
"""
用于测试环境的全局配置
"""
from settings import APP_ID
# ===============================================================================
# 数据库设置, 本地开发数据库设置
# ===============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 我们默认用mysql
        'NAME': APP_ID,                        # 数据库名 (默认与APP_ID相同)
        'USER': 'check-list',                            # 你的数据库user
        'PASSWORD': 'tlCMvTHO73',                        # 你的数据库password
        'HOST': 'XXXX',                   		   # 数据库HOST
        'PORT': '3306',                        # 默认3306
    },
}
