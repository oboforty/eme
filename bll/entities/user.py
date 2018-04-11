

class User():
    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.token = kwargs.get('token')
        self.salt = kwargs.get('salt')

        # business-related properties can be added here
        # self.virtualMoney = kwargs['virtualMoney']
