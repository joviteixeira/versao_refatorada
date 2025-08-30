# -*- coding: utf-8 -*-
from typing import List
from domain.interfaces import OrderServicePort, RepositoryPort, PricingServicePort, OrderItem, Order

class OrderService(OrderServicePort):
    def __init__(self, repo: RepositoryPort, pricing: PricingServicePort):
        self.repo = repo
        self.pricing = pricing

    def create_order(self, customer_id: int, items: List[OrderItem]) -> int:
        if not self.repo.get_customer(customer_id):
            raise ValueError(f"Cliente {customer_id} não existe.")
        if not items:
            raise ValueError("Pedido sem itens.")
        total = self.pricing.compute_total(items)
        oid = self.repo.next_order_id()
        o = Order(id=oid, customer_id=customer_id, items=items, total=total, status="NOVO")
        self.repo.save_order(o)
        return oid

    def list_orders(self) -> List[Order]:
        return self.repo.list_orders()
