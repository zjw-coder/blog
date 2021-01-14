from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, session
from app.forms import RegisterForm, LoginForm, UploadForm, ChangepwdForm, PostsForm, ChangeemailForm
from app.models import User, Posts, collections
from app.extensions import db, photos
from app.email import send_mail
from flask_login import login_user, logout_user, login_required, current_user
import os
from PIL import Image
import time

user = Blueprint('user', __name__)


@user.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 根据表单数据，创建用户对象
        u = User(username=form.username.data,
                 password=form.password.data,
                 email=form.email.data)
        # 将用户对象保存到数据库
        db.session.add(u)
        # 因为下面生成token需要使用id，此时还没有，因此需要手动提交
        db.session.commit()
        # 生成token
        token = u.generate_activate_token()
        # 发送用户账户的激活邮件
        send_mail(u.email, '账户激活', 'email/activate', username=u.username, token=token)
        # 弹出flash消息提示用户
        flash('用户已注册，请点击邮件中的链接以完成激活')
        # 跳转到首页/登录页面
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


@user.route('/activate/<token>')
def activate(token):
    if User.check_activate_token(token):
        flash('账户已激活')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败')
        return redirect(url_for('main.index'))


@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if not u:
            flash('无效的用户名')
        elif not u.confirmed:
            flash('账户尚未激活，请激活后再登录')
        elif u.verify_password(form.password.data):
            login_user(u, remember=form.remember.data)
            flash('登录成功')
            # 若get参数中有next则跳转到next位置，没有则跳转到首页
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('无效的密码')
    return render_template('user/login.html', form=form)


@user.route('/logout/')
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))


@user.route('/test/')
# 路由保护，需要登录才可访问
@login_required
def test():
    return '登录后才可访问的页面'


@user.route('/profile/')
@login_required
def profile():
    return render_template('user/profile.html')

@user.route('/change_icon/', methods=['POST', 'GET'])
@login_required
def change_icon():
    form = UploadForm()

    if form.validate_on_submit():
        # 获取后缀
        suffix = os.path.splitext(form.icon.data.filename)[-1]
        filename = random_string() + suffix
        photos.save(form.icon.data, name=filename)

        # 生成缩略图
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
        img = Image.open(pathname)
        img.thumbnail((128,128))
        img.save(pathname)

        # 删除原来的头像(不是默认的头像才删除)
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon))

        # 保存修改至数据库/
        current_user.icon = filename
        db.session.add(current_user)

        flash('头像已经保存')
        return redirect(url_for('user.change_icon'))
    img_url = photos.url(current_user.icon)
    return render_template('user/change_icon.html', form=form, img_url=img_url)


def random_string(length = 32):
    import random
    base_str = 'qwertyuioplkjhgfdsazxcvbnm0987654321'
    return ''.join([random.choice(base_str) for i in range(length)])


# 修改密码
@user.route('/change_pwd/', methods=['GET', 'POST'])
def change_pwd():
    form = ChangepwdForm()

    if form.validate_on_submit():
        oldpassword = form.oldpassword.data
        newpassword = form.newpassword.data
        u = User.query.filter_by(username=current_user.username).first()
        # 旧密码校验通过
        if u.verify_password(oldpassword):
            current_user.password=newpassword
            db.session.add(current_user)
            logout_user()
            flash('密码修改成功，请重新登陆')
            return redirect(url_for('user.login'))
        # 不通过
        flash('旧密码确认出错')
        return redirect(url_for('user.change_pwd'))
    return render_template('user/change_pwd.html', form=form)

# 修改邮箱
@user.route('/change_email/', methods=['POST', 'GET'])
def change_email():
    form = ChangeemailForm()

    if form.validate_on_submit():
        email = form.email.data
        form.email.data = ''

        # 判断邮箱
        if email == current_user.email:
            flash('新邮箱不能与旧邮箱一致')
            return render_template('user/change_email.html', form=form)
        if User.query.filter_by(email=email).first():
            flash('该邮箱已注册，请选用其他邮箱')
            return render_template('user/change_email.html', form=form)
        else:
            session['temp_email'] = email
            # 生成token
            token = int(time.time())
            # 发送用户账户的激活邮件
            send_mail(email, '账户激活', 'email/change', username=current_user.username, token=token)

            # 弹出flash消息提示用户
            flash('请点击邮件中的链接以完成确认更改')
            return redirect(url_for('main.index'))
    return render_template('user/change_email.html', form=form)

@user.route('/confirm_email/<token>')
def confirm_email(token):
    # return str(int(time.time()) - int(token))
    if (int(time.time()) - int(token)) < 3600:
        current_user.email = session.get('temp_email')
        db.session.add(current_user)
        session.pop('temp_email', None)
        flash('邮箱修改成功')
        return redirect(url_for('main.index'))
    else:
        session.pop('temp_email', None)
        flash('邮箱修改失败')
        return redirect(url_for('main.index'))

@user.route('/mine/', methods=['POST', 'GET'])
@login_required
def mine():
    form = PostsForm()

    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.filter_by(uid=current_user.id).order_by(Posts.timestamp.desc()).paginate(page, per_page=3, error_out=False)
    mine_posts = pagination.items

    if form.validate_on_submit():
        u = current_user._get_current_object()  # 代理对象，获取当前的登陆用户
        p = Posts(content=form.content.data, user=u)
        db.session.add(p)
        return redirect(url_for('user.mine'))

    # return mine_posts.content
    return render_template('user/mine.html', form=form, mine_posts=mine_posts, pagination=pagination)

# 我收藏的
@user.route('/favorite/')
@login_required
def favorite():
    page = request.args.get('page', 1, type=int)
    # 只保留我收藏的博客，按照时间倒叙排序，然后选择一页数据
    lis = []
    for i in current_user.favorites.all():
        lis.append(i.id)
    pagination = Posts.query.filter(Posts.id.in_(lis)).order_by(Posts.timestamp.desc()).paginate(page, per_page=3,
                                                                                        error_out=False)
    posts = pagination.items
    return render_template('user/my_favorites.html', posts=posts, pagination=pagination)