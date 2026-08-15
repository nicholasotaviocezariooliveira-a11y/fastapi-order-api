# 🚀 FastAPI Order API

API REST em FastAPI para cadastro e autenticação de usuários, além do gerenciamento de pedidos e itens de pedido. A aplicação usa JWT para proteger as rotas de pedidos, SQLAlchemy para persistência e SQLite como banco de dados configurado no projeto.

## 📌 Sobre o projeto

O projeto expõe recursos para criar contas, autenticar usuários e renovar tokens de acesso. Usuários autenticados podem criar pedidos, incluir ou remover itens, cancelar ou finalizar pedidos e consultar informações de pedidos conforme as permissões implementadas.

As rotas de pedidos dependem de um token Bearer válido. Algumas operações também verificam se o usuário é administrador ou proprietário do pedido.

## ✨ Funcionalidades

- Cadastro de usuários com senha armazenada usando bcrypt.
- Login por JSON ou formulário OAuth2 e emissão de tokens JWT.
- Renovação de token de acesso.
- Criação, consulta, cancelamento e finalização de pedidos.
- Inclusão e remoção de itens, com recálculo do preço do pedido.
- Listagem de pedidos para administradores e consulta dos pedidos do usuário autenticado.
- Migrações de esquema versionadas com Alembic.

## 🛠️ Tecnologias

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/) e SQLite
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [python-jose](https://python-jose.readthedocs.io/) para JWT
- [Passlib](https://passlib.readthedocs.io/) com bcrypt
- [python-dotenv](https://github.com/theskumar/python-dotenv)

## 📁 Estrutura do projeto

```text
.
├── alembic/                         # Ambiente e versões de migração do banco
│   ├── env.py                       # Configuração do Alembic e metadata SQLAlchemy
│   └── versions/                    # Revisões de esquema
├── alembic.ini                      # Configuração do Alembic (SQLite local)
├── main.py                          # Aplicação FastAPI e configurações de autenticação
├── auth_routes.py                   # Rotas de cadastro, login e renovação de token
├── order_routes.py                  # Rotas protegidas de pedidos e itens
├── models.py                        # Modelos SQLAlchemy: Usuario, Pedido e ItemPedidos
├── schemas.py                       # Schemas Pydantic de entrada e resposta
├── dependencie.py                   # Sessão do banco e validação de token JWT
└── teste.py                         # Cliente manual de requisição HTTP
```

## ⚙️ Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/nicholasotaviocezariooliveira-a11y/fastapi-order-api.git
cd fastapi-order-api
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

O repositório não possui um arquivo de dependências. Instale os pacotes importados pelo projeto:

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy sqlalchemy-utils alembic \
  python-dotenv "passlib[bcrypt]" "python-jose[cryptography]" python-multipart requests
```

## 🔐 Variáveis de ambiente

`main.py` carrega as configurações de um arquivo `.env`. Crie esse arquivo na raiz do projeto e mantenha-o fora do controle de versão.

Exemplo de valores de desenvolvimento:

```env
SECRET_KEY=uma_chave_secreta_de_desenvolvimento
ALGORITHM=HS256
ACCESS_TOCKEN_EXPIRE_MINUTES=30
```

> O nome `ACCESS_TOCKEN_EXPIRE_MINUTES` segue exatamente a variável lida pelo código atual.

Não publique chaves, tokens, senhas ou conteúdo do seu `.env`.

## 🗄️ Banco de dados e migrações

O projeto configura SQLite no arquivo `alembic.ini`, apontando para `sqlite:///banco.db`. O arquivo do banco é local e está ignorado pelo Git.

As migrações Alembic criam as tabelas `usuarios`, `pedidos` e `itens_pedido`. Para aplicar todas as revisões:

```bash
alembic upgrade head
```

Para criar uma nova revisão após alterações nos modelos:

```bash
alembic revision --autogenerate -m "descricao_da_migracao"
```

Revise a migração gerada antes de aplicá-la.

## ▶️ Executando o projeto

Com o ambiente virtual ativo e as variáveis configuradas, inicie o servidor:

```bash
uvicorn main:app --reload
```

Por padrão, a aplicação estará disponível em `http://127.0.0.1:8000`.

## 📚 Documentação da API

Como a aplicação usa FastAPI, com o servidor em execução a documentação interativa fica disponível em:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Esquema OpenAPI: `http://127.0.0.1:8000/openapi.json`

Para autenticar rotas protegidas na interface, obtenha um token em `POST /auth/login-form` e informe-o como Bearer token no botão **Authorize**.

## 📡 Principais endpoints

As rotas abaixo são as declaradas no código atual. As rotas sob `/pedidos` exigem autenticação Bearer.

| Método | Rota | Finalidade |
| --- | --- | --- |
| `GET` | `/auth/` | Rota padrão de autenticação. |
| `POST` | `/auth/criar_conta` | Cria uma conta de usuário. |
| `POST` | `/auth/login` | Autentica usando e-mail e senha enviados em JSON. |
| `POST` | `/auth/login-form` | Autentica usando formulário OAuth2. |
| `GET` | `/auth/refresh` | Gera novo token de acesso para o usuário autenticado. |
| `GET` | `/pedidos/` | Rota padrão de pedidos. |
| `POST` | `/pedidos/pedido` | Cria um pedido para um usuário informado. |
| `POST` | `/pedidos/pedido/cancelar/{id_pedido}` | Cancela um pedido existente. |
| `POST` | `/pedidos/pedido/adicionar-item/{id_pedido}` | Adiciona um item ao pedido. |
| `POST` | `/pedidos/pedido/remover-item/{id_item_pedido}` | Remove um item do pedido. |
| `POST` | `/pedidos/pedido/finalizar/{id_pedido}` | Finaliza um pedido. |
| `GET` | `/pedidos/listar` | Lista todos os pedidos para usuários administradores. |
| `GET` | `/pedidos/pedido/{id.pedido}` | Consulta um pedido; rota declarada em `order_routes.py`. |
| `GET` | `/pedidos/listar/pedidos.usuario` | Lista os pedidos do usuário autenticado. |

## 🧪 Testes

Não há uma suíte de testes automatizados ou uma configuração de test runner no repositório. O arquivo `teste.py` é um cliente manual que realiza uma requisição HTTP para a rota de renovação de token. Para testes automatizados, será necessário adicionar uma ferramenta e casos de teste ao projeto.

## 👨‍💻 Autor

`nicholasotaviocezariooliveira-a11y` — identificação disponível no histórico Git do repositório.
