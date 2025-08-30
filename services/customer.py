# -*- coding: utf-8 -*-
import re
from typing import List
from domain.interfaces import CustomerServicePort, RepositoryPort, Customer, EmailServicePort

class CustomerService(CustomerServicePort):
    def __init__(self, repo: RepositoryPort, email: EmailServicePort):
        self.repo = repo
        self.email = email

    def _email_valido(self, email: str) -> bool:
        # validação minimamente decente
        return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))

    def add_customer(self, name: str, email: str, phone: str) -> int:
        if not self._email_valido(email):
            raise ValueError("E-mail inválido.")
        cid = self.repo.next_customer_id()
        c = Customer(id=cid, name=name.strip(), email=email.strip(), phone=phone.strip())
        self.repo.save_customer(c)
        # notifica com opt-in assumido para fins didáticos
        self.email.send(to=c.email, subject="Bem-vindo!", body=f"Olá {c.name}, seu cadastro foi criado!")
        return cid

    def list_customers(self) -> List[Customer]:
        return self.repo.list_customers()
