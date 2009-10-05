from django.test import TestCase

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from djangoratings.fields import RatingField

rating_field = RatingField(weight=0, range=5, allow_multi_vote=True)
rating_field.contribute_to_class(Site, 'rating')

class MultiVoteTest(TestCase):
        
    def test_multi_vote(self):
        """
        Test to rate the same object multiple times by the same user
        """
        site = Site.objects.get_current()
        
        user, created = User.objects.get_or_create(username='testuser')
        
        site.rating.add(1, user, '127.0.0.1')
        site.rating.add(2, user, '127.0.0.1')
        site.rating.add(3, user, '127.0.0.1')
        
        self.failUnlessEqual(site.rating.get_rating(), 2)
        self.failUnlessEqual(site.rating.votes, 3)
        self.failUnlessEqual(site.rating.score, 6)
        