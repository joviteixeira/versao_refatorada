# -*- coding: utf-8 -*-
"""
VERSÃO INICIAL (SEM PADRÕES) — PROPOSITALMENTE MAL PROJETADA
-----------------------------------------------------------
Este arquivo concentra "tudo": regras, persistência, "envio de e-mail",
menu CLI, validações, cálculos e logs. Foi feito para evidenciar
anti‑patterns (God Object, Spaghetti Code, Lava Flow, alto acoplamento).
"""

# "Configurações globais" (mudadas em tempo de execução... por quê?)
GLOBAL_DISCOUNT = 0.05   # desconto padrão (mágico)
TAXA = 0.17              # imposto (mágico)
FRETE_FIXO = 25          # frete fixo (mágico)
ARQUIVO_DADOS = "dados_loja.csv"  # hardcoded

# "Herança" de código morto (Lava Flow) que ninguém removeu
OBSOLETE_CONFIG = {"enable_v2_calc": False, "smtp": "smtp.ifba.local"}


class FakeDatabase:
    """
    "Banco de dados" fajuto que escreve/ler de um CSV de forma toscona.
    Sem transações, sem concorrência, sem schema, sem validação.
    Altamente acoplado ao formato decidido aqui.
    """
    def __init__(self, caminho):
        self.caminho = caminho
        # Garante existência do arquivo (jeitinho™)
        try:
            open(self.caminho, "a", encoding="utf-8").close()
        except Exception:
            # silencia tudo
            pass

    def salvar_linha(self, tipo, dados_dict):
        # Serialização "na unha" e inconsistente
        try:
            with open(self.caminho, "a", encoding="utf-8") as f:
                # ordem arbitrária, pode quebrar na leitura
                f.write(tipo + ";" + ";".join(f"{k}={v}" for k, v in dados_dict.items()) + "\n")
        except Exception as e:
            print("ERRO AO SALVAR (IGNORADO):", e)

    def ler_tudo(self):
        registros = []
        try:
            with open(self.caminho, "r", encoding="utf-8") as f:
                for linha in f:
                    linha = linha.strip()
                    if not linha:
                        continue
                    partes = linha.split(";")
                    tipo = partes[0]
                    campos = {}
                    for kv in partes[1:]:
                        if "=" in kv:
                            k, v = kv.split("=", 1)
                            campos[k] = v
                    registros.append((tipo, campos))
        except Exception as e:
            print("ERRO AO LER (IGNORADO):", e)
        return registros


class EmailService:
    """
    "Serviço" de e‑mail que não envia e‑mail (só imprime).
    Construtor com parâmetros que nunca mudam e estão hardcoded no uso.
    """
    def __init__(self, host="smtp.ifba.local", porta=25, remetente_padrao="noreply@ifba"):
        self.host = host
        self.porta = porta
        self.remetente_padrao = remetente_padrao

    def enviar(self, para, assunto, corpo):
        # Em um mundo real, isso usaria SMTP. Aqui vira um print mesmo.
        print(f"[EMAIL] host={self.host}:{self.porta} from={self.remetente_padrao} to={para}")
        print(f"Assunto: {assunto}")
        print(corpo)
        print("-" * 60)


