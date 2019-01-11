import json

from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from api import factories
from api.factories import UserFactory, PowtoonFactory
from api.models import Powtoon

client = Client()


class PowtoonListTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username='user')
        self.user.set_password('123')
        self.user.save()

    def test_retrieving_powtoon_for_owner(self):
        powtoon = factories.PowtoonFactory(user=self.user)

        client.login(username=self.user.username, password='123')
        response = client.get(reverse('powtoon-list'))

        self.assertEquals(response.json()[0]['id'], powtoon.id)
        self.assertEquals(response.json()[0]['name'], powtoon.name)
        self.assertEquals(response.json()[0]['content'], powtoon.content)

    def test_retrieving_powtoon_for_shared_with_user(self):
        another_user = UserFactory(username='another_user')
        powtoon = factories.PowtoonFactory(user=another_user, shared_with=[self.user, ])

        client.login(username=self.user.username, password='123')
        response = client.get(reverse('powtoon-list'))

        self.assertEquals(response.json()[0]['id'], powtoon.id)
        self.assertEquals(response.json()[0]['name'], powtoon.name)
        self.assertEquals(response.json()[0]['content'], powtoon.content)

    def test_retrieving_multiple_powtoons_for_shared_with_user(self):
        another_user = UserFactory(username='another_user')
        for i in range(0, 5):
            factories.PowtoonFactory(user=another_user, shared_with=[self.user, ])
        client.login(username=self.user.username, password='123')
        response = client.get(reverse('powtoon-list'))

        self.assertEquals(len(response.json()), 5)

    def test_retrieving_powtoon_for_not_allowed_user(self):
        another_user = UserFactory(username='another_user')
        factories.PowtoonFactory(user=another_user)

        client.login(username=self.user.username, password='123')
        response = client.get(reverse('powtoon-list'))

        self.assertEquals(len(response.json()), 0)

    def test_retrieving_powtoon_for_user_with_extra_permissions(self):
        another_user = UserFactory(username='another_user')
        permission = Permission.objects.get(name='Can see any Powtoons')
        self.user.user_permissions.add(permission)
        another_powtoon = factories.PowtoonFactory(user=another_user)

        client.login(username=self.user.username, password='123')
        response = client.get(reverse('powtoon-list'))

        self.assertEquals(response.json()[0]['id'], another_powtoon.id)
        self.assertEquals(response.json()[0]['name'], another_powtoon.name)
        self.assertEquals(response.json()[0]['content'], another_powtoon.content)


class PowtoonGetTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username='user')
        self.user.set_password('123')
        self.user.save()

    def test_retrieving_powtoon_for_owner_user(self):
        powtoon = factories.PowtoonFactory(user=self.user)

        client.login(username=self.user.username, password='123')
        response = client.get(
            reverse('powtoon-detail', args=(powtoon.pk, ))
        )

        self.assertEquals(response.json()['id'], powtoon.id)
        self.assertEquals(response.json()['name'], powtoon.name)
        self.assertEquals(response.json()['content'], powtoon.content)

    def test_retrieving_powtoon_for_shared_wihth_user(self):
        powtoon = factories.PowtoonFactory(shared_with=[self.user, ])

        client.login(username=self.user.username, password='123')
        response = client.get(
            reverse('powtoon-detail', args=(powtoon.pk, ))
        )

        self.assertEquals(response.json()['id'], powtoon.id)
        self.assertEquals(response.json()['name'], powtoon.name)
        self.assertEquals(response.json()['content'], powtoon.content)

    def test_retrieving_powtoon_for_not_allowed_user_returns_404(self):
        another_user = UserFactory(username='another_user')
        powtoon = factories.PowtoonFactory(user=another_user)

        client.login(username=self.user.username, password='123')
        response = client.get(
            reverse('powtoon-detail', args=(powtoon.pk,))
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


class PowtoonCreateTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username='user')
        self.user.set_password('123')
        self.user.save()

    def test_creating_powtoon_for_any_user_and_it_is_ok(self):
        powtoon_data = {
            'name': 'powtoon test',
            'content': '{}',
        }
        client.login(username=self.user.username, password='123')

        response = client.post(reverse('powtoon-list'), data=powtoon_data)

        users_powtoon = Powtoon.objects.filter(user=self.user)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(users_powtoon.exists())

        self.assertEquals(users_powtoon.get().name, powtoon_data['name'])


