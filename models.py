from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

challenge_tags = Table(
    'challenge_tags', Base.metadata,
    Column('challenge_id', String, ForeignKey('challenges.challenge_id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class Challenge(Base):
    """
    Models the challenges table
    """
    __tablename__ = 'challenges'

    challenge_id = Column(String, primary_key=True)
    title = Column(String, index=True)
    description = Column(Text)
    category = Column(String, index=True)
    difficulty = Column(String, index=True)
    points = Column(Integer)

    tags = relationship('Tag', secondary=challenge_tags, back_populates='challenges')
    objectives = relationship('Objective', cascade='all, delete-orphan')
    hints = relationship('Hint', cascade='all, delete-orphan')
    conversations = relationship('Conversation', cascade='all, delete-orphan')


class Tag(Base):
    """
    Models the tags table
    """
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    challenges = relationship('Challenge', secondary=challenge_tags, back_populates='tags')


class Objective(Base):
    """
    Models the objectives table
    """
    __tablename__ = 'objectives'
    id = Column(Integer, primary_key=True, autoincrement=True)
    challenge_id = Column(String, ForeignKey('challenges.challenge_id'), index=True)
    content = Column(Text)


class Hint(Base):
    """
    Models the hints table
    """
    __tablename__ = 'hints'
    id = Column(Integer, primary_key=True, autoincrement=True)
    challenge_id = Column(String, ForeignKey('challenges.challenge_id'), index=True)
    content = Column(Text)


class Conversation(Base):
    """
    Models the conversations table
    """
    __tablename__ = 'conversations'
    id = Column(String, primary_key=True)
    topic = Column(String, index=True)
    category = Column(String, index=True)
    challenge_id = Column(String, ForeignKey('challenges.challenge_id'), index=True)
    assigned_to = Column(String, nullable=True, index=True)

    posts = relationship('Post', cascade='all, delete-orphan')


class Post(Base):
    """
    Models the posts table
    """
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, ForeignKey('conversations.id'), index=True)
    user = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    content = Column(Text)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
