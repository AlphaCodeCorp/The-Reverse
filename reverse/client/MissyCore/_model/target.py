from reverse.core import Role
from discord import TextChannel, Guild


class Target(Role):

    def __new__(cls, id: int, channel: TextChannel, name: str, role: Role, guild: Guild):
        return super(Target, cls).__new__(cls, role, guild)

    def __init__(self, id: int, channel: TextChannel, name: str, role: Role, guild: Guild):
        super().__init__(role, guild)
        self.id = id
        self.channel = channel
        self.name = name

    def compare(self, toCompare):
        if self.role == toCompare.role and self.channel == toCompare.channel:
            return True
        else:
            return False