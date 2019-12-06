import random


class Team:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating


class Group:
    def __init__(self, name):
        self.name = name
        self.teams = []

        for i in range(4):
            team = Team(f"{self.name}_{i}", random.randint(60, 100)) # Teams aanmaken (Normaal worden gegevens opgehaald via database)
            self.teams.append([team, 0, 0, 0, 0, 0, 0, 0, 0]) # Stand van de competitie voordat er wedstrijden zijn gespeeld

    def standing(self):
        self.teams.sort(key=lambda x: (x[8], x[7], x[5]), reverse=True) # De teams sorteren op basis van punten, doelsaldo en aantal gescoorde doelpunten

        print(f"\nGroup {self.name}")
        print("Team           MP   W   D   L  GF  GA  GD Pts")
        for i, team in enumerate(self.teams):
            statistics = " ".join(map(lambda x: f"{x:3}", team[1:]))
            print(f"[{i + 1}] {team[0].name} ({team[0].rating:3}) {statistics}")

    def simulate(self): # De simulatie van wedstrijden in de competitie, elk team speelt 1 keer tegen elkaar. Er zijn totaal 3 rondes.
        for i, team_A in enumerate(self.teams):
            for j, team_B in enumerate(self.teams[i + 1:]):
                score = self.play(team_A[0], team_B[0])
                j = j + i + 1

                self.teams[i][1] = self.teams[i][1] + 1
                self.teams[i][5] = self.teams[i][5] + score[0]
                self.teams[i][6] = self.teams[i][6] + score[1]
                self.teams[i][7] = self.teams[i][5] - self.teams[i][6]

                self.teams[j][1] = self.teams[j][1] + 1
                self.teams[j][5] = self.teams[j][5] + score[1]
                self.teams[j][6] = self.teams[j][6] + score[0]
                self.teams[j][7] = self.teams[j][5] - self.teams[j][6]

                if score[0] > score[1]: # Stand van de competitie updaten als team A wint
                    self.teams[i][2] = self.teams[i][2] + 1
                    self.teams[j][4] = self.teams[j][4] + 1
                    self.teams[i][8] = self.teams[i][8] + 3
                elif score[0] < score[1]: # Stand van de competitie updaten als team B wint
                    self.teams[i][4] = self.teams[i][4] + 1
                    self.teams[j][2] = self.teams[j][2] + 1
                    self.teams[j][8] = self.teams[j][8] + 3
                else:                   # Stand van de competitie updaten als TEAM A en TEAM B gelijkspelen
                    self.teams[i][3] = self.teams[i][3] + 1
                    self.teams[j][3] = self.teams[j][3] + 1
                    self.teams[i][8] = self.teams[i][8] + 1
                    self.teams[j][8] = self.teams[j][8] + 1

    def play(self, A, B, show=True):
        AGM = 3.08 # Gemiddelde gescoorde doelpunten per wedstrijd (Deze gegeven komt uit de eredivisie)
        GPM = AGM / 90 # Doelpunten per minuut
        AB_r = A.rating / (A.rating + B.rating) # Winpercentage, kan gewijzigd worden.

        scoreboard = [0, 0]

        if show:
            print(f"\n{A.name} VS {B.name}")
            print("-"*18)

        for i in range(1, 91): # Hier wordt per minuut gekeken of er een doelpunt valt of niet, op basis van de Gemiddelde doelpunten per wedstrijd en het winpercentage van de team.
            if random.uniform(0, 1) <= GPM: 
                if random.uniform(0, 1) <= AB_r:
                    scoreboard[0] = scoreboard[0] + 1

                    if show:
                        print(f"[{i:02}] {A.name} Scored!!!")
                else:
                    scoreboard[1] = scoreboard[1] + 1

                    if show:
                        print(f"[{i:02}] {B.name} Scored!!!")

        if show:
            print(f"\n{A.name}: {scoreboard[0]}\n{B.name}: {scoreboard[1]}")
            print("~"*18)

        return scoreboard


class Tournament: # Competitie starten met uitslagen en de uiteindelijke stand
    def __init__(self):
        self.groups = []
        self.names = ["A", "B", "C", "D"]

        for i in range(4):
            self.groups.append(Group(self.names[i]))

    def standings(self):
        for group in self.groups:
            group.standing()

    def simulate(self):
        for group in self.groups:
            group.simulate()


tournament = Tournament()
tournament.simulate()
tournament.standings()
