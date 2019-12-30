from email.utils import parseaddr

from flask import render_template, request
from werkzeug.utils import redirect

from game.instance import users
from webapp.services import login, mail

from .UserManager import UserException, UserManager


userManager = UserManager(users)


class UsersControllerBase():
    def __init__(self, server):
        self.server = server
        self.name = "Users"


    def get_index(self):
        user = login.getUser()

        return render_template('/users/profile.html',
           err=request.args.get('err')
        )


    def get_login(self):
        if login.getUser().username:
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
                user = userManager.authenticateCredentials(password, email=username_or_email)
            else:
                user = userManager.authenticateCredentials(password, username=username_or_email)

            if user:
                #login.logout()
                login.setUser(user, remember=remember)

                next = request.args.get("next")
                if next:
                    return redirect(next)
                else:
                    return redirect('/')
        except UserException as e:
            return redirect('/users/login?err={}'.format(e.reason))


    def get_register(self):
        if login.getUser().username:
            return redirect('/users')

        return render_template('/users/register.html',
           err=request.args.get('err')
        )


    def post_register(self):
        try:
            user = userManager.create(**request.form.to_dict())

            return redirect('/users/login?err=ok')
        except UserException as e:
            return redirect('/users/register?err={}'.format(e.reason))


    @login.login_required
    def get_logout(self):
        login.logout()

        return redirect('/users/login')

    def get_forgot(self):
        if login.getUser().username:
            return redirect('/users')

        return render_template('/users/forgot.html',
           err=request.args.get('err')
        )


    def post_forgot(self):
        email = request.form['email']
        paddr = parseaddr(email)

        if not paddr[1] == email:
            return ''

        code = userManager.forgot(email)
        if code:
            mail.send_mail(email, "Password reset", render_template('/mails/forgot.html', code=code))

        return render_template('/users/login.html',
           err='forgot_sent'
        )


    def get_reset(self):
        if login.getUser().username:
            return redirect('/users')

        code = request.args['code']

        user = userManager.authenticateCode(code)

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
            userManager.reset_password(code, password, password2)

            return redirect('/users/login?err={}'.format("reset_success"))
        except UserException as e:
            return redirect('/users/reset?err={}'.format(e.reason))
