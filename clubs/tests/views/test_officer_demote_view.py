# from django.test import TestCase
# from django.urls import reverse
# from clubs.helpers import reverse_with_next
# from clubs.models import Club, User, Members, Events
#
# class OfficerPromoteTest(TestCase):
#
#     fixtures = [
#         "clubs/tests/fixtures/default_user_jane.json",
#         "clubs/tests/fixtures/default_member_jane_hame.json",
#         "clubs/tests/fixtures/other_users.json",
#         "clubs/tests/fixtures/other_members.json",
#     ]
#
#     def setUp(self):
#         self.user = User.objects.get(email='mikidoe@example.org') #officer
#         self.url = reverse('officer_demote', kwargs={'member_id': self.member.id})
#
#
#
#     def test_officer_promote_url(self):
#         self.assertEqual(self.url,f'/officer_demote/{self.member.id}')
#
#     def
