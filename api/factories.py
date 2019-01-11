import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group

from api.models import Powtoon


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', )
    first_name = "John"
    last_name = "Doe"
    username = "username"
    password = make_password('password')


class PowtoonFactory(factory.DjangoModelFactory):
    class Meta:
        model = Powtoon
        django_get_or_create = ('name', )
    user = factory.SubFactory(UserFactory)
    name = factory.Faker('name')
    content = "{}"

    @factory.post_generation
    def shared_with(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for user in extracted:
                self.shared_with.add(user)


class GroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = Group
        django_get_or_create = ('name', )
    name = 'admin'

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for group in extracted:
                self.groups.add(group)
