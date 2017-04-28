import re
import requests

from enum import Enum


ORACLE_URL = 'https://easy.crypto.uw2017.p4.team/'

WRONG_PADDING = "Invalid padding"
WRONG_JSON = "Could not decode json"


class Result(Enum):
    OK = 1
    WRONG_PADDING = 2
    WRONG_JSON = 3


class Oracle():
    sess = None
    reg = re.compile("<div class=\"alert alert-danger\" role=\"alert\">([\w\W]*?)</div>")

    def __init__(self):
        self.sess = requests.session()

    def check_session(self, token, print_info=False):
        response = self.sess.get(ORACLE_URL, params={
            'session': token
        })

        info = self.reg.search(response.text)

        if print_info:
            print(token)
            if info:
                print(info.group(1).strip())
            else:
                print("Response ok")

        if not info:
            return Result.OK

        info_text = info.group(1).strip()

        if info_text == WRONG_PADDING:
            return Result.WRONG_PADDING
        elif info_text == WRONG_JSON:
            return Result.WRONG_JSON


token = '4d0c549cafa4099d3843a4176068cb35b2d5f7db8234090429eb160740e0cda11d52734367f36382e2a50b11c6e37384d66eeb1171e57e18722bad03228482493ae9f3db15066636df352f13e84b488f3251423aad434cf1ba48a4b8f2a8b662'
token_bad_1 = '4d0c549cafa4099d3843a4176068cb35b2d5f7db8234090429eb160740e0cda11d52734367f36382e2a50b11c6e37384d66eeb1171e57e18722bad03228482493ae9f3db15066636df352f13e84b488f3251423aad434cf1ba48a4b8f2a8b663'
token_bad_2 = '4d0c549cafa4099d3843a4176068cb35b2d5f7db8234090429eb160740e0cda11d52734367f36382e2a50b11c6e37384d66eeb1171e57e18722bad03228482493ae9f3db15066636df352f13e84b488f3251423aad434cf1ba48a4b8f2a8b661'


def solve():
    oracle = Oracle()

    print(oracle.check_session(token))
    print(oracle.check_session(token_bad_1))
    print(oracle.check_session(token_bad_2))


if __name__ == '__main__':
    solve()
