# -*- coding: utf-8 -*-
from domain.interfaces import EmailServicePort

class ConsoleEmailService(EmailServicePort):
    def __init__(self, host: str, port: int, sender: str):
        self.host = host
        self.port = port
        self.sender = sender

    def send(self, to: str, subject: str, body: str) -> None:
        print(f"[EMAIL] {self.host}:{self.port} from={self.sender} to={to}")
        print(f"Assunto: {subject}")
        print(body)
        print("-"*60)
