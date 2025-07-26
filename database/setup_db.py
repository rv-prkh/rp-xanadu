"""Simple script to set up the database"""
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI
from models import Base, Challenge, Tag, Objective, Hint, Conversation, Post

engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    """Initialize the database"""
    Base.metadata.create_all(engine)


def load_challenges():
    """
    Loads challenges from json file
    """
    with open('pennylane_coding_challenges.json') as file:
        data = json.load(file)

    for coding_challenge in data['coding_challenges']:
        challenge = Challenge(
            challenge_id=coding_challenge['challenge_id'],
            title=coding_challenge['title'],
            description=coding_challenge['description'],
            category=coding_challenge['category'],
            difficulty=coding_challenge['difficulty'],
            points=coding_challenge['points']
        )

        for tag_name in coding_challenge['tags']:
            tag = session.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            challenge.tags.append(tag)

        challenge.objectives = [Objective(content=o) for o in coding_challenge['learning_objectives']]
        challenge.hints = [Hint(content=h) for h in coding_challenge['hints']]

        session.add(challenge)
    session.commit()


def load_conversations():
    """
    Loads conversations from json file
    """
    with open('pennylane_support_conversations.json') as f:
        data = json.load(f)

    for support_conversation in data['support_conversations']:
        conversation = Conversation(
            id=support_conversation['identifier'],
            topic=support_conversation['topic'],
            category=support_conversation['category'],
            challenge_id=support_conversation['challenge_id']
        )

        for post_data in support_conversation['posts']:
            post = Post(
                id=post_data['post_id'],
                user=post_data['user'],
                timestamp=post_data['timestamp'],
                content=post_data['content']
            )
            conversation.posts.append(post)

        session.add(conversation)
    session.commit()


if __name__ == '__main__':
    # Initializes the DB
    init_db()
    print("Database initialized")

    # Loads database with data
    load_challenges()
    load_conversations()
    print("Database populated.")
