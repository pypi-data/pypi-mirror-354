# my_data_lib

Uma biblioteca Python para manipulação de dados em diferentes fontes, com interface unificada e fácil de usar.

---

## Índice

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Como usar](#como-usar)
- [Desenvolvimento](#desenvolvimento)
- [Testes](#testes)
- [Distribuição no PyPI](#distribuição-no-pypi)

---

## Estrutura do Projeto

```
my_data_lib/
│
├── my_data_lib/                # Código-fonte da biblioteca
│   ├── __init__.py
│   ├── factory.py
│   ├── csv_handler.py
│   ├── postgres_handler.py
│   ├── mongodb_handler.py
│   └── logger.py
│
├── examples/                   # Exemplos de uso
│   ├── example_csv.py
│   ├── example_ETL.py
│   ├── example_postgres.py
│   └── example_mongo.py
│
├── tests/                      # Testes automatizados
│   ├── __init__.py
│   ├── test_csv_handler.py
│   ├── test_postgres_handler.py
│   └── test_mongodb_handler.py
│
├── requirements.txt
├── pyproject.toml
├── README.md
```

---

## Instalação

Instale a biblioteca diretamente do PyPI:

```
pip install my_data_lib
```

As dependências necessárias serão instaladas automaticamente.

---

## Como usar

Veja exemplos práticos na pasta [`examples/`](examples/):

- **Para manipular CSV:**  
  Consulte o arquivo [`examples/example_csv.py`](examples/example_csv.py).

- **Para manipular PostgreSQL:**  
  Consulte o arquivo [`examples/example_postgres.py`](examples/example_postgres.py).

- **Para manipular MongoDB:**  
  Consulte o arquivo [`examples/example_mongo.py`](examples/example_mongo.py).

- **Para um fluxo completo ETL (Extract, Transform, Load):**  
  Consulte o arquivo [`examples/example_ETL.py`](examples/example_ETL.py).

---

## Desenvolvimento

Para contribuir ou desenvolver localmente:

1. Clone o repositório:
    ```
    git clone https://github.com/seu_usuario/my_data_lib.git
    cd my_data_lib
    ```
2. Instale as dependências:
    ```
    pip install -r requirements.txt
    ```
3. Faça suas alterações no código-fonte dentro da pasta `my_data_lib/`.

---

## Testes

Os testes automatizados estão na pasta `tests/`.  
Para rodar os testes:

```
python -m pytest
```

---

## Distribuição no PyPI

Para empacotar e publicar uma nova versão:

1. Atualize a versão em `pyproject.toml`.
2. Gere os arquivos de distribuição:
    ```
    python -m build
    ```
3. Faça upload para o PyPI:
    ```
    python -m twine upload dist/*
    ```
   Use seu usuário do PyPI ou um API token.

---
