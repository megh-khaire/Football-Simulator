import random

import simulator.configs.manager as scm


class Manager:
    """
    A class to represent a football manager.
    """

    def __init__(self):
        """
        Initializes a Manager instance with a random name and formation.
        """
        self.name: str = self._get_random_name()
        self.formation: str = self._get_random_formation()

    def _get_random_name(self) -> str:
        """
        Selects a random name from the list of names in the configuration.

        Returns:
            str: A randomly chosen manager name.
        """
        return random.choice(scm.names)

    def _get_random_formation(self) -> str:
        """
        Selects a random formation from the list of formations in the configuration.

        Returns:
            str: A randomly chosen formation.
        """
        return random.choice(scm.formations)
