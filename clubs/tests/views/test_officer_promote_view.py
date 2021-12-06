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
#         self.user = User.objects.get(email='janedoe@example.org') #owner
#         self.userMiki = User.objects.get(email='mikidoe@example.org') #officer
#
#
#
#     def test_officer_promote_url(self):
#         self.assertEqual(self.urlHame,f'/club/{self.clubHame.id}')
