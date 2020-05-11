import random
from typing import List

from faker import Faker

from SpiritGuard.friends.model.friend import Friend

fk = Faker()


def create_img_url(id):
    sex = 'men' if rand_bool() else 'women'
    src = "https://randomuser.me/api/portraits/{}/{}.jpg".format(sex, id)
    return src


def get_mock_friends() -> List[Friend]:
    return [Friend(fk.name(), create_img_url(id), rand_bool()) for id in range(5, 21)]


def rand_bool():
    return random.randint(0, 10) & 1 == 1
