from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse('users:register'),
            data={
                "username": "muhammadqodir",
                "first_name": "Muhammadqodir",
                "last_name": "Jalilov",
                "email": "jalilov@gmail.com",
                "password": "somepassword"
            }
        )

        user = CustomUser.objects.get(username="muhammadqodir")
        self.assertEqual(user.username, "muhammadqodir")
        self.assertEqual(user.first_name, "Muhammadqodir")
        self.assertEqual(user.last_name, "Jalilov")
        self.assertEqual(user.email, "jalilov@gmail.com")
        self.assertNotEqual(user.password, "somepassword")
        self.assertTrue(user.check_password('somepassword'))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                "first_name": "Muhammadqodir",
                "last_name": "Jalilov",
                "email": "jalilov"
            }
        )

        user_count = CustomUser.objects.count()
        form = response.context['form']
        self.assertEqual(user_count, 0)
        self.assertFormError(form, "username", "This field is required.")
        self.assertFormError(form, "password", "This field is required.")
        self.assertFormError(form, "email", "Enter a valid email address.")

    def test_duplicate_username(self):
        CustomUser.objects.create_user(
            username='muhammadqodir',
            first_name='Muhammadqodir',
            last_name='Jalilov',
            email='jalilovm@gmail.com',
            password='somepass'
        )

        response = self.client.post(
            reverse('users:register'),
            data={
                "first_name": "Muhammadqodir",
                "last_name": "Jalilov",
                "email": "jalilov@gmail",
                "password": "somepassword",
                "username": "muhammadqodir"
            }
        )

        user_count = CustomUser.objects.count()
        form = response.context['form']
        self.assertEqual(user_count, 1)
        self.assertFormError(form, "username", "A user with that username already exists.")


class LogInTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create_user(username='muhammadqodir', first_name='Muhammadoqdir')
        self.db_user.set_password('somepassword')
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                "username": "muhammadqodir",
                "password": "somepassword"
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        response = self.client.post(
            reverse('users:login'),
            data={
                "username": "wrong-username",
                "password": "somepassword"
            }
        )

        form = response.context["login_form"]
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertIn("Please enter a correct username and password. Note that both fields may be case-sensitive.",
                      form.non_field_errors())

        self.client.post(
            reverse('users:login'),
            data={
                "username": "muhammadqodir",
                "password": "wrong-password"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:login'),
            data={}
        )
        form = response.context['login_form']
        self.assertFormError(form, "username", "This field is required.")
        self.assertFormError(form, "password", "This field is required.")

    def test_successful_logout(self):
        self.client.login(username="muhammadqodir", password="somepassword")
        self.client.get(reverse('users:logout'))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username='muhammadqodir', first_name='Muhammadqodir', last_name='Jalilov',
                                   email='muhammadq@gmail.com')
        self.db_user.set_password('somepassword')
        self.db_user.save()

    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login')+"?next=/users/profile/")

    def test_user_profile_info(self):
        self.client.login(username="muhammadqodir", password="somepassword")

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.db_user.username)
        self.assertContains(response, self.db_user.first_name)
        self.assertContains(response, self.db_user.last_name)

    def test_profile_edit(self):
        self.client.login(username="muhammadqodir", password="somepassword")
        response = self.client.post(
            reverse('users:profile-edit'),
            data={
                'username': 'muhammadqodir',
                'first_name': 'Muhammadqodir',
                'last_name': "Do'stov",
                'email': 'jalilovm54@gamil.com'
            }
        )
        self.db_user.refresh_from_db()

        self.assertEqual(response.url, reverse('users:profile'))
        self.assertEqual(self.db_user.last_name, "Do'stov")
        self.assertEqual(self.db_user.email, "jalilovm54@gamil.com")
