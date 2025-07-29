from typing import Any, Dict, List, Optional, Tuple, Union

from ._base import KumaRestAPIModule


class KumaRestAPIReports(KumaRestAPIModule):
    """
    Методы для работы с алертами
    """

    def __init__(self, base):
        super().__init__(base)

    def search(self, tenants_ids: List[str], **kwargs) -> Tuple[int, List | str]:
        """
        Searching reports info
        Args:
            tenants_ids (List[str]): List of tenant filter
            id (List[str]): Report UUID
            name (str): Case-insensetine name regex filter
            limit (int): Maximum number of entities to return
            offset (int): Number of entities to skip
            order (str): Columns for sorting ('-' is for DESC)
            column** (str): Returned columns of JSON (use several times)
        """
        params = {"tenantIDs": tenants_ids, **kwargs}
        return self._make_request("GET", "reports", params=params)
