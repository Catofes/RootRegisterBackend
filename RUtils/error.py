import falcon
from falcon import HTTPError

Error_text = {
    0: ['Unknown Error.',
        falcon.HTTP_500],
    1: ['SQL Error.',
        falcon.HTTP_500],
    2: ['Password Error. Please Contact Admin.',
        falcon.HTTP_403],
    3: ['Error Name',
        falcon.HTTP_403],
    4: ['Error Phone',
        falcon.HTTP_403],
    5: ['Error Email',
        falcon.HTTP_403],
    6: ['Error School',
        falcon.HTTP_403],
    8: ['Duplicate Phone. If You Submitted Wrong Info. Please Contact Admin',
        falcon.HTTP_403],
    9: ['Duplicate Email. If You Submitted Wrong Info. Please Contact Admin',
        falcon.HTTP_403],
    403: ['',
          falcon.HTTP_403],
    404: ['',
          falcon.HTTP_404]
}


class RError(HTTPError):
    def __init__(self, code=0):
        global Error_text
        self.code = code
        if self.code not in Error_text.keys():
            self.code = 0
        self.text = Error_text[self.code][0]
        self.http_code = Error_text[self.code][1]
        HTTPError.__init__(self, self.http_code, self.text, code=self.code)
