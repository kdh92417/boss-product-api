import random
from collections import OrderedDict

from faker import Faker

from app.models import User, Product
from app.models.product import SizeType

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


def create_product(
    category=None,
    barcode=None,
    price=None,
    cost=None,
    name=None,
    description=None,
    expiration_date=None,
    size=None,
    user: User = None,
):
    if not user:
        user, _ = create_fake_user()

    product = Product.objects.create(
        category=category or fake.name(),
        barcode=barcode or fake.ssn(),
        price=price or random.randint(1, 100) * 1000,
        cost=cost or random.randint(1, 100) * 1000,
        name=name or fake.name(),
        description=description or fake.paragraph(nb_sentences=5),
        expiration_date=expiration_date or fake.date(),
        size=size or random.choice(SizeType.values),
        user=user,
    )
    return product


def create_product_list(n: int = 5, user: User = None) -> [Product]:
    product_list = []
    for _ in range(n):
        product = create_product(user=user)
        product_list.append(product)

    return product_list
