from django.test import TestCase
from django.urls import reverse
from clubs.models import Club

class ShowUserTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            club_name='London Chess Club',
            location='SE14XA',
            description='The quick brown fox jumps over the lazy dog.'
        )
        self.url = reverse('show_club', kwargs={'club_id': self.club.id})

    def test_show_club_url(self):
        self.assertEqual(self.url,f'/club/{self.club.id}')

    # def test_get_show_club_with_valid_id(self):
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'show_club.html')
    #     self.assertContains(response, "London Chess Club")

    def test_get_show_user_with_invalid_id(self):
        url = reverse('show_club', kwargs={'club_id': self.club.id+1})
        response = self.client.get(url, follow=True)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_list.html')
        

        # tests for apply button and leave button

        #test for resend button

