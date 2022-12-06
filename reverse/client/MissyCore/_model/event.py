import random, datetime
from .assignation import Assignation
from .target import Target
from discord import Embed

class Event():

    listAssignations = ["Animateur", "Secretaire", "Scribe", "Gestionnaire"]

    def __init__(self, _createAt: datetime.date, _startOn: str, _target_Id: str):
        self.createAt = _createAt
        self.startOn = _startOn
        self.target_Id = _target_Id
        self.assignation_Id = 0

    @staticmethod
    def getLastXTirages(assignation: str):
        # TODO Récupération des derniers tirages
        return ["Jean", "Paul"]

    @staticmethod
    def clearTirage(users: list, lastTirage: list):
        # TODO Supprimer les membres dispo au tirage et le membres déjà pick auparavant 
        return ["Jean", "Paul", "Maurice", "Alain", "Bob", "Thomas"]

    @staticmethod
    def pickOn(user: list):
        return random.choices(user)

    async def roll(self, date: datetime.date, target: Target):
        membersPick = {}

        # Pour la target
        listMembers = target.getAllMembers()

        # Comparer la liste des utilisateurs de ce role sur le serveur 
        # à la liste des utilisateurs dans la base de données
        if target.compare(listMembers):
            for name_assignation in self.listAssignations:
                
                    XlastTirage = self.getLastXTirages(name_assignation)
                    users = listMembers
                    user = self.pickOn(users)
                    while(user[0].name in membersPick.values()):
                        user = self.pickOn(users)
                    membersPick[name_assignation] = user[0].name
                    #membersPick.append([name_assignation, user[0].name])

            print(membersPick)
            _assignation = Assignation(1)
            _assignation.splitAssignations(membersPick)

            await self.message(membersPick, target, date)
    
    async def message(self, membersPick: dict, target: Target, date:datetime.date):
        embed = Embed(title=date, color=0xe80005, timestamp=datetime.datetime.today())
        
        for key, value in membersPick.items():
            embed.add_field(name=key, value=value, inline=False)

        await target.channel.send(content="<@&" + str(target.role.id) + ">",embed=embed)