class PowtoonUpdateTetCase(TestCase):

    def setUp(self):
        self.user = UserFactory(username='user')
        self.user.set_password('123')
        self.user.save()

    def test_updating_powtoon_for_owner_and_it_is_ok(self):
        powtoon = PowtoonFactory(user=self.user)

        powtoon_updated_data = {
            'name': 'new name',
            'content': json.dumps({'key': 'value'})
        }

        client.login(username=self.user.username, password='123')
        response = client.put(
            reverse('powtoon-detail', args=(powtoon.pk, )),
            content_type='application/json',
            data=powtoon_updated_data
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            Powtoon.objects.filter(user=self.user).get().name,
            powtoon_updated_data['name']
        )

    def test_updating_powtoon_for_not_owner_returns_403(self):
        another_user = UserFactory(username='another_user')
        powtoon = factories.PowtoonFactory(user=another_user, shared_with=[self.user, ])

        powtoon_updated_data = {
            'name': 'new name',
            'content': json.dumps({'key': 'value'})
        }

        client.login(username=self.user.username, password='123')
        response = client.put(
            reverse('powtoon-detail', args=(powtoon.pk,)),
            content_type='application/json',
            data=powtoon_updated_data
        )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class PowtoonDestroyTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username='user')
        self.user.set_password('123')
        self.user.save()

    def test_delete_powtoon_for_owner(self):
        powtoon = PowtoonFactory(user=self.user)
        self.assertEquals(Powtoon.objects.count(), 1)

        client.login(username=self.user.username, password='123')
        response = client.delete(
            reverse('powtoon-detail', args=(powtoon.pk,)),
        )
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Powtoon.objects.count(), 0)

    def test_delete_for_non_owner_return_404(self):
        another_user = UserFactory(username='another_user')
        powtoon = PowtoonFactory(user=another_user)

        client.login(username=self.user.username, password='123')
        response = client.delete(
            reverse('powtoon-detail', args=(powtoon.pk,)),
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


class PowtoonSharedTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username='user')
        self.user.set_password('123')
        self.user.save()

    def test_getting_shared_with_powtoons(self):
        another_user = UserFactory(username='another_user')
        for i in range(0, 5):
            PowtoonFactory(user=another_user, shared_with=[self.user, ])
            PowtoonFactory(user=another_user)
        client.login(username=self.user.username, password='123')
        response = client.get(reverse('powtoon-shared-list'))
        response_data = response.json()
        self.assertListEqual(
            list(
                Powtoon.objects.filter(shared_with__in=[self.user]).values_list('id', flat=True)
            ),
            [powtoon['id'] for powtoon in response_data]
        )

    def test_share_powtoon_for_owner(self):
        powtoon = PowtoonFactory(user=self.user)
        another_user = UserFactory(username='another_user')

        client.login(username=self.user.username, password='123')

        shared_data = {'shared_with': [another_user.id, ]}
        response = client.put(
            reverse('powtoon-shared-detail', args=(powtoon.pk, )),
            content_type='application/json',
            data=json.dumps(shared_data),
        )
        self.assertEquals(response.json()['shared_with'], [another_user.id, ])

    def test_share_powtoon_for_user_with_extra_permissions(self):
        first_user = UserFactory(username='firs')
        second_user = UserFactory(username='second')
        third_user = UserFactory(username='third')

        powtoon = PowtoonFactory(user=first_user)

        permission = Permission.objects.get(name='Can share any Powtoons')
        self.user.user_permissions.add(permission)
        client.login(username=self.user.username, password='123')

        shared_with = [second_user.id, third_user.id]
        shared_data = {'shared_with': shared_with}

        response = client.put(
            reverse('powtoon-shared-detail', args=(powtoon.pk,)),
            content_type='application/json',
            data=json.dumps(shared_data),
        )

        self.assertEquals(response.json()['shared_with'], shared_with)

    def test_share_for_not_owned_powtoon_return_404(self):
        another_user = UserFactory(username='another_user')
        powtoon = PowtoonFactory(user=another_user)

        client.login(username=self.user.username, password='123')
        shared_data = {'shared_with': [self.user.id, ]}

        response = client.put(
            reverse('powtoon-shared-detail', args=(powtoon.pk,)),
            content_type='application/json',
            data=json.dumps(shared_data),
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
