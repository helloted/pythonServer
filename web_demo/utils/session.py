from functools import wraps
import json

def login_required(func):
    @wraps(func)
    def token_verfiy(self,*args, **kwargs):
        session = self.get_secure_cookie('session_save')
        print 'session',session
        if session:
            return func(self, *args, **kwargs)
        else:
            data = {}
            data['code'] = 4
            data['msg'] = 'you need login'
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            self.add_header("Access-Control-Allow-Origin", self.request.headers.get('Origin'))
            self.add_header("Access-Control-Allow-Credentials", 'true')
            self.write(json.dumps(data))
    return token_verfiy