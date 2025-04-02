# Cookie Setter: Wrap AT, RT in Cookes
from rest_framework.response import Response
class CookieHandler:
    def __init__(self):
        pass

    def set_cookies(self, response: Response, cookies: dict):
        """
        Wrap Tokens in Cookies
        """
        # secure = not settings.DEBUG  # 如果是開發模式 (DEBUG=True)，secure=False
        for (key, value) in cookies.items():
            print(key, value)
            if value:
                response.set_cookie(
                key= key,
                value= value,
                httponly= True,
                secure= True, # only passing through https and also run in localhost
                samesite= 'None',
                path= "/"
                # domain= "localhost"
            )