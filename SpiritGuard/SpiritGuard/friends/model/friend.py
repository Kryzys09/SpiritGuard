from dataclasses import dataclass


@dataclass
class Friend:
    """For serving jinja template during generating list of friends"""
    name: str
    profile_picture_src: str
    currently_partying: bool

