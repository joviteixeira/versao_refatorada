# versao_inicial — Sistema Loja (sem padrões)

> **ATENÇÃO:** Esta é a **versão propositalmente mal projetada** para a *Etapa 1 – Implementação Inicial (Sem Padrões)*.
Ela contém **anti-patterns** claros (God Object, Spaghetti Code, Lava Flow), acoplamento forte, ausência de interfaces,
validações repetidas, números mágicos, persistência frágil, etc. **Não** é um exemplo de boas práticas.

## Como executar
Requisitos: Python 3.10+

```bash
cd versao_inicial
python main.py
```

Um menu de terminal será exibido para cadastrar clientes, criar pedidos e listar dados.
Os registros são jogados em um CSV simples (`dados_loja.csv`) no mesmo diretório.

## O que observar (anti-patterns evidentes)
- **God Object**: a classe `SistemaLoja` concentra praticamente todas as responsabilidades.
- **Spaghetti Code**: menu e fluxo de interação com `input()` aninhado, validações pobres e repetidas.
- **Lava Flow**: funções e configs obsoletas que ficaram no código (ex.: `_algoritmo_precos_v1_obsoleto`, `OBSOLETE_CONFIG`).
- **Acoplamento forte**: uso direto de `FakeDatabase` e `EmailService` com parâmetros hardcoded.
- **Números mágicos**: `GLOBAL_DISCOUNT`, `TAXA`, `FRETE_FIXO` e regras de frete/tributos espalhadas.
- **Persistência frágil**: CSV improvisado sem esquema, sem tratamento de erro adequado.

## Próximos passos (para as próximas etapas)
- Diagnosticar formalmente os anti-patterns e violações SOLID.
- Definir interfaces e separar responsabilidades (camadas).
- Reestruturar com IoC/DI e/ou Service Locator.
- Escrever testes.
- Melhorar persistência, validações e logs.
