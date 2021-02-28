import random, datetime
from .assignation import Assignation

class Event():

    listAssignations = ["Animateur", "Secretaire", "Scribe", "Gestionnaire"]

    def __init__(self, _createAt: datetime.date, _startOn: String, _target_Id: String):
        self.createAt = _createAt
        self.startOn = _startOn
        self.target_Id = _target_Id
        self.assignation_Id = 0

    @staticmethod
    def getLastXTirages(assignation: String):
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

        membersPick = []

        # Pour la target
        listMembers = target.getAllMembers()

        # Comparer la liste des utilisateurs de ce role sur le serveur 
        # à la liste des utilisateurs dans la base de données
        if target.compare(listMembers):
            for name_assignation in self.listAssignations:
                
                    XlastTirage = self.gettLastXTirages(name_assignation)
                    users = self.clearTirage(listMembers, XlastTirage)
                    user = self.pickOn(users)
                    membersPick.append([name_assignation, user])

            print(membersPick)
            _assignation = Assignation(1)
            _assignation.splitAssignations(membersPick)

            await self.message(membersPick, target, date)
    
    async def message(self, membersPick: list, target: Target, date:datetime.date):
        embed = Embed(title=date, color=0xe80005, timestamp=datetime.datetime.today())
        
        for member in membersPick:
            embed.add_field(name=member[0], value=member[1], inline=False)

        await target.channel.send(content="<@&" + str(target.role.id) + ">",embed=embed)