from core._models.role import Role

class Target(Role):

    def __init__(self, role_id: int, channel_id: int):
        self.role_id = role_id
        self.channel_id = channel_id