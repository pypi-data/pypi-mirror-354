from typing import Optional
import pandas as pd
from pymongo import MongoClient
from my_data_lib.logger import Logger
from pymongo.collection import Collection

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

        Nota:
            Cria a conexão com o MongoDB e inicializa os atributos de acesso à base e coleção.
            O atributo `self.col` é do tipo `Collection` do PyMongo e deve ser usado para operações como find, insert_many, etc.
        """
        self.uri: str = uri
        self.database: str = database
        self.collection: str = collection
        self.logger = Logger()
        self.client: MongoClient = MongoClient(self.uri)
        self.db = self.client[self.database]
        self.col: Collection = self.db[self.collection]

    def read(self, filter_query: Optional[dict] = None) -> pd.DataFrame:
        """
        Lê documentos da coleção MongoDB e retorna um DataFrame.

        Args:
            filter_query (dict, opcional): Filtro para consulta MongoDB. Padrão é None (retorna todos).

        Returns:
            pandas.DataFrame: Dados lidos da coleção MongoDB.
        """
        self.logger.info(f"Lendo dados da coleção MongoDB: {self.collection}")
        try:
            cursor = self.col.find(filter_query or {})
            df = pd.DataFrame(list(cursor))
            self.logger.info(f"Leitura bem-sucedida. Linhas: {df.shape[0]}")
            return df
        except Exception as e:
            self.logger.error(f"Erro ao ler coleção MongoDB: {e}")
            raise

    def write(self, df: pd.DataFrame):
        """
        Escreve os dados de um DataFrame na coleção MongoDB.

        Args:
            df (pandas.DataFrame): DataFrame a ser inserido na coleção.
        """
        self.logger.info(f"Gravando dados no MongoDB, coleção: {self.collection}")
        try:
            self.col.delete_many({})
            self.col.insert_many(df.to_dict(orient="records"))
            self.logger.info("Gravação bem-sucedida.")
        except Exception as e:
            self.logger.error(f"Erro ao gravar dados no MongoDB: {e}")
            raise
