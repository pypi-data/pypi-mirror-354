# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

"""
It is the module where the AbstractTransaction will handle
web transactions in an automated browser.
"""
from logging import getLogger, Logger
from typing import Any, NoReturn, Union, Dict
from guara.utils import is_dry_run

LOGGER: Logger = getLogger("guara")


class AbstractTransaction:
    """
    It will handle web transactions in an automated browser.
    """

    def __init__(self, driver: Any):
        """
        Initializing the transaction which will allow it to interact
        with the driver.

        Args:
            driver: (Any): It is the driver that controls the user-interface.
        """
        self._driver: Any = driver

    @property
    def __name__(self) -> property:
        """
        The name of the transaction

        Returns:
            (str) The name of the transaction being implemented.
        """
        return self.__class__.__name__

    def do(self, **kwargs: Dict[str, Any]) -> Union[Any, NoReturn]:
        """
        It performs a specific transaction

        Args:
            kwargs: (dict): It contains all the necessary data and parameters for the transaction.

        Returns:
            (Any | NoReturn)

        Raises:
            NotImplementedError: The method is not implemented in the subclass.
        """
        raise NotImplementedError

    def act(self, **kwargs: Dict[str, Any]) -> Union[Any, NoReturn]:
        if is_dry_run():
            return
        return self.do(**kwargs)

    def undo(self):
        """
        Reverts the actions performed by the method `do`

        Returns:
            (NoReturn)
        """
        LOGGER.info(" Nothing to revert")

    def revert_action(self) -> NoReturn:
        if is_dry_run():
            return
        return self.undo()
