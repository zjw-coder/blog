from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


# 发表博客
class PostsForm(FlaskForm):
    # 若想设置input的指定属性，可以通过render_kw
    # content = TextAreaField('',render_kw={'placeholder' : '这一刻的想法...'}, validators=[Length(1, 9999, message='字数超过限制')])
    content = TextAreaField('',render_kw={'placeholder' : '这一刻的想法...'}, validators=[DataRequired()])
    submit = SubmitField('发表')

# 发表评论
class DetailForm(FlaskForm):
    comment = TextAreaField('', render_kw={'placeholder':'发表点意见...'}, validators=[DataRequired()])
    submit = SubmitField('评论')