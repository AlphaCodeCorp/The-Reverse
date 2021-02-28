import random

class Event():

    def __init__():
        self.createAt
        self.startOn
        self.target_Id
        self.assignation
        self.user_Id

    def getLastXTirages(self):
        # TODO Récupération des derniers tirages
        return ["Jean", "Paul"]

    def clearTirage(self, users: list, lastTirage: list):
        # TODO Supprimer les membres dispo au tirage et le membres déjà pick auparavant 
        return ["Jean", "Paul", "Maurice", "Alain", "Bob", "Thomas"]

    def roll(self, user: list):
        return random.choices(user)

    async def roll(self, date: datetime.date, target: Target):
        print("--------START------")
        print(self.listTargets)
        print("--------------------")
        print(self.listAssignations)
        print("---------END--------")

        membersPick = []

        # Pour la target
        listMembers = target.getAllMembers()

        # Comparer la liste des utilisateurs de ce role sur le serveur 
        # à la liste des utilisateurs dans la base de données
        if target.compare(listMembers):
            for assignation in self.listAssignations:
                if assignation.target == target:

                    XlastTirage = assignation.getLastXTirages()
                    users = assignation.clearTirage(listMembers, XlastTirage)
                    user = assignation.roll(users)
                    membersPick.append([assignation.name, user])

            print(membersPick)
            await self.message(membersPick, target, date)
    
    async def message(self, membersPick: list, target: Target, date:datetime.date):
        embed = Embed(title=date, color=0xe80005, timestamp=datetime.datetime.today())
        
        for member in membersPick:
            embed.add_field(name=member[0], value=member[1], inline=False)

        await target.channel.send(content="<@&" + str(target.role.id) + ">",embed=embed)