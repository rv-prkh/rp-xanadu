import unittest
import json
from app import app, db
from models import Conversation
from flask_testing import TestCase
from datetime import datetime

class APITestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        self.tearDown()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_challenges(self):
        response = self.client.get('/api/v1/challenges')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreaterEqual(len(data), 30)
        self.assertEqual(data[0]["title"], "Begin Here")

    def test_get_conversations_for_challenge(self):
        response = self.client.get('/api/v1/conversations/CHAL_111')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(any("Test Topic" in conv["topic"] for conv in data))

    def test_get_all_conversations(self):
        response = self.client.get('/api/v1/conversations')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreaterEqual(len(data), 60)

    def test_create_conversation(self):
        payload = {
            "topic": "New Topic",
            "category": "Support",
            "user": "user123",
            "timestamp": int(datetime.utcnow().timestamp() * 1000),
            "post_content": "Help me",
            "challenge_id": "CHAL_111"
        }
        response = self.client.post('/api/v1/conversations', json=payload)
        self.assertEqual(response.status_code, 201)

    def test_assign_conversation(self):
        payload = {"assigned_to": "admin1"}
        response = self.client.post('/api/v1/conversations/CONV_333/assign', json=payload)
        self.assertEqual(response.status_code, 200)
        updated = db.session.get(Conversation, "CONV_333")
        self.assertEqual(updated.assigned_to, "admin1")

    def test_reply_to_conversation(self):
        payload = {
            "user": "admin",
            "content": "We’re looking into this.",
            "timestamp": int(datetime.utcnow().timestamp() * 1000)
        }
        response = self.client.post('/api/v1/conversations/CONV_333/reply', json=payload)
        self.assertEqual(response.status_code, 201)
        posts = db.session.get(Conversation, "CONV_333").posts
        self.assertTrue(any(p.user == "admin" for p in posts))


if __name__ == '__main__':
    unittest.main()
