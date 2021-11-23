from django.test import TestCase
from django.urls import reverse
from clubs.models import Club

class ClubListTest(TestCase):
    def setUp(self):
        self.url = reverse('club_list')

    def test_club_list_url(self):
        self.assertEqual(self.url,'/clubs/')

    def test_get_club_list(self):
        self._create_test_clubs(15)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_list.html')
        self.assertEqual(len(response.context['clubs']), 15)
        for club_id in range(15):
            self.assertContains(response, f'Name{club_id}')
            self.assertContains(response, f'Location{club_id}')
            club = Club.objects.get(club_name=f'Name{club_id}')
            club_url = reverse('show_club', kwargs={'club_id': club.id})
            self.assertContains(response, club_url)

    def _create_test_clubs(self, club_count=10):
        for club_id in range(club_count):
            Club.objects.create(
                club_name=f'Name{club_id}',
                location=f'Location{club_id}',
                description=f'Description{club_id}',
            )
