from typing import Optional
import pandas as pd
from my_data_lib.logger import Logger

class CSVHandler:
    """
    Manipula operações de leitura e escrita em arquivos CSV.

    Args:
        path (str): Caminho do arquivo CSV a ser manipulado.
    """

    def __init__(self, path: str):
        """
        Inicializa o handler para um arquivo CSV específico.

        Args:
            path (str): Caminho do arquivo CSV.
        """
        self.path = path
        self.logger = Logger()

    def read(self) -> pd.DataFrame:
        """
        Lê os dados do arquivo CSV e retorna um DataFrame.

        Returns:
            pandas.DataFrame: Dados lidos do arquivo CSV.
        """
        self.logger.info(f"Lendo dados do arquivo CSV: {self.path}")
        try:
            df = pd.read_csv(self.path)
            self.logger.info(f"Leitura bem-sucedida. Linhas: {df.shape[0]}")
            return df
        except Exception as e:
            self.logger.error(f"Erro ao ler arquivo CSV: {e}")
            raise

    def write(self, df: pd.DataFrame):
        """
        Escreve um DataFrame no arquivo CSV especificado.

        Args:
            df (pandas.DataFrame): DataFrame a ser salvo no arquivo CSV.
        """
        self.logger.info(f"Gravando dados no arquivo CSV: {self.path}")
        try:
            df.to_csv(self.path, index=False)
            self.logger.info("Gravação bem-sucedida.")
        except Exception as e:
            self.logger.error(f"Erro ao gravar arquivo CSV: {e}")
            raise
