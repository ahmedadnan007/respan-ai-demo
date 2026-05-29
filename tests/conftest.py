import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_client():
    client = MagicMock()
    response = MagicMock()
    response.choices[0].message.content = "Mock AI response"
    client.chat.completions.create.return_value = response
    return client
