import os

base_dir = os.path.abspath(os.path.dirname(__file__))


# 通用配置
class Config:
    # 秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'
    # 数据库操作
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 邮件发送
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or '你的邮箱服务器'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '你的邮箱'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '你的邮箱授权码'
    # bootstrap使用本地库
    BOOTSTRAP_SERVE_LOCAL = True

    # 上传文件
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024

    # 上传文件保存的地方
    # UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'static/upload')
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'static/upload')


    # 初始化函数，完成特定环境的初始化
    @staticmethod
    def init_app(app):
        pass


# 开发环境配置
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-dev.sqlite')


# 测试环境配置
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-test.sqlite')


# 生产环境配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog.sqlite')


# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    # 默认环境
    'default': DevelopmentConfig
}
