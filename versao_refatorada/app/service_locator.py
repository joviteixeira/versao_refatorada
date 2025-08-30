# -*- coding: utf-8 -*-
"""
Service Locator — Registro central de dependências.
Permite registrar fábricas (callables) e resolver instâncias sob uma "chave".
"""

from typing import Callable, Dict, Any

class ServiceLocator:
    def __init__(self):
        self._factories: Dict[str, Callable[[], Any]] = {}
        self._singletons: Dict[str, Any] = {}

    def register_factory(self, key: str, factory: Callable[[], Any]) -> None:
        self._factories[key] = factory

    def register_singleton(self, key: str, instance: Any) -> None:
        self._singletons[key] = instance

    def resolve(self, key: str) -> Any:
        if key in self._singletons:
            return self._singletons[key]
        if key in self._factories:
            return self._factories[key]()
        raise KeyError(f"Serviço não encontrado: {key!r}")


# Chaves padrão usadas pela aplicação
REPO = "repository"
EMAIL = "email_service"
PRICING = "pricing_service"
CUSTOMERS = "customer_service"
ORDERS = "order_service"

# Instância global do Registry (poderia ser passado por composição onde preferir)
locator = ServiceLocator()
