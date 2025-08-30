README: Versão Inicial (Propositalmente Mal Projetada)
Sistema Loja — Versão Inicial (Sem Padrões)
ATENÇÃO: Esta é uma versão propositalmente mal projetada para fins de estudo. Ela serve como um exemplo claro de "o que não fazer", concentrando uma série de anti-patterns e violações de princípios de design para evidenciar os problemas de uma arquitetura de software fraca.

Como Executar
O sistema é contido em um único arquivo e não requer nenhuma dependência externa além de uma versão recente do Python.

Requisitos:

Python 3.10+

Passos:

Navegue até o diretório do projeto:

Bash

cd versao_inicial
Execute o script principal:

Bash

python main.py
Um menu interativo será exibido no terminal, permitindo cadastrar clientes, criar pedidos e listar os dados. Os registros são salvos de forma frágil em um arquivo dados_loja.csv no mesmo diretório.

Diagnóstico da Arquitetura
Esta versão sofre de graves problemas de design que a tornam difícil de manter, testar e estender.

Anti-Patterns Identificados
God Object (Objeto Divino): A classe SistemaLoja é o exemplo perfeito deste anti-pattern. Ela centraliza todas as responsabilidades do sistema:

Interface com o usuário (método rodar).

Regras de negócio (cálculo de totais em _calcular_total).

Persistência de dados (através do acoplamento direto com FakeDatabase).

Notificações por e-mail (EmailService).

Spaghetti Code (Código Espaguete): O método rodar possui um fluxo de controle confuso, baseado em uma série de if/elif e input()s aninhados, tornando a lógica difícil de seguir e modificar.

Lava Flow (Fluxo de Lava): O código contém "código morto" que ninguém se atreve a remover. Exemplos claros são a variável OBSOLETE_CONFIG e o método _algoritmo_precos_v1_obsoleto, que não são chamados em nenhum lugar.

Hard Coded Values / Magic Numbers (Valores "Hardcoded"): Constantes de negócio como GLOBAL_DISCOUNT, TAXA, e FRETE_FIXO estão definidas diretamente no código, sem uma fonte centralizada, dificultando a configuração e o entendimento das regras.

Violações dos Princípios SOLID
Princípio da Responsabilidade Única (SRP): Violado flagrantemente pela classe SistemaLoja, que faz muito mais do que uma única coisa.

Princípio do Aberto/Fechado (OCP): O sistema é fechado para extensão. Adicionar uma nova opção de menu ou uma nova regra de frete exige a modificação direta do código existente nos métodos rodar e _calcular_total.

Princípio da Inversão de Dependência (DIP): A classe SistemaLoja depende diretamente de implementações concretas (FakeDatabase, EmailService), instanciando-as em seu construtor. Isso cria um forte acoplamento que impede a fácil substituição dessas dependências.

Diagrama UML da Versão Inicial
Snippet de código

classDiagram
    class SistemaLoja {
        -db: FakeDatabase
        -email: EmailService
        +cadastrar_cliente(nome, email, telefone)
        +criar_pedido(cliente_id, itens)
        +rodar()
    }

    class FakeDatabase {
        +salvar_linha(tipo, dados_dict)
        +ler_tudo()
    }

    class EmailService {
        +enviar(para, assunto, corpo)
    }

    SistemaLoja "1" *-- "1" FakeDatabase : compõe
    SistemaLoja "1" *-- "1" EmailService : compõe
README: Versão Refatorada (Arquitetura Limpa)
Sistema Loja — Versão Refatorada com Arquitetura Limpa
Esta versão do sistema foi completamente reestruturada para seguir boas práticas de engenharia de software, utilizando uma arquitetura em camadas, princípios SOLID e Inversão de Controle (IoC).

Principais Melhorias
Arquitetura em Camadas: O código foi organizado em quatro camadas distintas (domain, services, infrastructure, app), separando claramente as responsabilidades.

Inversão de Dependência: As classes de serviço agora dependem de interfaces (Ports) definidas no domínio, não de implementações concretas, seguindo o Princípio da Inversão de Dependência.

Inversão de Controle (IoC): Um Service Locator foi implementado para gerenciar o ciclo de vida e o fornecimento das dependências, desacoplando os componentes.

Configuração Centralizada: "Números mágicos" foram eliminados e movidos para um arquivo app/settings.py.

Interface de Linha de Comando (CLI): A interação com o usuário foi reimplementada de forma robusta com a biblioteca argparse.

Como Executar
Requisitos:

Python 3.10+

Passos:

Navegue até o diretório do projeto:

Bash

cd versao_refatorada
Use a interface de linha de comando para interagir com o sistema. Veja a ajuda para todas as opções:

Bash

python -m app.cli --help
Exemplos de Uso:

Bash

# Cadastrar um novo cliente
python -m app.cli clientes add --nome "Maria" --email "maria@example.com" --telefone "71999990000"

# Listar todos os clientes
python -m app.cli clientes list

# Criar um novo pedido para o cliente de ID 1
python -m app.cli pedidos add --cliente-id 1 --item "Teclado Mecanico:1:150.0" --item "Mouse Gamer:2:75.50"

# Listar todos os pedidos
python -m app.cli pedidos list
Os dados são armazenados em ./data/clientes.csv e ./data/pedidos.csv.

Diagrama UML da Versão Refatorada
Este diagrama ilustra a nova arquitetura, incluindo as relações entre as entidades de domínio e a separação por camadas.

Snippet de código

classDiagram
    direction LR

    subgraph domain
        Customer "1" <-- "many" Order : "é associado a"
        Order "*" o-- "1..*" OrderItem : "contém"

        class Customer {
            +id: int
            +name: str
            +email: str
            +phone: str
        }
        class Order {
            +id: int
            +customer_id: int
            +items: List~OrderItem~
            +total: float
            +status: str
        }
        class OrderItem {
            +name: str
            +quantity: float
            +price: float
        }

        class RepositoryPort { <<Interface>> }
        class EmailServicePort { <<Interface>> }
        class PricingServicePort { <<Interface>> }
    end

    subgraph services
        class CustomerService { -repo: RepositoryPort }
        class OrderService { -repo: RepositoryPort }
        class PricingService { }
    end

    subgraph infrastructure
        class CsvRepository { }
        class ConsoleEmailService { }
    end

    subgraph app
      class ServiceLocator { +resolve(key) }
      class CLI { }
    end

    CsvRepository ..|> RepositoryPort
    ConsoleEmailService ..|> EmailServicePort
    CustomerService o-- RepositoryPort
    OrderService o-- RepositoryPort
    CLI --> ServiceLocator : uses