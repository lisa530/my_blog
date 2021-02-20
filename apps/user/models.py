from datetime import datetime

from exts import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(30))
    icon = db.Column(db.String(100))
    isdelete = db.Column(db.Boolean, default=False)
    rdatetime = db.Column(db.DateTime, default=datetime.now)
    # 增加一个关联字段，在Article类中增加一个uesr属性
    # 通过用户查询文章，user.articles，根据文章查询用户：article.user
    articles = db.relationship('Article', backref='user')
    # 增加关联字段，根据用户找评论(user.comments),根据评论找用户(comments.user)
    comments = db.relationship('Comment', backref='user')

    def __str__(self):
        return self.username


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo_name = db.Column(db.String(50), nullable=False)
    photo_datetime = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return self.photo_name
