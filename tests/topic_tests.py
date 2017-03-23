import os
import unittest
import webapp2
import webtest
import uuid
from google.appengine.ext import testbed

from handlers.comments import CommentAdd
from main import MainHandler
from handlers.topics import TopicAdd, TopicDetails, DeleteTopic
from google.appengine.api import users, memcache


class TopicTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/', MainHandler, name="main-page"),
                webapp2.Route('/topic/add', TopicAdd, name="topic_add"),
                webapp2.Route('/topic/<topic_id:\d+>', TopicDetails, name="topic-details"),
                webapp2.Route('/topic/<topic_id:\d+>/comment/add', CommentAdd, name="comment-add"),
                webapp2.Route('/topic/<topic_id:\d+>/delete', DeleteTopic, name="delete-topic"),
            ])

        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        """ Uncomment the stubs that you need to run tests. """
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # self.testbed.init_mail_stub()
        # self.testbed.init_taskqueue_stub()
        self.testbed.init_user_stub()
        # ...

        """ Uncomment if you need user (Google Login) and if this user needs to be admin. """
        os.environ['USER_EMAIL'] = 'some.user@example.com'
        # os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()

    def test_add_topic_handler(self):
        # GET zahteva
        get = self.testapp.get('/topic/add')  # get  add topic handler
        self.assertEqual(get.status_int, 200)  # if GET request was ok, it should return 200 status code
        self.assertIn("Add new topic", get.body)

        # POST zahteva
        title = "Moj testni topic"
        content = "blabafbj"

        csrf = str(uuid.uuid4())
        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value=True, time=3600)

        params = {"title": title, "text": content, "csrf_token": csrf_token}

        post = self.testapp.post('/topic/add', params=params)
        self.assertEqual(post.status_int, 302)

