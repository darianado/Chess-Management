from django.test import TestCase
from django.urls import reverse

from clubs.views import show_user

class UserProfileViewTestCase(TestCase):
    def setUp(self):
        #self.user = user_profile.objects.get(username="@johndoe")
        self.url = reverse("show_user", kwargs={"user_id": 1})
        self.url2 = reverse("show_user", kwargs={"user_id": 3})

    def test_show_user_url(self):
        self.assertEqual(self.url, "/user/1")
        self.assertEqual(self.url2, "/user/3")

    def test_get_show_user_with_valid_id(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "show_user.html")

    def test_correct_user_is_returned(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["user"], self.user)

    def test_case_when_id_is_incorrect(self):
        response = self.client.get(self.url2, follow=True)
        redirect_url = reverse("user_list")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
