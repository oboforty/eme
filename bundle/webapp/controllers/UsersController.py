from email.utils import parseaddr

from flask import render_template, request, url_for
from werkzeug.utils import redirect

from eme.auth import AuthException

from webapp.services import mail, auth


class UsersController():

    def __init__(self, app):
        self.app = app

        self.app.preset_endpoints({
            # multiple routes for the same thing:
            'GET /me': 'Users.get_index',
            'GET /profile': 'Users.get_index',

            # Further demonstrating custom routes
            'GET /login': 'Users.get_login',
            'GET /logout': 'Users.get_logout',
            'GET /register': 'Users.get_register',
        })

    @auth.login_required
    def get_index(self):
        return render_template('/users/profile.html',
           err=request.args.get('err')
        )

    @auth.login_forbidden
    def get_login(self):
        return render_template('/users/login.html',
           err=request.args.get('err')
        )

    @auth.login_forbidden
    def post_login(self):
        username_or_email = request.form['email']
        password = request.form['password']
        remember = bool(request.form.get('remember'))

        is_email = '@' in username_or_email
        try:
            if is_email:
                user = auth.user_manager.get_by_credentials(password, email=username_or_email)
            else:
                user = auth.user_manager.get_by_credentials(password, username=username_or_email)

            if user:
                auth.login_user(user, remember=remember)

                next = request.args.get("next")
                if next:
                    return redirect(next)
                else:
                    return redirect('/')
        except AuthException as e:
            return redirect(url_for('Users.get_login', err=e.reason))

    @auth.login_forbidden
    def get_register(self):
        return render_template('/users/register.html',
           err=request.args.get('err')
        )

    @auth.login_forbidden
    def post_register(self):
        try:
            # todo: itt: update user with default user values
            userDict = request.form.to_dict()
            userDict.update()

            user = auth.user_manager.create(**userDict)

            return redirect(url_for('Users.get_login', err='ok'))
        except AuthException as e:
            return redirect(url_for('Users.get_register', err=e.reason))

    @auth.login_required
    def get_logout(self):
        auth.logout()

        return redirect('/')

    @auth.login_forbidden
    def get_forgot(self):
        return render_template('/users/forgot.html',
           err=request.args.get('err')
        )

    @auth.login_forbidden
    def post_forgot(self):
        email = request.form['email']
        paddr = parseaddr(email)

        if not paddr[1] == email:
            return ''

        code = auth.user_manager.request_forgot_code(email)
        if code:
            mail.send_mail(email, "Password reset", render_template('/mails/forgot.html', code=code))

        return render_template('/users/login.html',
           err='forgot_sent'
        )

    @auth.login_forbidden
    def get_reset(self):
        code = request.args['code']

        user = auth.user_manager.get_by_code(code)

        if not user:
            return redirect('/')

        return render_template('/users/forgot_reset.html',
           code=code,
           err=request.args.get('err')
        )

    @auth.login_forbidden
    def post_reset(self):
        code = request.form['code']
        password = request.form['password']
        password2 = request.form['password-confirm']

        try:
            auth.user_manager.reset_password(code, password, password2)

            return redirect(url_for('Users.get_login', err='reset_success'))
        except AuthException as e:
            return redirect(url_for('Users.get_reset', err=e.reason))
