from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime

class BaseHandler(ABC):
    @abstractmethod
    def fetch_data(self, query: str = None, start_date: datetime = None, end_date: datetime = None, working_dir: str = None, **args) -> Dict[str, Any]:
        """
        Handle the data center operation.
        This method should be overridden by subclasses.
        """
        pass