# -*- coding: utf-8 -*-
import os, csv, json
from typing import List
from domain.interfaces import RepositoryPort, Customer, Order, OrderItem

class CsvRepository(RepositoryPort):
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.customers_csv = os.path.join(self.data_dir, "clientes.csv")
        self.orders_csv = os.path.join(self.data_dir, "pedidos.csv")
        # cria arquivos / cabeçalhos se necessário
        if not os.path.exists(self.customers_csv):
            with open(self.customers_csv, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f, delimiter=";")
                w.writerow(["id", "name", "email", "phone"])
        if not os.path.exists(self.orders_csv):
            with open(self.orders_csv, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f, delimiter=";")
                w.writerow(["id", "customer_id", "items_json", "total", "status"])

    # ---- Customers ----
    def _read_all_customers(self) -> List[Customer]:
        out: List[Customer] = []
        with open(self.customers_csv, "r", newline="", encoding="utf-8") as f:
            r = csv.DictReader(f, delimiter=";")
            for row in r:
                out.append(Customer(
                    id=int(row["id"]),
                    name=row["name"],
                    email=row["email"],
                    phone=row["phone"]
                ))
        return out

    def next_customer_id(self) -> int:
        items = self._read_all_customers()
        return (max((c.id or 0 for c in items), default=0) + 1)

    def save_customer(self, c: Customer) -> None:
        # append sempre (não edita; simples para a atividade)
        with open(self.customers_csv, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow([c.id, c.name, c.email, c.phone])

    def list_customers(self) -> List[Customer]:
        return self._read_all_customers()

    def get_customer(self, cid: int) -> Customer | None:
        for c in self._read_all_customers():
            if c.id == cid:
                return c
        return None

    # ---- Orders ----
    def _read_all_orders(self) -> List[Order]:
        out: List[Order] = []
        with open(self.orders_csv, "r", newline="", encoding="utf-8") as f:
            r = csv.DictReader(f, delimiter=";")
            for row in r:
                items = [OrderItem(**d) for d in json.loads(row["items_json"])]
                out.append(Order(
                    id=int(row["id"]),
                    customer_id=int(row["customer_id"]),
                    items=items,
                    total=float(row["total"]),
                    status=row["status"]
                ))
        return out

    def next_order_id(self) -> int:
        items = self._read_all_orders()
        return (max((o.id or 0 for o in items), default=0) + 1)

    def save_order(self, o: Order) -> None:
        with open(self.orders_csv, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow([
                o.id,
                o.customer_id,
                json.dumps([i.__dict__ for i in o.items], ensure_ascii=False),
                f"{o.total:.2f}",
                o.status
            ])

    def list_orders(self) -> List[Order]:
        return self._read_all_orders()
