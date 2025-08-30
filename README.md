# Etapa 3 — Reestruturação com IoC (Service Locator)

Esta versão reestrutura o sistema usando **Inversão de Controle** por meio do **Service Locator**.
A aplicação deixa de depender diretamente de implementações concretas e passa a obtê-las a partir
de um **registro central de serviços**.

## Objetivos cumpridos
- Separação por **camadas** (domain, services, infrastructure, app).
- Definição de **portas/contratos** (ABCs) para serviços de e-mail, precificação e persistência.
- **Service Locator** (`app/service_locator.py`) para registrar e resolver dependências.
- Remoção de números mágicos e globais; uso de `app/settings.py`.
- Persistência simples via `infrastructure/csv_repository.py` (CSV + JSON embutido para itens).
- CLI enxuta (`app/cli.py`) com `argparse`.

## Como executar
Requisitos: Python 3.10+

```bash
cd etapa3_service_locator
python -m app.cli --help
```

Fluxo rápido:
```bash
# Cadastrar cliente
python -m app.cli clientes add --nome "Maria" --email "maria@example.com" --telefone "71999990000"

# Listar clientes
python -m app.cli clientes list

# Criar pedido (ex.: 2 itens; use formato nome:qtd:preco)
python -m app.cli pedidos add --cliente-id 1 --item "Teclado:1:120" --item "Mouse:2:60"

# Listar pedidos
python -m app.cli pedidos list
```

Os dados são armazenados em `./data/clientes.csv` e `./data/pedidos.csv`.

## Estrutura
```
app/
  cli.py              # Interface de linha de comando
  service_locator.py  # Registro de serviços (IoC - Service Locator)
  settings.py         # Parâmetros (frete, impostos, descontos)
domain/
  interfaces.py       # Portas (ABCs) e tipos
  models.py           # Entidades (dataclasses)
infrastructure/
  csv_repository.py   # Implementação de persistência
  console_email.py    # Implementação de envio de e-mail (console)
services/
  pricing.py          # Regras de precificação
  customer.py         # Caso de uso: clientes
  order.py            # Caso de uso: pedidos
```

## Observações
- O **Service Locator** é uma abordagem de IoC aceitável para fins didáticos, mas em projetos reais prefira
  **injeção de dependências explícita** para facilitar testes e manutenibilidade.
