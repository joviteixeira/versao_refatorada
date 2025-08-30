# -*- coding: utf-8 -*-
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol, Iterable, List, Dict, Tuple
from dataclasses import dataclass

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


class EmailServicePort(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> None: ...


class RepositoryPort(ABC):
    """Persistência simplificada (apenas o necessário para a atividade)."""
    # Customers
    @abstractmethod
    def next_customer_id(self) -> int: ...
    @abstractmethod
    def save_customer(self, c: Customer) -> None: ...
    @abstractmethod
    def list_customers(self) -> List[Customer]: ...
    @abstractmethod
    def get_customer(self, cid: int) -> Customer | None: ...

    # Orders
    @abstractmethod
    def next_order_id(self) -> int: ...
    @abstractmethod
    def save_order(self, o: Order) -> None: ...
    @abstractmethod
    def list_orders(self) -> List[Order]: ...


class PricingServicePort(ABC):
    @abstractmethod
    def compute_total(self, items: List[OrderItem]) -> float: ...


class CustomerServicePort(ABC):
    @abstractmethod
    def add_customer(self, name: str, email: str, phone: str) -> int: ...
    @abstractmethod
    def list_customers(self) -> List[Customer]: ...


class OrderServicePort(ABC):
    @abstractmethod
    def create_order(self, customer_id: int, items: List[OrderItem]) -> int: ...
    @abstractmethod
    def list_orders(self) -> List[Order]: ...
