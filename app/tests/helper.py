from collections import OrderedDict

from faker import Faker

from app.models import User

locales = OrderedDict(
    [
        ("ko_KR", 1),
        ("en-US", 2),
    ]
)

fake = Faker(locales)


def create_fake_user(phone_number=None, password=None) -> (User, str):
    if not password:
        password = fake.password()
    user = User.objects.create_user(
        phone_number=phone_number or fake.phone_number(), password=password
    )

    return user, password
