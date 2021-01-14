from flask import Blueprint, render_template, request
from app.forms import PostsForm, DetailForm
from app.models import Posts, User, Comments, collections
from flask_login import current_user
from flask import flash, redirect, url_for
from app.extensions import db
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostsForm()

    if form.validate_on_submit():
        # 判断用户是否登陆
        if current_user.is_authenticated:
            u = current_user._get_current_object()  # 代理对象，获取当前的登陆用户
            p = Posts(content=form.content.data, user=u)
            db.session.add(p)
            return redirect(url_for('main.index'))
        else:
            flash('登录后才可以发表')
            return redirect(url_for('user.login'))

    # 读取所有的博客
    # posts = Posts.query.filter_by(rid=0).all()
    # 读取分页数据
    page = request.args.get('page', 1, type=int)
    # 只保留发表的博客，按照时间倒叙排序，然后选择一页数据
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=3, error_out=False)
    posts = pagination.items

    return render_template('main/index.html', form=form, posts=posts, pagination=pagination)



@main.route('/post_detail/<id>', methods=['GET', 'POST'])
@login_required
def post_detail(id):
    form = DetailForm()
    post = Posts.query.get(id)  # 文章

    # 读取分页数据
    page = request.args.get('page', 1, type=int)
    pagination = Comments.query.filter_by(pid=id).order_by(Comments.timestamp.desc()).paginate(page, per_page=3, error_out=False)  # 对应文章评论的列表
    comments = pagination.items


    if form.validate_on_submit():
        comment = form.comment.data
        form.comment.data = ''
        c = Comments(content=comment,pid=id, uid=current_user.id)
        db.session.add(c)
        # return render_template('main/post_detail.html', form=form, post=post, comments=comments, id=id, pagination=pagination)
        return redirect(url_for('main.post_detail', form=form, post=post, comments=comments, id=id, pagination=pagination))
    return render_template('main/post_detail.html', form=form, post=post, comments=comments, id=id, pagination=pagination)
