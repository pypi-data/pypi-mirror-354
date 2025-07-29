import pytest
from sentor import Client
from unittest.mock import Mock

@pytest.fixture
def mock_client():
    client = Client("test-key")
    client._make_request = Mock()
    return client

def test_sentiment_analysis(mock_client):
    mock_client._make_request.return_value = {
        "results": [
            {
                "predicted_label": "positive",
                "probabilities": {
                    "positive": 0.95
                }
            }
        ]
    }
    
    result = mock_client.analyze("Test text")
    assert result['results'][0]['predicted_label'] == "positive"
    assert result['results'][0]['probabilities']['positive'] == 0.95

def test_client_initialization():
    client = Client()
    assert isinstance(client, Client)

def test_client_connection():
    client = Client()
    assert client.is_connected() == False
    # Add more specific test cases based on your client implementation

def test_client_operations():
    client = Client()
    # Add test cases for specific client operations
    pass

if __name__ == "__main__":
    pytest.main([__file__])