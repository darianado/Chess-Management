# from django.test import TestCase
# from django.urls import reverse
# from clubs.models import User, Events
# from clubs.tests.helper import reverse_with_next
#
# class EventListTest(TestCase):
#
#     fixtures = [
#         "clubs/tests/fixtures/default_user_john.json",
#     ]
#
#     def setUp(self):
#         self.url = reverse('event_list')
#         self.userJohn = User.objects.get(email="johndoe@example.org")
#
#     def test_event_list_url(self):
#         self.assertEqual(self.url,'/home/dashboard')
#
#     def test_get_event_list_when_not_logged_in(self):
#         response = self.client.get(self.url)
#         redirect_url = reverse("log_in")
#         self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
#
#     def test_get_event_list(self):
#         self.client.login(email=self.userJohn.email, password="Password123")
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'events_list.html')
