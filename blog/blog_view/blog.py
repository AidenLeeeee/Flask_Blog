from flask import Flask, Blueprint, jsonify, request, render_template, redirect, url_for
from flask_login import login_user, current_user, logout_user
from blog_control.user_mgmt import User
import datetime

blog_abtest = Blueprint('blog', __name__)

@blog_abtest.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'GET':
        # print(request.args.get('user_email'))
        return redirect(url_for('blog.test_blog'))
    else:
        user_email = request.form['user_email']
        user = User.create(user_email, 'A')
        login_user(user, remember=True, duration=datetime.timedelta(days=365))
        # login_user(user)

        return redirect(url_for('blog.test_blog'))
        # content-type : application/x-www-form-urlencoded ---> html form 'POST'
        # data = request.form['user_email']
        
        # content-type : application/json ---> REST API 'POST'
        # data = request.get_json()

    # print(request.headers) ---> Request Headers
    # print(request.args.get('user_email')) ---> html form 'GET'

    # return redirect('/blog/test_blog')
    # return make_response(jsonify(success=True), 200)


@blog_abtest.route('/test_blog')
def test_blog():
    if current_user.is_authenticated:
    # current_user.is_authenticated 호출 시, login_manager.user_loader 의 load_user() 실행
    # load_user() 는 User.get() 함수의 리턴값을 반환하고 current_user 에 담는다.
        return render_template('blog_A.html', user_email=current_user.user_email)
    else:
        return render_template('blog_A.html')


@blog_abtest.route('/logout')
def logout():
    User.delete(current_user.id)
    logout_user()
    return redirect(url_for('blog.test_blog'))