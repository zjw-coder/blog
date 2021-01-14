from .user import User
from .posts import Posts
from .comments import Comments

# 添加用户与帖子的收藏中间关联
from app.extensions import db
collections = db.Table('collections',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)