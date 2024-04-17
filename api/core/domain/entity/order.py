import datetime
from dataclasses import dataclass


@dataclass
class Order:
    _id: int
    _datetime_of_order: datetime.datetime
