from dataclasses import dataclass
from typing import List

userid = 0


@dataclass
class User:
    identifier: str
    email: str
    profile_picture_src: str
    friends: List[str]
    sent_invitations: List[str]
    pending_invitations: List[str]

    @staticmethod
    def generate_id():
        global userid
        userid += 1
        return userid
