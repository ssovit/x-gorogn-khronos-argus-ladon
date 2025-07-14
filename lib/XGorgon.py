
import hashlib
from copy import deepcopy
import time

class XGorgon:
    def __encryption(self):
        tmp = ''
        hex_zu = []
        for i in range(0, 256):
            hex_zu.append(i)
        for i in range(0, 256):
            if i == 0:
                A = 0
            elif tmp:
                A = tmp
            else:
                A = hex_zu[i - 1]
            B = self.hex_str[i % 8]
            if A == 85:
                if i != 1:
                    if tmp != 85:
                        A = 0
            C = A + i + B
            while C >= 256:
                C = C - 256
            if C < i:
                tmp = C
            else:
                tmp = ''
            D = hex_zu[C]
            hex_zu[i] = D
        return hex_zu

    def __initialize(self, input, hex_zu):
        tmp_add = []
        tmp_hex = deepcopy(hex_zu)
        for i in range(self.length):
            A = input[i]
            if not tmp_add:
                B = 0
            else:
                B = tmp_add[-1]
            C = hex_zu[i + 1] + B
            while C >= 256:
                C = C - 256
            tmp_add.append(C)
            D = tmp_hex[C]
            tmp_hex[i + 1] = D
            E = D + D
            while E >= 256:
                E = E - 256
            F = tmp_hex[E]
            G = A ^ F
            input[i] = G
        return input

    def __handle(self, input):
        for i in range(self.length):
            A = input[i]
            B = self.__reverse(A)
            C = input[(i + 1) % self.length]
            D = B ^ C
            E = self.__RBIT(D)
            F = E ^ self.length
            G = ~F
            while G < 0:
                G += 4294967296
            H = int(hex(G)[-2:], 16)
            input[i] = H
        return input

    def __main(self,gorgon):
        result = ''
        for item in self.__handle(self.__initialize(gorgon, self.__encryption())):
            result = result + self.__hex2string(item)
        return '0404{hash1}{hash2}{hash3}{hash4}{hash5}'.format(
            hash1=self.__hex2string(self.hex_str[7]),
            hash2=self.__hex2string(self.hex_str[3]),
            hash3=self.__hex2string(self.hex_str[1]),
            hash4=self.__hex2string(self.hex_str[6]),
            hash5=result)

    def __init__(self):
        self.length = 20
        #self.hex_str = [30, 0, 224,  228,  147,  69,  1,  208]
        self.hex_str=[30, 64, 224, 217, 147, 69, 0, 180]

    def __reverse(self, num):
        tmp_string = hex(num)[2:]
        if len(tmp_string) < 2:
            tmp_string = '0' + tmp_string
        return int(tmp_string[1:] + tmp_string[:1], 16)

    def __RBIT(self, num):
        result = ''
        tmp_string = bin(num)[2:]
        while len(tmp_string) < 8:
            tmp_string = '0' + tmp_string
        for i in range(0, 8):
            result = result + tmp_string[7 - i]
        return int(result, 2)

    def __hex2string(self, num):
        tmp_string = hex(num)[2:]
        if len(tmp_string) < 2:
            tmp_string = '0' + tmp_string
        return tmp_string

    def calculate(self, params:str, headers={}):
        gorgon = []
        headers2 = {}
        Khronos = hex(int(time.time()))[2:]
        url_md5 = hashlib.md5(params.encode("UTF-8")).hexdigest()
        for i in range(0, 4):
            gorgon.append(int(url_md5[2 * i: 2 * i + 2], 16))

        for k, v in headers.items():
            headers2[k.lower()] = v

        if "x-ss-stub" in headers2:
            data_md5 = headers2['x-ss-stub']
            for i in range(0, 4):
                gorgon.append(int(data_md5[2 * i: 2 * i + 2], 16))
        else:
            for i in range(0, 4):
                gorgon.append(0)
        if "cookie" in headers2:
            cookie_md5 = hashlib.md5(
                headers2['cookie'].encode("UTF-8")).hexdigest()
            for i in range(0, 4):
                gorgon.append(int(cookie_md5[2 * i: 2 * i + 2], 16))
        else:
            for i in range(0, 4):
                gorgon.append(0)

        for i in range(0, 4):
            gorgon.append(0)
        for i in range(0, 4):
            gorgon.append(int(Khronos[2 * i: 2 * i + 2], 16))
        return {'X-Gorgon': self.__main(gorgon), 'X-Khronos': str(int(Khronos, 16))}
