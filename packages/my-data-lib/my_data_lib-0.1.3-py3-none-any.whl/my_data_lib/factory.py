from typing import Literal, Union, Optional
from .csv_handler import CSVHandler
from .postgres_handler import PostgresHandler
from .mongodb_handler import MongoDBHandler

def get_data_handler(
    source_type: Literal["csv", "postgres", "mongodb"],
    path: str = "",
    host: str = "",
    port: int = 0,
    database: str = "",
    user: str = "",
    password: str = "",
    uri: str = "",
    collection: str = "",
    table_name: str = ""
) -> Union[CSVHandler, PostgresHandler, MongoDBHandler]:
    """
    Cria e retorna um handler de dados conforme o tipo de fonte.

    Parâmetros:
        source_type (str): 'csv', 'postgres' ou 'mongodb'.
        path (str): Necessário para CSV.
        host, port, database, user, password (str/int): Necessários para Postgres.
        uri, database, collection (str): Necessários para MongoDB.
        table_name (str, opcional): Nome da tabela para Postgres.

    Retorna:
        Instância do handler correspondente.
    """
    if source_type == "csv":
        if not path:
            raise ValueError("O parâmetro 'path' é obrigatório para CSVHandler.")
        return CSVHandler(path=path)
    elif source_type == "postgres":
        if not all([host, port, database, user, password]):
            raise ValueError("Parâmetros obrigatórios para PostgresHandler: host, port, database, user, password.")
        connection_string = (
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        )
        return PostgresHandler(
            connection_string=connection_string,
            table_name=None
        )
    elif source_type == "mongodb":
        if not all([uri, database, collection]):
            raise ValueError("Parâmetros obrigatórios para MongoDBHandler: uri, database, collection.")
        return MongoDBHandler(
            uri=uri,
            database=database,
            collection=collection
        )
    else:
        raise ValueError(f"Fonte de dados '{source_type}' não suportada.")