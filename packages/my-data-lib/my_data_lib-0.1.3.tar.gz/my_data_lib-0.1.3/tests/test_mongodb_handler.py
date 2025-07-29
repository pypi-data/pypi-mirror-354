"""
Testes para o handler de MongoDB da biblioteca my_data_lib.
"""

from unittest.mock import MagicMock, patch
import pytest
import pandas as pd
from my_data_lib.mongodb_handler import MongoDBHandler

@pytest.fixture
def mock_mongo_client():
    """
    Fixture que faz mock do MongoClient do pymongo para testes sem conexão real.
    """
    with patch("my_data_lib.mongodb_handler.MongoClient") as MockClient:
        mock_client = MockClient.return_value
        mock_db = mock_client.__getitem__.return_value
        mock_collection = mock_db.__getitem__.return_value

        # Mock do método find para retornar lista de documentos
        mock_collection.find.return_value = [
            {"_id": 1, "nome": "teste1"},
            {"_id": 2, "nome": "teste2"},
        ]

        # Mock do método insert_many
        mock_collection.insert_many = MagicMock()

        yield MockClient

def test_mongodb_read_write(mock_mongo_client):
    """
    Testa se o MongoDBHandler consegue ler e escrever corretamente usando mocks.
    """
    handler = MongoDBHandler(uri="mongodb://fake_uri", database="db", collection="col")
    
    df = handler.read()
    assert not df.empty
    assert "nome" in df.columns

    handler.write(df)
    mock_mongo_client.return_value.__getitem__.return_value.__getitem__.return_value.insert_many.assert_called_once()