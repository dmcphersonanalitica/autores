from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict
from core.settings import STATIC_URL
import requests


class User(AbstractUser):

    def generate_request(self, url, params={}):
        try:
            response = requests.get(url, verify=False)

            if response.status_code == 200:
                return response.json()
        except Exception as ex:
            pass

    def get_author_image(self, params={}):
        countBlankSpaceNames = self.autores.nombre.count(' ')
        lowerNames = self.autores.nombre.lower().replace(' ', '-', countBlankSpaceNames)
        countBlankSpaceLastNames = self.autores.apellidos.count(' ')
        lowerLastNames = self.autores.apellidos.lower().replace(' ', '-', countBlankSpaceLastNames)
        lowerFullNames = lowerNames + '-' + lowerLastNames
        email = self.autores.correo

        response = self.generate_request('https://dmcphersoneditorial.com:3001/api/autor/by-full-name/' +
                                         lowerFullNames, params)
        if response:
            imageUrl = response.get('picture_address')
            return imageUrl

        response = self.generate_request('https://dmcphersoneditorial.com:3001/api/autor/by-email/' + email, params)
        if response:
            imageUrl = response.get('picture_address')
            return imageUrl

        return '{}{}'.format(STATIC_URL, 'image/Author.jpg')

    def toJson(self):
        item = model_to_dict(self, fields=['id', 'username', 'email'])
        # if self.last_login:
        #     item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        # else:
        #     item['last_login'] = ''
        #item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'Login_user'
        ordering = ["id"]
        indexes = [models.Index(fields=['id', 'username', 'email'])]
