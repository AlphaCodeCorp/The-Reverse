from reverse.core import Role
from discord import TextChannel, Guild


class Target(Role):

    def __new__(cls, id: int, channel: TextChannel, name: str, role_id: int, guild: Guild):
        return super(Target, cls).__new__(cls, role_id, guild)

    def __init__(self, id: int, channel: TextChannel, name: str, role_id: int, guild: Guild):
        super().__init__(role_id, guild)
        self.id = id
        self.channel = channel
        self.name = name

    def compare(self, toCompare):
        return True