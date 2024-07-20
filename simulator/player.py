from simulator.configs.player import Position, TeamStatus


class Player:
    GOALKEEPER_ATTRIBUTES = [
        "gk_diving",
        "gk_handling",
        "gk_kicking",
        "gk_reflexes",
        "gk_speed",
        "gk_positioning",
    ]

    def __init__(self, df_player):
        stats = df_player.to_dict()
        self.name = stats["short_name"]
        self.nationality = stats["nationality"]
        self.overall = stats["overall"]
        self.pace = stats["pace"]
        self.shooting = stats["shooting"]
        self.passing = stats["passing"]
        self.dribbling = stats["dribbling"]
        self.defending = stats["defending"]
        self.physic = stats["physic"]
        self.keeping = 0
        self.team_status = TeamStatus.RESERVE
        self.position = self._determine_position(stats["player_positions"])
        self._set_goalkeeper_rating(stats)

    def _determine_position(self, player_positions):
        main_position = player_positions.split(",")[0]
        if "B" in main_position:
            return Position.DEFENDER
        elif "M" in main_position:
            return Position.MIDFIELDER
        elif "S" in main_position or "F" in main_position or "W" in main_position:
            return Position.ATTACKER
        else:
            return Position.GOALKEEPER

    def _set_goalkeeper_rating(self, stats):
        if self.position == Position.GOALKEEPER:
            gk_rating = sum(
                stats[attribute] for attribute in Player.GOALKEEPER_ATTRIBUTES
            )
            self.keeping = gk_rating // len(Player.GOALKEEPER_ATTRIBUTES)

    @property
    def is_attacker(self):
        return self.position == Position.ATTACKER

    @property
    def is_midfielder(self):
        return self.position == Position.MIDFIELDER

    @property
    def is_defender(self):
        return self.position == Position.DEFENDER

    @property
    def is_goalkeeper(self):
        return self.position == Position.GOALKEEPER

    @property
    def is_starter(self):
        return self.team_status == TeamStatus.STARTER

    def set_as_starter(self):
        self.team_status = TeamStatus.STARTER
