import logging

class Logger:
    """
    Logger utilitário para registrar mensagens de informação, erro e debug.

    Args:
        name (str, opcional): Nome do logger. Padrão é 'data_lib'.
    """

    def __init__(self, name: str = "data_lib"):
        """
        Inicializa o logger com o nome especificado.

        Args:
            name (str, opcional): Nome do logger. Padrão é 'data_lib'.

        Nota:
            Para evitar mensagens duplicadas no log, o handler só é adicionado se ainda não houver handlers
            associados ao logger. Isso garante que múltiplas instâncias desta classe não causem duplicidade
            de mensagens no console.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def info(self, message: str):
        """
        Registra uma mensagem de informação.

        Args:
            message (str): Mensagem a ser registrada.
        """
        self.logger.info(message)

    def error(self, message: str):
        """
        Registra uma mensagem de erro.

        Args:
            message (str): Mensagem a ser registrada.
        """
        self.logger.error(message)

    def debug(self, message: str):
        """
        Registra uma mensagem de debug.

        Args:
            message (str): Mensagem a ser registrada.
        """
        self.logger.debug(message)
