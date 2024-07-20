import random
from typing import Dict, List, Optional

from simulator.configs.odds import odds, shot_outcome
from simulator.player import Player


class Event:
    def __init__(
        self, event: str, side: str, minute: int, player: Optional[Player] = None
    ):
        self.event: str = event
        self.side: str = side
        self.minute: int = minute
        self.player: Optional[Player] = player
        self.sides: Dict[str, str] = {}
        self.reverse: Dict[str, str] = {}

    def set_home_and_away_sides(self, home_side: str, away_side: str):
        self.sides = {home_side: "Home", away_side: "Away"}
        self.reverse = {home_side: away_side, away_side: home_side}

    def set_player_for_events(self, eventslist: List["Event"]) -> List["Event"]:
        """
        Assigns a player to each event in the events list.
        """
        position = random.choice(
            ["goalkeeper", "defenders", "midfielders", "attackers"]
        )
        players = list(eventslist[0].side.squad[position])
        player = random.choice(players)

        for event in eventslist:
            if event.event == "Saved":
                event.player = event.side.squad["goalkeeper"][0]
            else:
                event.player = player

        return eventslist

    def evaluate_event(self) -> List["Event"]:
        """
        Evaluates the current event and returns a list of resulting events.
        """
        if self.event == "Attempt":
            return self._evaluate_attempt()
        elif self.event == "Foul":
            return self._evaluate_foul()
        else:
            return self._evaluate_generic_event()

    def _evaluate_attempt(self) -> List["Event"]:
        events = [Event(self.event, self.side, self.minute)]
        attodds = [shot_outcome[oc]["Probability"] for oc in shot_outcome]
        att = random.choices(list(shot_outcome.keys()), attodds, k=1)[0]
        events.append(Event(att, self.side, self.minute))

        if att == "On target":
            goalodds = list(shot_outcome["On target"]["is_goal"].values())
            goal = random.choices(["Saved", "Goal"], goalodds, k=1)[0]
            if goal == "Saved":
                self.side = self.reverse[self.side]
            events.append(Event(goal, self.side, self.minute))

        return self.set_player_for_events(events)

    def _evaluate_foul(self) -> List["Event"]:
        events = [
            Event("Foul", self.side, self.minute),
            Event("Free kick won", self.reverse[self.side], self.minute),
        ]

        yellow_card_prob = (
            odds[self.minute][self.sides[self.side]]["Events"]["Yellow card"]
            / odds[self.minute][self.sides[self.side]]["Events"]["Foul"]
        )
        red_card_prob = (
            odds[self.minute][self.sides[self.side]]["Events"]["Red card"]
            / odds[self.minute][self.sides[self.side]]["Events"]["Foul"]
        )
        no_card_prob = 1 - (yellow_card_prob + red_card_prob)

        card = random.choices(
            ["Yellow card", "Red card", "No card"],
            [yellow_card_prob, red_card_prob, no_card_prob],
            k=1,
        )[0]

        if card != "No card":
            events.append(Event(card, self.side, self.minute))

        return self.set_player_for_events(events)

    def _evaluate_generic_event(self) -> List["Event"]:
        events = [Event(self.event, self.side, self.minute)]
        return self.set_player_for_events(events)

    def show_event(self):
        """
        Displays the event details.
        """
        print(
            f"{self.minute}' {self.side.name} {self.event} {self.player.name if self.player else ''}"
        )
