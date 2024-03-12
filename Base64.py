import string


class Base64:
    base64_string = string.ascii_uppercase + \
        string.ascii_lowercase + \
        string.digits + \
        "+/"

    def __init__(self, text):
        self.text = text

    @staticmethod
    def char_to_bit(char: str):
        string = bin(ord(char))[2:]
        return '0' * (8 - len(string)) + string

    @classmethod
    def bit_to_base64(cls, bit: str):
        return cls.base64_string[eval(f"0b{bit}")]

    def encode(self):
        string_of_ascii = "".join(
            [self.char_to_bit(char) for char in self.text]
        )
        # pad 0
        if m := (len(string_of_ascii) % 6):
            string_of_ascii += '0' * (6 - m)

        string_of_base64 = "".join(
            [self.__class__.bit_to_base64(
                string_of_ascii[6*i: 6*(i+1)]) for i in range(int(len(string_of_ascii)/6))]
        )

        # pad =
        if m := (len(string_of_base64) % 4):
            string_of_base64 += "=" * (4 - m)

            return string_of_base64


if __name__ == "__main__":
    test = Base64("Ma")
    print(
        test.encode()
    )
