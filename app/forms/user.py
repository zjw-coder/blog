from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.validators import ValidationError
from app.models import User
from flask_wtf.file import FileAllowed, FileRequired, FileField
from app.extensions import photos
from flask_login import current_user

# 用户注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(4, 20, message='用户名只能在4~20个字符之间')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 20, message='密码长度必须在6~20个字符之间')])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message='两次密码不一致')])
    email = StringField('邮箱', validators=[Email(message='邮箱格式不正确')])
    submit = SubmitField('立即注册')

    # 自定义字段验证函数，验证username
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户已注册，请选用其它用户名')

    # 自定义字段验证函数，验证email
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册，请选用其它邮箱')


# 用户登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember = BooleanField('记住我')
    submit = SubmitField('立即登录')

# 头像上传表单
class UploadForm(FlaskForm):
    icon = FileField('头像', validators=[FileRequired('请选择文件'), FileAllowed(photos, '只能上传图片')])
    submit = SubmitField('上传')

# 修改密码
class ChangepwdForm(FlaskForm):
    oldpassword = PasswordField('旧密码', validators=[DataRequired()])
    newpassword = PasswordField('新密码', validators=[DataRequired()])
    confirm = PasswordField('确认密码', validators=[EqualTo('newpassword', message='两次密码不一致')])
    submit = SubmitField('修改密码')

class ChangeemailForm(FlaskForm):
    email = StringField('', render_kw={'placeholder':'输入邮箱'}, validators=[Email(message='邮箱格式不正确')])
    submit = SubmitField('修改邮箱')

