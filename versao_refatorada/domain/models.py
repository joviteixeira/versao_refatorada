# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List

@dataclass
class Customer:
    id: int | None
    name: str
    email: str
    phone: str

@dataclass
class OrderItem:
    name: str
    quantity: float
    price: float

@dataclass
class Order:
    id: int | None
    customer_id: int
    items: List[OrderItem]
    total: float
    status: str = "NOVO"
