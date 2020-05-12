import random
from typing import List

from faker import Faker

from SpiritGuard.friends.model.friend import Friend

fk = Faker()

RANDOM_IMAGE_URL_TEMPLATE = "https://randomuser.me/api/portraits/{}/{}.jpg"


def create_random_img_url():
    sex = 'men' if rand_bool() else 'women'
    identifier = random.choice([i for i in range(5, 100)])
    src = RANDOM_IMAGE_URL_TEMPLATE.format(sex, identifier)
    return src


def create_img_url(identifier):
    sex = 'men' if rand_bool() else 'women'
    src = RANDOM_IMAGE_URL_TEMPLATE.format(sex, identifier)
    return src


def get_mock_friends() -> List[Friend]:
    return [Friend(fk.name(), create_img_url(identifier), rand_bool()) for identifier in range(5, 21)]


def rand_bool():
    return random.randint(0, 10) & 1 == 1
