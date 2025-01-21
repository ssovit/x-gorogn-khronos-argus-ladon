import binascii
import codecs
import ctypes


class XLOG:
    def encrypt(self, inputStart):
        inputStart = list(inputStart.encode())
        sourceLen = len(inputStart)

        fillCount = 4 - sourceLen % 4

        fillNum = 8 - sourceLen % 8

        if fillNum == 8:
            fillNum = 0

        _bytes = []
        for i in range(sourceLen + fillNum + 8):
            _bytes.append(0)
        eorByte = [0x78, 0x46, 0x8e, 0xc4, 0x74, 0x4c, 0x00, 0x00]
        _bytes[0] = 0x80 | fillNum - 256
        _bytes[1] = 0x30
        _bytes[2] = 0x22
        _bytes[3] = 0x24

        result = "02"

        for i in range(len(inputStart)):
            _bytes[fillCount + i] = inputStart[i]

        for i in range(len(_bytes) // 8):

            sb = ""
            for j in range(8):

                r1 = _bytes[j + 8 * i]

                r2 = eorByte[j]

                if r2 < 0:
                    r2 = r2 + 256
                if r1 < 0:
                    r1 = r1 + 256

                tmp = r1 ^ r2

                if tmp == 0:
                    sb += "00"

                else:
                    sb += self.hex2string(tmp)

            times = self.getHandleCount("78468ec4")
            s = self.calculateRev(sb, times)

            for z in range(8):
                substring = s[2 * z: 2 * z + 2]
                eorByte[z] = int(substring, 16)

            result += s

        result += "78468ec4"

        return binascii.unhexlify(result)

    def decrypt(self, decode):
        decode = decode.hex()
        s = decode[2:]
        strList = []
        for i in range(int(len(s) / 16)):
            input = s[i * 16: i * 16 + 16]
            strList.append(input)
        last = s[(int(len(s) / 16) * 16):]
        strList.append(last)
        times = self.getHandleCount(last)
        _str = ""
        for i in range(len(strList) - 1):
            calculate = self.calculate(strList[i], times)

            if i == 0:
                tmp = last + "744c0000"
                for j in range(8):
                    xor = self.xor(
                        calculate[j * 2:j * 2 + 2], tmp[j * 2: j * 2 + 2])
                    if len(xor) < 2:
                        xor = "0" + xor
                    _str += xor
            if i >= 1:
                tmp = strList[i - 1]
                for j in range(8):
                    xor = self.xor(
                        calculate[j * 2:j * 2 + 2], tmp[j * 2: j * 2 + 2])
                    if len(xor) < 2:
                        xor = "0" + xor
                    _str += xor
        _bytes = codecs.decode(_str, 'hex_codec')

        count = int(_bytes[0]) & 7

        resultLen = (len(decode) // 2) - 13 - count
        count = count % 4
        if count == 0:
            count = 4
        result = bytearray(resultLen)
        for i in range(resultLen):
            result[i] = _bytes[count + i]

        res= bytes(result).decode()
        return res

    def calculate(self, input, times):
        if len(input) != 16:
            return ""
        s108 = ctypes.c_int(0xBFFFE920 << 0).value
        s136 = ctypes.c_int((0x9e3779b9 * times) << 0).value
        s140 = int(input[0:8], 16) << 0 & 0xFFFFFFFF
        s144 = int(input[8:16], 16) << 0 & 0xFFFFFFFF

        for i in range(times):
            r0 = s140
            r2 = s140
            r4 = s140
            r6 = s136
            r5 = s108
            s = format(self.rshift(r6 >> 0xb, 0) >> 0, 'b')
            if len(s) < 3:
                s = "0"
            else:
                s = s[len(s) - 2:]

            r6 = int(s, 2)
            r0 = ctypes.c_int(((self.rshift(r2, 5) ^ r0 << 4) + r4) << 0).value
            r5 = ctypes.c_int(self.getShifting(r5 + (r6 << 2))).value
            r6 = 0x61c88647 << 0 & 0xFFFFFFFF
            r2 = (s136 + r5) << 0 & 0xFFFFFFFF

            r5 = s136
            r0 = r0 ^ r2
            r2 = s108

            r6 = (r6 + r5) << 0 & 0xFFFFFFFF
            r4 = (s144 - r0) << 0 & 0xFFFFFFFF

            r5 = r6 & 3
            r0 = r4 << 4
            r2 = self.getShifting(r2 + (r5 << 2) & 0xFFFFFFFF)
            r0 = ((r0 ^ (self.rshift(r4, 5))) + r4) << 0
            r2 = (r2 + r6) << 0 & 0xFFFFFFFF
            r0 = r0 ^ r2
            s140 = (s140 - r0) << 0 & 0xFFFFFFFF
            s136 = r6 & 0xFFFFFFFF
            s144 = r4 & 0xFFFFFFFF
        str140 = format(self.rshift(s140, 0), 'x')

        str144 = format(self.rshift(s144, 0), 'x')

        if len(str140) < 8:
            count = 8 - len(str140)

            for i in range(count):
                str140 = "0" + str140

        if len(str144) < 8:
            count = 8 - len(str144)
            for i in range(count):
                str144 = "0" + str144

        return str140 + str144

    def xor(self, strHex_X, strHex_Y):
        anotherBinary = format(int(strHex_X, 16), 'b')
        thisBinary = format(int(strHex_Y, 16), 'b')
        result = ""
        if len(anotherBinary) != 8:
            for i in range(len(anotherBinary), 8):
                anotherBinary = "0" + anotherBinary

        if len(thisBinary) != 8:
            for i in range(len(thisBinary), 8):
                thisBinary = "0" + thisBinary
        for i in range(len(anotherBinary)):
            if thisBinary[i] == anotherBinary[i]:
                result += "0"
            else:
                result += "1"

        return format((int(result, 2)), 'x')

    def getHandleCount(self, hex):
        reverse = self.reverse(hex)
        r0 = 0xCCCCCCCD
        r1 = int(reverse, 16)
        r2 = self.getUmullHigh(r1, r0)
        r2 = ctypes.c_int(r2 >> 2).value
        r2 = r2 + ctypes.c_int((r2 << 2)).value
        r1 = r1 - r2
        r2 = 0x20
        r1 = r2 + ctypes.c_int(r1 << 3).value
        return r1

    def getShifting(self, point):
        p = ctypes.c_int(point << 0).value

        if p == ctypes.c_int(0xbfffe920 << 0).value:
            return ctypes.c_int(0x477001de << 0).value
        if p == ctypes.c_int(0xbfffe924 << 0).value:
            return ctypes.c_int(0xfacedead << 0).value
        if p == ctypes.c_int(0xbfffe928 << 0).value:
            return ctypes.c_int(0x30303030 << 0).value
        if p == ctypes.c_int(0xbfffe92c << 0).value:
            return ctypes.c_int(0x39353237 << 0).value
        return 0x00000000

    def calculateRev(self, input, times):
        s108 = 0xbfffe920 << 0 & 0xFFFFFFFF
        s136 = 0x0
        s140 = int(input[0:8], 16) << 0 & 0xFFFFFFFF
        s144 = int(input[8:16], 16) << 0 & 0xFFFFFFFF

        for i in range(times):
            r2 = s108
            r6 = s136
            r4 = s144
            r5 = r6 & 3 & 0xFFFFFFFF
            r0 = r4 << 4 & 0xFFFFFFFF
            r2 = self.getShifting(r2 + (r5 << 2) & 0xFFFFFFFF)
            r0 = ((r0 ^ (self.rshift(r4, 5))) + r4) << 0
            r2 = ctypes.c_int((r2 + r6) << 0 ^ 0).value
            r0 = r0 ^ r2
            s140 = ctypes.c_int((s140 + r0) << 0 ^ 0).value
            s136 = ctypes.c_int((s136 - 0x61c88647) << 0 ^ 0).value

            r5 = s108
            r4 = s140
            r2 = s140
            r0 = s140
            r6 = s136
            s = format(self.rshift((r6 >> 0xb), 0), 'b')
            if len(s) < 3:
                s = "0"
            else:
                s = s[len(s) - 2:]

            r6 = int(s, 2)
            r0 = ctypes.c_int(((self.rshift(r2, 5) ^ r0 << 4) + r4) << 0).value
            r5 = self.getShifting(r5 + (r6 << 2))
            r2 = ctypes.c_int((s136 + r5) << 0 ^ 0).value
            r0 = r0 ^ r2
            s144 = ctypes.c_int((s144 + r0) << 0 ^ 0).value

        str140 = format(self.rshift(s140, 0), 'x')

        str144 = format(self.rshift(s144, 0), 'x')

        if len(str140) < 8:
            count = 8 - len(str140)
            for i in range(count):
                str140 = "0" + str140

        if len(str144) < 8:
            count = 8 - len(str144)
            for i in range(count):
                str144 = "0" + str144

        return str140 + str144

    def reverse(self, hex: str):
        return hex[6:8] + hex[4:6] + hex[2:4] + hex[0:2]

    def rshift(self, val, n):
        return (val % 0x100000000) >> n

    def getUmullHigh(self, r0, r2):
        n1 = r0
        n2 = r2
        result = n1 * n2
        s = format(result, 'x')
        s = s[0: len(s) - 8]
        return int(s, 16)

    def hex2string(self, num: int):
        s = format(num, 'x')
        if len(s) < 2:
            return '0' + s
        return s

    def fch(self, xlog):
        xlog = xlog[0:len(xlog) - 20] # we don't have blank space before closing brack after json.dumps
        fch_str = binascii.crc32(xlog.encode("utf-8"))
        fch_str = str(fch_str)
        for i in range(len(fch_str), 10):
            fch_str = '0' + fch_str
        return xlog + ',"fch":"{fch_str}" }'
