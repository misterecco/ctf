import io
import logging
import qrcode
import requests
import http.client as http_client
from PIL import Image


CODE_DIM = (400, 400)
OFFSET = (350, 50)
TICKET_PATH = 'free_ticket.png'
LOGIN_URL = 'https://easy.web.uw2017.p4.team/login'
VALIDATE_URL = 'https://easy.web.uw2017.p4.team/validate'
TICKET_OK = 'Twój bilet jest poprawny  i znajduje się w naszej bazie danych'
TICKET_WRONG = 'Twój bilet ma niepoprawny typ i nie znajduje się w naszej bazie danych'


def debug_on():
    http_client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


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


class EasyWeb():
    sess = None

    def login(self, username, password):
        login_data = {
            'username': username,
            'password': password,
        }

        self.sess = requests.session()
        response = self.sess.post(LOGIN_URL, data=login_data)


    def check_ticket(self, content):
        ticket = create_ticket_file(content)
        files = {
            'ticket': ('ticket.png', ticket)
        }

        response = self.sess.post(
            VALIDATE_URL,
            files=files,
        )

        # print(response.text)
        return TICKET_OK in response.text


if __name__ == '__main__':
    ew = EasyWeb()
    ew.login('tomek', 'kolejarz')

    r = ew.check_ticket("103b7c2f9abde8ab9f812f9e09b1acaabb8c46f1b5eefdfde65e00b654a0d3d7")
    print(r)
