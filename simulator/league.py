from typing import Dict, List, Tuple, Union

import pandas as pd
from tabulate import tabulate

import simulator.configs.league as scl
from simulator.match import Match
from simulator.player import Player
from simulator.team import Team


class League:
    LEAGUE_TABLE_ATTRIBUTES = [
        "Club",
        "Matches Played",
        "Wins",
        "Draws",
        "Losses",
        "Points",
        "GF",
        "GA",
        "GD",
    ]

    def __init__(self, option: int):
        self.week: int = 0
        self.name: str = scl.leagues[scl.countries[option]]["name"]
        self.players: Dict[str, Player] = {}
        self.teams: Dict[str, Team] = {}
        self.team_names: List[str] = scl.leagues[scl.countries[option]]["teams"]
        self.set_teams()
        self.set_players()
        self.schedule: List[List[Tuple[Union[str, None], Union[str, None]]]] = (
            self.create_balanced_round_robin(self.team_names)
        )
        self.standings: pd.DataFrame = self.init_league_table()

    def set_teams(self):
        """
        Initializes teams from the list of team names.
        """
        for name in self.team_names:
            self.teams[name] = Team(name)

    def set_players(self):
        """
        Updates the players dictionary with players from all teams.
        """
        for team in self.teams.values():
            self.players.update(team.players)

    def create_balanced_round_robin(
        self, teams: List[str]
    ) -> List[List[Tuple[Union[str, None], Union[str, None]]]]:
        """
        Creates a balanced round-robin schedule for the teams.
        """
        schedule = []
        if len(teams) % 2 == 1:
            teams.append(None)  # Add a dummy team for balancing

        team_count = len(teams)
        mid = team_count // 2

        for _ in range(team_count - 1):
            first_half = teams[:mid]
            second_half = teams[mid:]
            second_half.reverse()

            round_schedule = [
                (t1, t2) for t1, t2 in zip(first_half, second_half) if t1 and t2
            ]
            schedule.append(round_schedule)

            # Add the reverse fixtures
            reverse_round_schedule = [(t2, t1) for t1, t2 in round_schedule]
            schedule.append(reverse_round_schedule)

            teams.insert(1, teams.pop())  # Rotate the list

        return schedule

    def init_league_table(self) -> pd.DataFrame:
        """
        Initializes the league table DataFrame.
        """
        table = pd.DataFrame(columns=League.LEAGUE_TABLE_ATTRIBUTES)
        for team in self.team_names:
            row = pd.DataFrame(
                [[team, 0, 0, 0, 0, 0, 0, 0, 0]],
                columns=League.LEAGUE_TABLE_ATTRIBUTES,
            )
            table = pd.concat([table, row], ignore_index=True)
        table.index = table.index + 1
        return table

    def show_league_table(self):
        """
        Displays the league table using tabulate.
        """
        print(
            tabulate(self.standings, headers=self.standings.columns, tablefmt="github")
        )

    def update_league_table(self, match: Match):
        """
        Updates the league table based on the match result.
        """
        result, winner, loser = match.evaluate_match_result()
        table = self.standings
        num_winner_goals = match.stats[winner]["Goal"]
        num_loser_goals = match.stats[loser]["Goal"]

        if result == "Draw":
            self._update_team_stats(
                table, winner, draws=1, gf=num_winner_goals, ga=num_loser_goals
            )
            self._update_team_stats(
                table, loser, draws=1, gf=num_winner_goals, ga=num_loser_goals
            )
        else:
            self._update_team_stats(
                table, winner, wins=1, gf=num_winner_goals, ga=num_loser_goals, points=3
            )
            self._update_team_stats(
                table, loser, losses=1, gf=num_loser_goals, ga=num_winner_goals
            )

        table.sort_values(by="Points", inplace=True, ascending=False)
        table.reset_index(drop=True, inplace=True)

    def _update_team_stats(
        self,
        table: pd.DataFrame,
        team: Team,
        matches_played: int = 1,
        wins: int = 0,
        draws: int = 0,
        losses: int = 0,
        points: int = 0,
        gf: int = 0,
        ga: int = 0,
    ):
        """
        Updates the statistics of a specific team in the league table.
        """
        table.loc[
            table["Club"] == team.name,
            ["Matches Played", "Wins", "Draws", "Losses", "Points", "GF", "GA"],
        ] += [matches_played, wins, draws, losses, points, gf, ga]
        table.loc[table["Club"] == team.name, "GD"] = (
            table.loc[table["Club"] == team.name, "GF"]
            - table.loc[table["Club"] == team.name, "GA"]
        )

    def simulate_match(self, home_team_name: str, away_team_name: str):
        """
        Simulates a match between two teams and updates the league table.
        """
        home_team = self.teams[home_team_name]
        away_team = self.teams[away_team_name]
        match = Match(home_team, away_team)
        match.show_match_result()
        self.update_league_table(match)

    def simulate_week(self):
        """
        Simulates all matches for the current week.
        """
        for home_team, away_team in self.schedule[self.week]:
            self.simulate_match(home_team, away_team)
        self.week += 1

    def simulate_league(self):
        """
        Simulates the entire league season.
        """
        while self.week < len(self.schedule):
            self.simulate_week()
            self.show_league_table()