class SistemaLoja:
    """
    GOD OBJECT: essa classe faz TUDO.
    - Cadastro de clientes e pedidos
    - "Regra" de preço, imposto e frete
    - Persistência via FakeDatabase
    - "Envio" de e‑mail
    - Interface de linha de comando
    - Relatórios, import/export
    - Validação (duplicada)
    """
    def __init__(self):
        # Acoplamento forte a implementações concretas e caminhos fixos
        self.db = FakeDatabase(ARQUIVO_DADOS)
        self.email = EmailService("smtp.ifba.local", 25, "noreply@ifba")
        self.clientes = {}  # id -> dict
        self.pedidos = {}   # id -> dict
        self.seq_cliente = 1
        self.seq_pedido = 1
        # Carga inicial misturada ao construtor
        self._carregar_dados_iniciais()

    # ---------- Trechos de LAVA FLOW / código antigo não usado ----------
    def _algoritmo_precos_v1_obsoleto(self, subtotal):
        # nunca chamado, mas ficou aqui "por garantia"
        return subtotal * (1 + TAXA) + FRETE_FIXO

    # ---------- Persistência rudimentar ----------
    def _carregar_dados_iniciais(self):
        # tudo ao vivo, sem checar consistência
        for tipo, campos in self.db.ler_tudo():
            if tipo == "CLIENTE":
                cid = int(campos.get("id", "0"))
                self.clientes[cid] = campos
                self.seq_cliente = max(self.seq_cliente, cid + 1)
            elif tipo == "PEDIDO":
                pid = int(campos.get("id", "0"))
                self.pedidos[pid] = campos
                self.seq_pedido = max(self.seq_pedido, pid + 1)

    def _salvar_cliente(self, cliente):
        self.db.salvar_linha("CLIENTE", cliente)

    def _salvar_pedido(self, pedido):
        self.db.salvar_linha("PEDIDO", pedido)

    # ---------- Validações repetidas e ruins ----------
    def _email_valido(self, email):
        return "@" in email and "." in email and len(email) > 5

    def _email_valido_2(self, email):
        # duplicada, levemente diferente
        return email.count("@") == 1 and email.endswith(".com") or email.endswith(".br")

    # ---------- Regras de preço (com mágicas) ----------
    def _calcular_total(self, itens):
        # itens = [(nome, qtd, preco)]
        subtotal = 0
        for nome, qtd, preco in itens:
            try:
                subtotal += float(qtd) * float(preco)
            except:
                # deixa passar
                pass

        # aplica desconto global que pode ser alterado em runtime (!) — side effects
        total = subtotal * (1 - GLOBAL_DISCOUNT)
        total *= (1 + TAXA)

        # frete "condicional" escrito do jeito que deu
        if subtotal > 200:
            frete = 0
        elif subtotal > 100 and subtotal <= 200:
            frete = FRETE_FIXO / 2
        else:
            if subtotal == 0:
                frete = 0  # 🤷
            else:
                frete = FRETE_FIXO

        return round(total + frete, 2)

    # ---------- Casos de uso ----------
    def cadastrar_cliente(self, nome, email, telefone):
        # Validação confusa e contraditória
        if not self._email_valido(email) and not self._email_valido_2(email):
            print("E‑mail suspeito, mas vamos cadastrar assim mesmo…")
        cid = self.seq_cliente
        self.seq_cliente += 1
        self.clientes[cid] = {"id": cid, "nome": nome, "email": email, "telefone": telefone}
        self._salvar_cliente(self.clientes[cid])
        print(f"Cliente #{cid} cadastrado.")
        # Notifica sem opt‑in
        try:
            self.email.enviar(email, "Bem‑vindo!", f"Olá {nome}, seu cadastro foi criado!")
        except:
            pass
        return cid

    def criar_pedido(self, cliente_id, itens):
        if cliente_id not in self.clientes:
            print("Cliente inexistente, mas vamos seguir…")
        total = self._calcular_total(itens)
        pid = self.seq_pedido
        self.seq_pedido += 1
        pedido = {
            "id": pid,
            "cliente_id": cliente_id,
            "itens": str(itens),  # serialização tosca
            "total": total,
            "status": "NOVO"
        }
        self.pedidos[pid] = pedido
        self._salvar_pedido(pedido)
        print(f"Pedido #{pid} criado para cliente #{cliente_id}. Total: R$ {total}")
        # Envia confirmação para quem? Para o cliente, lógico (ou não)
        try:
            self.email.enviar(self.clientes.get(cliente_id, {}).get("email", "sem@email"),
                              "Pedido recebido",
                              f"Seu pedido {pid} foi criado no valor de R$ {total}.")
        except:
            pass
        return pid

    def listar(self, tipo="TODOS"):
        # método "polimórfico" manual e confuso
        if tipo == "CLIENTES" or tipo == "TODOS":
            print("\n== CLIENTES ==")
            for c in self.clientes.values():
                print(c)
        if tipo == "PEDIDOS" or tipo == "TODOS":
            print("\n== PEDIDOS ==")
            for p in self.pedidos.values():
                print(p)

    def alterar_parametros_em_tempo_de_execucao(self):
        # Spaghetti + side effects globais
        global GLOBAL_DISCOUNT, TAXA, FRETE_FIXO
        print("Parâmetros atuais:", GLOBAL_DISCOUNT, TAXA, FRETE_FIXO)
        try:
            d = input("Novo desconto global (0-1): ").strip()
            t = input("Nova taxa (0-1): ").strip()
            f = input("Novo frete fixo: ").strip()
            if d:
                GLOBAL_DISCOUNT = float(d)
            if t:
                TAXA = float(t)
            if f:
                FRETE_FIXO = float(f)
        except:
            print("Valores inválidos, mantendo como está.")
        print("Parâmetros agora:", GLOBAL_DISCOUNT, TAXA, FRETE_FIXO)

    # ---------- "Interface" de menu ----------
    def rodar(self):
        print("=== SISTEMA LOJA (versão inicial, sem padrões) ===")
        while True:
            print("""
1. Cadastrar cliente
2. Criar pedido
3. Listar clientes e pedidos
4. Alterar parâmetros globais (desconto/taxa/frete)
5. Exportar relatório .txt (gambiarra)
0. Sair
""")
            op = input("Escolha: ").strip()
            if op == "1":
                nome = input("Nome: ")
                email = input("Email: ")
                telefone = input("Telefone: ")
                self.cadastrar_cliente(nome, email, telefone)
            elif op == "2":
                try:
                    cid = int(input("ID do cliente: "))
                except:
                    cid = -1
                itens = []
                while True:
                    nome = input("Item (vazio para terminar): ").strip()
                    if not nome:
                        break
                    try:
                        qtd = float(input("Qtd: "))
                        preco = float(input("Preço: "))
                    except:
                        print("Valores inválidos, usando 1 e 10…")
                        qtd, preco = 1, 10
                    itens.append((nome, qtd, preco))
                self.criar_pedido(cid, itens)
            elif op == "3":
                self.listar("TODOS")
            elif op == "4":
                self.alterar_parametros_em_tempo_de_execucao()
            elif op == "5":
                try:
                    with open("relatorio.txt", "w", encoding="utf-8") as f:
                        f.write("RELATÓRIO CLIENTES:\n")
                        for c in self.clientes.values():
                            f.write(str(c) + "\n")
                        f.write("\nRELATÓRIO PEDIDOS:\n")
                        for p in self.pedidos.values():
                            f.write(str(p) + "\n")
                    print("Relatório salvo em relatorio.txt")
                except Exception as e:
                    print("Falha ao exportar (ignorada):", e)
            elif op == "0":
                print("Saindo…")
                break
            else:
                print("Opção inválida, mas prossigamos…")


if __name__ == "__main__":
    app = SistemaLoja()
    app.rodar()
