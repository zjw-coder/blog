from app.extensions import db
from datetime import datetime

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, index=True, default=0)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    collect_count = db.Column(db.Integer, default=0)

    # 添加关联外键:   表名.字段名
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
