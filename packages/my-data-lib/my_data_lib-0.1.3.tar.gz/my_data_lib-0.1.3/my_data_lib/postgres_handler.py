from typing import Optional
import pandas as pd
import psycopg2
import sqlalchemy
import os
from my_data_lib.logger import Logger

class PostgresHandler:
    """
    Manipula operações de leitura e escrita em uma tabela do PostgreSQL.

    Args:
        connection_string (str): String de conexão com o banco PostgreSQL.
        table_name (str): Nome da tabela a ser manipulada.
    """

    def __init__(self, connection_string=None, table_name=None):
        """
        Inicializa o handler para uma tabela PostgreSQL.

        Args:
            connection_string (str): String de conexão.
            table_name (str, opcional): Nome da tabela.
        """
        self.table_name = table_name
        self.engine = create_engine(connection_string)
        self.logger = Logger()

    def read(self) -> pd.DataFrame:
        """
        Lê todos os dados da tabela PostgreSQL e retorna um DataFrame.

        Returns:
            pandas.DataFrame: Dados lidos da tabela.
        """
        self.logger.info(f"Lendo dados da tabela PostgreSQL: {self.table_name}")
        try:
            df = pd.read_sql_table(self.table_name, self.engine)
            self.logger.info(f"Leitura bem-sucedida. Linhas: {df.shape[0]}")
            return df
        except Exception as e:
            self.logger.error(f"Erro ao ler tabela PostgreSQL: {e}")
            raise

    def write(self, df: pd.DataFrame):
        """
        Escreve um DataFrame na tabela PostgreSQL.

        Args:
            df (pandas.DataFrame): DataFrame a ser salvo.
        """
        self.logger.info(f"Gravando dados na tabela PostgreSQL: {self.table_name}")
        try:
            df.to_sql(self.table_name, self.engine, if_exists="replace", index=False)
            self.logger.info("Gravação bem-sucedida.")
        except Exception as e:
            self.logger.error(f"Erro ao gravar tabela PostgreSQL: {e}")
            raise
