"""
FortiAnalyzer Class
"""

import logging
from typing import Any

from .fortimanager import FortiManager

log = logging.getLogger("fotoobo")


class FortiAnalyzer(FortiManager):
    """
    Represents one FortiAnalyzer (digital twin)

    This class is inherited from FortiManager. Only the type of the object differs.
    """

    def __init__(self, hostname: str, username: str, password: str, **kwargs: Any) -> None:
        """
        Set some initial parameters.

        Args:
            hostname: The hostname of the FortiGate to connect to
            username: Username
            password: Password
            **kwargs: See Fortinet class for available arguments
        """
        super().__init__(hostname, username, password, **kwargs)
        self.type = "fortianalyzer"

    def get_version(self) -> str:
        """
        Get FortiAnalyzer version

        Returns:
            FortiAnalyzer version
        """
        faz_version = super().get_version()
        return faz_version
