# -*- coding: utf-8 -*-
from typing import List
from domain.interfaces import PricingServicePort, OrderItem
from app import settings

class PricingService(PricingServicePort):
    def compute_total(self, items: List[OrderItem]) -> float:
        subtotal = sum(max(0.0, i.quantity) * max(0.0, i.price) for i in items)

        total = subtotal * (1 - settings.DESCONTO_PADRAO)
        total *= (1 + settings.TAXA_IMPOSTO)

        # frete
        if subtotal > settings.LIMIAR_FRETE_GRATIS:
            frete = 0.0
        elif subtotal > settings.LIMIAR_MEIO_FRETE:
            frete = settings.FRETE_FIXO / 2.0
        else:
            frete = settings.FRETE_FIXO if subtotal > 0 else 0.0

        return round(total + frete, 2)
