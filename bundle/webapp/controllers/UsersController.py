from email.utils import parseaddr

from flask import render_template, request
from werkzeug.utils import redirect

from eme.auth import UserManager, AuthException

from webapp.services import mail, auth


class UsersController():

    def __init__(self, server):
        self.server = server
        self.name = "Users"

    @auth.login_required
    def get_index(self):
        user = auth.get_user()

        return render_template('/users/profile.html',
           err=request.args.get('err')
        )


    def get_login(self):
        if auth.get_user().username:
            return redirect('/')

        return render_template('/users/login.html',
           err=request.args.get('err')
        )


    def post_login(self):
        username_or_email = request.form['email']
        password = request.form['password']
        remember = bool(request.form.get('remember'))

        is_email = '@' in username_or_email
        try:
            if is_email:
                user = auth.user_manager.authenticateCredentials(password, email=username_or_email)
            else:
                user = auth.user_manager.authenticateCredentials(password, username=username_or_email)

            if user:
                #login.logout()
                auth.set_user(user, remember=remember)

                next = request.args.get("next")
                if next:
                    return redirect(next)
                else:
                    return redirect('/')
        except AuthException as e:
            return redirect('/users/login?err={}'.format(e.reason))


    def get_register(self):
        if auth.get_user().username:
            return redirect('/users')

        return render_template('/users/register.html',
           err=request.args.get('err')
        )


    def post_register(self):
        try:
            # todo: itt: update user with default user values
            userDict = request.form.to_dict()
            userDict.update()

            user = auth.user_manager.create(**userDict)

            return redirect('/users/login?err=ok')
        except AuthException as e:
            return redirect('/users/register?err={}'.format(e.reason))


    @auth.login_required
    def get_logout(self):
        auth.logout()

        return redirect('/users/login')

    def get_forgot(self):
        if auth.get_user().username:
            return redirect('/users')

        return render_template('/users/forgot.html',
           err=request.args.get('err')
        )


    def post_forgot(self):
        email = request.form['email']
        paddr = parseaddr(email)

        if not paddr[1] == email:
            return ''

        code = auth.user_manager.forgot(email)
        if code:
            mail.send_mail(email, "Password reset", render_template('/mails/forgot.html', code=code))

        return render_template('/users/login.html',
           err='forgot_sent'
        )


    def get_reset(self):
        if auth.get_user().username:
            return redirect('/users')

        code = request.args['code']

        user = auth.user_manager.authenticateCode(code)

        if not user:
            return redirect('/users')

        return render_template('/users/forgot_reset.html',
           code=code,
           err=request.args.get('err')
        )


    def post_reset(self):
        code = request.form['code']
        password = request.form['password']
        password2 = request.form['password-confirm']

        try:
            auth.user_manager.reset_password(code, password, password2)

            return redirect('/users/login?err={}'.format("reset_success"))
        except AuthException as e:
            return redirect('/users/reset?err={}'.format(e.reason))
