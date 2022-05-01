from flask import Flask, jsonify, request, render_template, make_response, session
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
from blog_view import blog
from blog_control.user_mgmt import User
import os

# https 만을 지원하는 기능을 http 에서 테스트할 때 필요한 설정
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
CORS(app)
app.secret_key = 'aiden_server'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'

app.register_blueprint(blog.blog_abtest, url_prefix='/blog')


@login_manager.user_loader
def load_user(user_id):
    # user_id 는 flask_login 이 http request 에서 usesr_id 를 추출해 자동으로 넣어준다.
    return User.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False), 401)


@app.before_request
def app_before_request():
    if 'client_id' not in session:
        session['client_id'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)