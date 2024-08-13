import random
import string
from datetime import timedelta

def generate_verification_code(length=6):
    """ Tasdiqlash kodi uchun tasodifiy raqam va harflardan iborat kod yaratadi """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

