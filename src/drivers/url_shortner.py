from random import SystemRandom
import string

def generate_short_url(length = 8) -> str:
    return "".join(SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))
