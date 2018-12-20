import random
import string

SourceIp = str


def generate_random_ip():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
