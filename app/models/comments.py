from app.extensions import db
from datetime import datetime

# 博客评论
class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)  # 对应文章的id
    uid = db.Column(db.Integer)  # 发表评论对应的用户id
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)