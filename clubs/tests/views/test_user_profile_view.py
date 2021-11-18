from django.test import TestCase
from django.urls import reverse
from clubs.models import User

class UserProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            '@johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
            password='Password123',
            bio='The quick brown fox jumps over the lazy dog.',
            chess_experience_level=1,
            personal_statement='nu mi place sa joc sah',
        )
        self.url = reverse("show_user", kwargs={"user_id": 1})
        self.url2 = reverse("show_user", kwargs={"user_id": 3})

    def test_show_user_url(self):
        self.assertEqual(self.url, "/user/1")
        self.assertEqual(self.url2, "/user/3")

    def test_get_show_user_with_valid_id_but_not_own_profile(self):
        user = self._create_second_user()
        self.client.login(username=user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'nu mi place sa joc sah')
        self.assertNotContains(response, 'johndoe@example.org')
        self.assertNotContains(response, 'Chess experience level')
        self.assertTemplateUsed(response, "show_user.html")

    def test_get_show_users_own_profile(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'nu mi place sa joc sah')
        self.assertContains(response, 'johndoe@example.org')
        self.assertContains(response, 'Chess experience level')
        self.assertTemplateUsed(response, "show_user.html")

    def test_correct_user_is_returned(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["user_profile"], self.user)

    # def test_case_when_id_is_incorrect(self):
    #     response = self.client.get(self.url2, follow=True)
    #     redirect_url = reverse("user_list")
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def _create_second_user(self):
        user = User.objects.create_user(
            '@janedoe',
            first_name='Jane',
            last_name='Doe',
            email='janedoe@example.org',
            password='Password123',
            bio="This is Jane's profile.",
            chess_experience_level= 3,
            personal_statement= 'mie imi place sa joc sah!'
        )
        return user
