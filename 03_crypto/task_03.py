import random
import re
import requests

from enum import Enum


ORACLE_URL = 'https://easy.crypto.uw2017.p4.team/'

WRONG_PADDING = "Invalid padding"
WRONG_JSON = "Could not decode json"

ALPHABET = "0123456789abcdef"


class Result(Enum):
    OK = 1
    WRONG_PADDING = 2
    WRONG_JSON = 3


def get_random_string(n):
    return ''.join(random.choice(ALPHABET) for _ in range(n))


def to_hex_string(number):
    res = "%x" % (number,)
    return res if len(res) % 2 == 0 else '0' + res


def to_int(s):
    return int(s, 16)


class PaddingOracle():
    sess = None
    reg = re.compile("<div class=\"alert alert-danger\" role=\"alert\">([\w\W]*?)</div>")
    token_reg = re.compile("<pre>(\w*?)</pre>")

    def __init__(self):
        self.sess = requests.session()


    def get_token(self):
        response = self.sess.get(ORACLE_URL)

        info = self.token_reg.search(response.text)

        return info.group(1)


    def ask(self, token, print_info=False):
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


    def prepare_attack_token(self, token, block, intermediate_state):
        padding = len(intermediate_state) + 1
        block_start = 32 * (block - 1)
        ciphered_padding = list(map(lambda x: x ^ padding, intermediate_state))
        ciphered_padding_string = ''.join(map(to_hex_string, ciphered_padding))

        return (token[:block_start + 32 - len(intermediate_state) * 2] +
                ciphered_padding_string + token[block_start + 32:])


    def uncipher_block(self, token, block):
        plain_text = ''
        intermediate_state = []
        random_fill = get_random_string(32)
        block_start = 32 * (block - 1)
        attack_token = token[:block_start] + random_fill + token[block_start+32:block_start+64]

        for byte in range(15, -1, -1):
            attack_token = self.prepare_attack_token(attack_token, block, intermediate_state)
            byte_index = block_start + byte * 2
            padding = 16 - byte
            cc = token[byte_index:byte_index+2]
            ci = to_int(cc)

            for b in range(0, 256):
                bs = to_hex_string(b)
                s = attack_token[:byte_index] + bs + attack_token[byte_index+2:]
                r = self.ask(s)

                if r != Result.WRONG_PADDING:
                    res = padding ^ b
                    intermediate_state[:0] = [res]
                    plain_text = chr(res ^ ci) + plain_text
                    print(plain_text)
                    break

        return plain_text


    def uncipher_text(self, token, max_block):
        result = ''

        for x in range(max_block, 0, -1):
            r = self.uncipher_block(token, x)
            result = r + result
            print(result)

        return result


def solve():
    oracle = PaddingOracle()

    token = oracle.get_token()

    print(token)

    max_block = len(token) // 32 - 1

    json_text = oracle.uncipher_text(token, max_block)
    print("=" * 80)
    print(json_text)


if __name__ == '__main__':
    solve()
