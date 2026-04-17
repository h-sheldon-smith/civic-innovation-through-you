from django import forms
from service_objects.services import Service

from users.services import GetOrCreateModUser

class CreateAutoModUser(Service):
    def process(self):
        username = 'AutoMod'
        email = 'civicinnovationthroughyou@gmail.com'
        password = 'letmein!' # TODO: make a secure version of password storage

        user, created, promoted = GetOrCreateModUser.execute({
            'username': username,
            'email': email,
            'password': password,
        })

        if not created:
            status = None
        else:
            status = user

        return status