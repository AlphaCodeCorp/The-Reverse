from reverse.core import Role
from discord import TextChannel


class Target(Role):

    def __init__(self, id: int, role: Role, channel: TextChannel, name: str):
        self.id
        self.role = role
        self.channel = channel
        self.guild = None
        super().__init__()

    def compare(self, toCompare):
        if self.role == toCompare.role and self.channel == toCompare.channel:
            return True
        else:
            return False