# Arquitetura do Sistema DoeBem

## Modelo arquitetural
O DoeBem utilizará uma arquitetura monolítica em camadas, organizada conforme o padrão MVT do Django.

## Camadas
- Interface: apresentação das páginas e formulários ao usuário.
- Lógica da aplicação: processamento das solicitações e validação das operações.
- Modelos: representação das campanhas, doações, entregas e usuários.
- Persistência: armazenamento dos dados no banco de dados SQLite durante o desenvolvimento.

## Tecnologias
- Python 3.12
- Django 5.2
- HTML5
- CSS3
- Bootstrap 5.3
- SQLite

## Fluxo principal
O voluntário acessa uma campanha, registra uma doação ou entrega e informa o tipo e a quantidade de agasalhos. O sistema valida os dados, atualiza o saldo disponível e registra a movimentação.
