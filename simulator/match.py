import copy
import random
from typing import Dict, List, Tuple

from simulator.configs.odds import odds
from simulator.event import Event
from simulator.team import Team


class Match:
    reverse = {"Home": "Away", "Away": "Home"}
    eventkeys = list(odds[0]["Home"]["Events"].keys())
    foulkeys = ["Free kick won", "Yellow card", "Second yellow card", "Red card"]

    def __init__(self, home_side: Team, away_side: Team):
        self.odds = copy.deepcopy(odds)
        self.home_side = home_side
        self.away_side = away_side
        self.sides = {home_side: "Home", away_side: "Away"}
        self.reverse = {home_side: away_side, away_side: home_side}
        self.matchevents: List[Event] = []
        self.home_stats = self._initialize_stats()
        self.away_stats = self._initialize_stats()
        self.stats = {home_side: self.home_stats, away_side: self.away_stats}
        self.home_players = home_side.players
        self.away_players = away_side.players
        self._set_odds()
        self._set_events()

    def _initialize_stats(self) -> Dict[str, int]:
        """
        Initializes the match statistics.
        """
        tlist = copy.deepcopy(Match.eventkeys)
        tlist.extend(
            ["On target", "Saved", "Off target", "Blocked", "Hit the bar", "Goal"]
        )
        return dict(zip(tlist, [0] * len(tlist)))

    def _set_odds(self):
        """
        Adjusts the odds based on team defense and midfield ratings.
        """
        hdf = (self.home_side.defence**2 * self.home_side.midfield) / (
            self.away_side.attack**2 * self.away_side.midfield
        )
        adf = (self.away_side.defence**2 * self.away_side.midfield) / (
            self.home_side.attack**2 * self.home_side.midfield
        )
        for minute in range(100):
            self.odds[minute]["Home"]["Events"]["Attempt"] /= adf**2.33
            self.odds[minute]["Away"]["Events"]["Attempt"] /= hdf**2.33

    def add_event(self, event: Event):
        """
        Adds an evaluated event to the match events.
        """
        for e in event.evaluate_event():
            if e.event == "Substitution":
                if self.stats[e.side][e.event] < 3:
                    self._track_event(e)
            else:
                self._track_event(e)
            e.show_event()
            self.matchevents.append(e)

    def _set_events(self):
        """
        Sets events for the match based on odds and probabilities.
        """
        for minute in range(100):
            for _ in range(135):
                if random.uniform(0, 1) < self.odds[minute]["Event"]:
                    plist = [
                        self.odds[minute]["Home"]["Probability"],
                        self.odds[minute]["Away"]["Probability"],
                    ]
                    side = random.choices([self.home_side, self.away_side], plist, k=1)[
                        0
                    ]
                    event = random.choices(
                        Match.eventkeys,
                        list(self.odds[minute][self.sides[side]]["Events"].values()),
                        k=1,
                    )[0]
                    if event not in Match.foulkeys:
                        e = Event(event, side, minute)
                        e.set_home_and_away_sides(self.home_side, self.away_side)
                        self.add_event(e)

    def _track_event(self, event: Event):
        """
        Tracks the event by updating the statistics.
        """
        if event.side == self.home_side:
            self.home_stats[event.event] += 1
        else:
            self.away_stats[event.event] += 1
        self.stats = {self.home_side: self.home_stats, self.away_side: self.away_stats}

    def evaluate_match_result(self) -> Tuple[str, "Team", "Team"]:
        """
        Evaluates the result of the match.

        Returns:
            Tuple[str, Team, Team]: The match result and the teams involved.
        """
        home_goals = self.stats[self.home_side]["Goal"]
        away_goals = self.stats[self.away_side]["Goal"]
        if home_goals == away_goals:
            return ("Draw", self.home_side, self.away_side)
        elif home_goals > away_goals:
            return ("Win", self.home_side, self.away_side)
        else:
            return ("Win", self.away_side, self.home_side)

    def show_match_result(self):
        """
        Displays the result of the match.
        """
        home_goals = self.stats[self.home_side]["Goal"]
        away_goals = self.stats[self.away_side]["Goal"]
        if home_goals > away_goals:
            print(f"{self.home_side.name} won the match")
            print(f"Score {home_goals} - {away_goals}")
        elif away_goals > home_goals:
            print(f"{self.away_side.name} won the match")
            print(f"Score {home_goals} - {away_goals}")
        else:
            print(
                f"The match between {self.home_side.name} and {self.away_side.name} was a Draw"
            )
            print(f"Score {home_goals} - {away_goals}")
