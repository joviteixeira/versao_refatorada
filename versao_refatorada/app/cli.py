# -*- coding: utf-8 -*-
import argparse
from typing import List
from app.service_locator import locator, REPO, EMAIL, PRICING, CUSTOMERS, ORDERS
from app import settings
from infrastructure.csv_repository import CsvRepository
from infrastructure.console_email import ConsoleEmailService
from services.pricing import PricingService
from services.customer import CustomerService
from services.order import OrderService
from domain.interfaces import OrderItem

def bootstrap():
    # Registrar implementações concretas no Service Locator
    locator.register_singleton(REPO, CsvRepository(settings.DATA_DIR))
    locator.register_singleton(EMAIL, ConsoleEmailService(settings.SMTP_HOST, settings.SMTP_PORT, settings.SMTP_FROM))
    locator.register_factory(PRICING, lambda: PricingService())

    # Services de aplicação
    repo = locator.resolve(REPO)
    email = locator.resolve(EMAIL)
    pricing = locator.resolve(PRICING)

    locator.register_singleton(CUSTOMERS, CustomerService(repo, email))
    locator.register_singleton(ORDERS, OrderService(repo, pricing))

def parse_item(s: str) -> OrderItem:
    # formato: nome:qtd:preco
    try:
        nome, qtd, preco = s.split(":")
        return OrderItem(name=nome, quantity=float(qtd), price=float(preco))
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Item inválido '{s}'. Use nome:qtd:preco") from e

def main(argv: List[str] | None = None) -> int:
    bootstrap()

    parser = argparse.ArgumentParser(prog="loja", description="CLI — Etapa 3 com Service Locator")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Clientes
    p_cli = sub.add_parser("clientes", help="Operações com clientes")
    sub_cli = p_cli.add_subparsers(dest="op", required=True)

    p_cli_add = sub_cli.add_parser("add", help="Adicionar cliente")
    p_cli_add.add_argument("--nome", required=True)
    p_cli_add.add_argument("--email", required=True)
    p_cli_add.add_argument("--telefone", required=True)

    p_cli_list = sub_cli.add_parser("list", help="Listar clientes")

    # Pedidos
    p_ped = sub.add_parser("pedidos", help="Operações com pedidos")
    sub_ped = p_ped.add_subparsers(dest="op", required=True)

    p_ped_add = sub_ped.add_parser("add", help="Criar pedido")
    p_ped_add.add_argument("--cliente-id", type=int, required=True)
    p_ped_add.add_argument("--item", action="append", required=True, type=parse_item,
                           help="Item no formato nome:qtd:preco (pode repetir)")

    p_ped_list = sub_ped.add_parser("list", help="Listar pedidos")

    args = parser.parse_args(argv)

    if args.cmd == "clientes":
        svc = locator.resolve(CUSTOMERS)
        if args.op == "add":
            cid = svc.add_customer(args.nome, args.email, args.telefone)
            print(f"Cliente #{cid} criado.")
        elif args.op == "list":
            for c in svc.list_customers():
                print(f"{c.id:03d} | {c.name} | {c.email} | {c.phone}")

    elif args.cmd == "pedidos":
        svc = locator.resolve(ORDERS)
        if args.op == "add":
            oid = svc.create_order(args.cliente_id, args.item)
            print(f"Pedido #{oid} criado.")
        elif args.op == "list":
            for o in svc.list_orders():
                itens = ", ".join(f"{i.name} x{i.quantity} @ {i.price:.2f}" for i in o.items)
                print(f"{o.id:03d} | cliente={o.customer_id} | total=R$ {o.total:.2f} | {itens} | {o.status}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
