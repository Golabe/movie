from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/movie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# 会员
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号码
    desc = db.Column(db.Text)  # 描述
    face = db.Column(db.String(255), unique=True)  # 头像
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 创建时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识s
    userlogs = db.relationship('UserLog', backref='user')  # 会员日志外键关联
    comment = db.relationship('Comment', backref='user')  # 评论外键关联
    movie_collects = db.relationship('MovieCollect', backref='user')  # 电影收藏外键关联

    def __repr__(self):
        return "<User %r>" % self.name


# 会员登录日志
class UserLog(db.Model):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # IP地址
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 登录时间

    def __repr__(self):
        return "<UserLog %r>" % self.id


# 标签
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间
    movies = db.relationship('Movie', backref='tag')  # 电影外键

    def __repr__(self):
        return "<Tag %r>" % self.name


# 电影
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)  # 地址
    desc = db.Column(db.Text)  # 描述
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    play_num = db.Column(db.BigInteger)  # 播放次数
    comment_num = db.Column(db.BigInteger)  # 评论次数
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签
    area = db.String(db.String(255))  # 地区
    release_time = db.Column(db.Date)  # 发布时间
    length = db.Column(db.String(100))  # 播放时间
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 创建时间
    comment = db.relationship('Comment', backref='movie')  # 评论外键
    movie_collects = db.relationship('MovieCollect', backref='movie')  # 电影收藏外键

    def __repr__(self):
        return "<Movie %r>" % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 创建时间

    def __repr__(self):
        return "<Preview %r>" % self.title


# 评论
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 创建时间

    def __repr__(self):
        return "<Comment %r>" % self.id


# 电影收藏
class MovieCollect(db.Model):
    __tablename__ = 'moviecollect'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 创建时间

    def __repr__(self):
        return "<MovieCollect %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 创建时间

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 创建时间

    def __repr__(self):
        return "<Role %r>" % self.name


# 管理员

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 密码
    is_supper = db.Column(db.SmallInteger)  # 是否为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 创建时间
    admin_logs = db.relationship('AdminLog', backref='admin')  # 管理员登录日志
    op_logs = db.relationship('OpLog', backref='admin')  # 管理员操作日志

    def __repr__(self):
        return "<Admin %r>" % self.name


# 管理员登录日志
class AdminLog(db.Model):
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # IP地址
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 登录时间

    def __repr__(self):
        return "<AdminLog %r>" % self.id


# 操作日志
class OpLog(db.Model):
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # IP地址
    reason = db.Column(db.String(600))  # 操作原因
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 登录时间

    def __repr__(self):
        return "<OpLog %r>" % self.id


if __name__ == '__main__':
    db.create_all()
