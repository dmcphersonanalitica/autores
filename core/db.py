import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MYSQL = {
    'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'dmcpherson_editorial_mecs',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': 3306
        }
}

MYSQLONLINE = {
    'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'edit_dmcpherson_editorial_mecs',
            'USER': 'edit_dmcpherson_editorial_mecs',
            'PASSWORD': '6S5Yke8b',
            'HOST': 'server.mcphersoncloud.com',
            'PORT': 3306
        }
}