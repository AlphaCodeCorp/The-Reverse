from core._models.role import Role
from discord import Channel

class Target(Role):

    def __init__(self, id: int, role: Role, channel: Channel, name: String):
        self.id
        self.role = role
        self.channel = channel
        self.guild = guild
        super().__init__()

    @staticmethod
    def compare(toCompare: Target):
        if self.role == toCompare.role and self.channel == toCompare.channel:
            return True
        else:
            return False