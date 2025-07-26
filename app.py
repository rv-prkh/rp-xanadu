from datetime import datetime

from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload

from config import DATABASE_URI
from models import Challenge, Conversation, Post

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/challenges')
def user_page():
    return render_template('challenges.html')


@app.route('/admin')
def admin_page():
    return render_template('admin.html')


@app.route('/api/v1/challenges', methods=['GET'])
def get_challenges():
    challenges = db.session.query(Challenge).options(
        joinedload(Challenge.tags),
        joinedload(Challenge.objectives),
        joinedload(Challenge.hints)
    ).all()

    results = []
    for challenge in challenges:
        results.append({
            "challenge_id": challenge.challenge_id,
            "title": challenge.title,
            "description": challenge.description,
            "category": challenge.category,
            "difficulty": challenge.difficulty,
            "points": challenge.points,
            "tags": [tag.name for tag in challenge.tags],
            "learning_objectives": [obj.content for obj in challenge.objectives],
            "hints": [hint.content for hint in challenge.hints]
        })
    return jsonify(results)


@app.route('/api/v1/conversations/<challenge_id>', methods=['GET'])
def get_conversations_for_challenge(challenge_id):
    conversations = (
        db.session.query(Conversation)
        .filter_by(challenge_id=challenge_id)
        .options(joinedload(Conversation.posts))
        .all()
    )
    result = [
        {
            "topic": conv.topic,
            "posts": [
                {
                    "post_id": post.id,
                    "user": post.user,
                    "timestamp": post.timestamp.isoformat(),
                    "content": post.content
                } for post in conv.posts
            ]
        }
        for conv in conversations
    ]
    return jsonify(result)


@app.route('/api/v1/conversations', methods=['GET'])
def get_conversations():
    query = db.session.query(Conversation).options(joinedload(Conversation.posts))
    conversations = query.all()
    result = []
    for conversation in conversations:
        result.append({
            "id": conversation.id,
            "topic": conversation.topic,
            "category": conversation.category,
            "assigned_to": conversation.assigned_to,
            "challenge_id": conversation.challenge_id,
            "posts": [post.to_dict() for post in conversation.posts]
        })
    return jsonify(result)


@app.route('/api/v1/conversations', methods=['POST'])
def create_conversation():
    data = request.get_json()
    conversation = Conversation(
        id=f"CONV_{str(data['timestamp'])}",
        topic=data['topic'],
        category=data['category'],
        challenge_id=data['challenge_id']
    )

    post = Post(
        id=int(datetime.now().timestamp()),
        user=data['user'],
        timestamp=datetime.fromtimestamp(data['timestamp'] / 1000),
        content=data['post_content']
    )
    conversation.posts.append(post)

    db.session.add(conversation)
    db.session.commit()
    return jsonify({"message": "Conversation created", "id": conversation.id}), 201


@app.route('/api/v1/conversations/<conversation_id>/assign', methods=['POST'])
def assign_conversation(conversation_id):
    data = request.get_json()
    conversation = db.session.get(Conversation, conversation_id)
    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404

    conversation.assigned_to = data['assigned_to']
    db.session.commit()
    return jsonify({"message": f"Conversation assigned to {data['assigned_to']}"}), 200


@app.route('/api/v1/conversations/<conversation_id>/reply', methods=['POST'])
def post_reply(conversation_id):
    data = request.get_json()
    conversation = db.session.get(Conversation, conversation_id)
    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404

    post = Post(
        id=int(datetime.now().timestamp()),
        user=data['user'],
        content=data['content'],
        timestamp=datetime.fromtimestamp(data['timestamp'] / 1000),
        conversation_id=conversation_id
    )
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": "Reply posted"}), 201


if __name__ == '__main__':
    app.run()
