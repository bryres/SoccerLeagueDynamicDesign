class Team(object):

    def __init__(self, id, name, league_id, coach_id):
        self.id = id
        self.name = name
        self.league_id = league_id
        self.coach_id = coach_id

    def __str__(self):
        return "<%s: %s/>" % (self.id, self.name)

