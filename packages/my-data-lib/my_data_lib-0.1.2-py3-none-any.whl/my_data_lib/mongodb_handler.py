from typing import Optional
import pandas as pd
from pymongo import MongoClient
from my_data_lib.logger import Logger

class MongoDBHandler:
    """
    Manipula operações de leitura e escrita em uma coleção MongoDB.

    Args:
        uri (str): URI de conexão com o MongoDB.
        database (str): Nome do banco de dados.
        collection (str): Nome da coleção.
    """

    def __init__(self, uri: str, database: str, collection: str):
        """
        Inicializa o handler para uma coleção MongoDB específica.

        Args:
            uri (str): URI de conexão com o MongoDB.
            database (str): Nome do banco de dados.
            collection (str): Nome da coleção.
        """
        self.client = MongoClient(uri)
        self.collection = self.client[database][collection]
        self.logger = Logger()

    def read(self) -> pd.DataFrame:
        """
        Lê documentos da coleção MongoDB e retorna um DataFrame.

        Args:
            filter_query (dict, opcional): Filtro para consulta MongoDB. Padrão é None (retorna todos).

        Returns:
            pandas.DataFrame: Dados lidos da coleção MongoDB.
        """
        self.logger.info(f"Lendo dados do MongoDB, coleção: {self.collection.name}")
        try:
            data = list(self.collection.find())
            df = pd.DataFrame(data)
            self.logger.info(f"Leitura bem-sucedida. Linhas: {df.shape[0]}")
            return df
        except Exception as e:
            self.logger.error(f"Erro ao ler dados do MongoDB: {e}")
            raise

    def write(self, df: pd.DataFrame):
        """
        Escreve os dados de um DataFrame na coleção MongoDB.

        Args:
            df (pandas.DataFrame): DataFrame a ser inserido na coleção.
        """
        self.logger.info(f"Gravando dados no MongoDB, coleção: {self.collection.name}")
        try:
            self.collection.delete_many({})
            self.collection.insert_many(df.to_dict(orient="records"))
            self.logger.info("Gravação bem-sucedida.")
        except Exception as e:
            self.logger.error(f"Erro ao gravar dados no MongoDB: {e}")
            raise
