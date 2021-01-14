from flask import Blueprint, jsonify, redirect, render_template, url_for
from flask_login import current_user, login_required
from app.forms import PostsForm
from app.models import Posts
from app.extensions import db

posts = Blueprint('posts', __name__)

@posts.route('/collect/<int:pid>')
def collect(pid):
    # 判断是否收藏

    # 如果已收藏
    if current_user.is_favorite(pid):
        # 取消收藏
        current_user.del_favorite(pid)
        c = Posts.query.filter_by(id=pid).first()
        if c.collect_count > 0:
            c.collect_count = c.collect_count - 1
        db.session.add(c)
        db.session.commit()

        # 否则添加收藏
    else:
        current_user.add_favorite(pid)
        c = Posts.query.filter_by(id=pid).first()
        c.collect_count = c.collect_count + 1
        db.session.add(c)
        db.session.commit()
    return redirect(url_for('main.index'))

# 发表博客
@posts.route('/pub/', methods=['GET', 'POST'])
@login_required
def pub():
    form = PostsForm()

    if form.validate_on_submit():
        u = current_user._get_current_object()  # 代理对象，获取当前的登陆用户
        p = Posts(content=form.content.data, user=u)
        db.session.add(p)
        return render_template('posts/success.html')

    return render_template('posts/pub.html', form=form)