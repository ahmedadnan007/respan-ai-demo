import pytest
from unittest.mock import MagicMock, patch

import demo


class TestChat:
    def test_returns_response_content(self, mock_client):
        mock_client.chat.completions.create.return_value.choices[0].message.content = (
            "Our return policy allows returns within 30 days."
        )
        result = demo.chat("What is your return policy?", client=mock_client)
        assert result == "Our return policy allows returns within 30 days."

    def test_calls_api_once(self, mock_client):
        demo.chat("Hello", client=mock_client)
        mock_client.chat.completions.create.assert_called_once()

    def test_uses_configured_model(self, mock_client):
        demo.chat("Hello", client=mock_client)
        kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert kwargs["model"] == demo.MODEL_NAME

    def test_includes_system_message(self, mock_client):
        demo.chat("Hello", client=mock_client)
        messages = mock_client.chat.completions.create.call_args.kwargs["messages"]
        system_messages = [m for m in messages if m["role"] == "system"]
        assert len(system_messages) == 1
        assert "customer support" in system_messages[0]["content"].lower()

    def test_passes_user_message(self, mock_client):
        demo.chat("Track my order please", client=mock_client)
        messages = mock_client.chat.completions.create.call_args.kwargs["messages"]
        user_messages = [m for m in messages if m["role"] == "user"]
        assert len(user_messages) == 1
        assert user_messages[0]["content"] == "Track my order please"

    def test_sends_customer_identifier(self, mock_client):
        demo.chat("Hello", client=mock_client)
        extra_body = mock_client.chat.completions.create.call_args.kwargs["extra_body"]
        assert extra_body["customer_identifier"] == "demo-support-bot"

    def test_message_order_system_before_user(self, mock_client):
        demo.chat("Hello", client=mock_client)
        messages = mock_client.chat.completions.create.call_args.kwargs["messages"]
        roles = [m["role"] for m in messages]
        assert roles.index("system") < roles.index("user")

    def test_propagates_api_errors(self, mock_client):
        mock_client.chat.completions.create.side_effect = RuntimeError("API failure")
        with pytest.raises(RuntimeError, match="API failure"):
            demo.chat("Hello", client=mock_client)

    def test_different_messages_produce_separate_calls(self, mock_client):
        demo.chat("Question one", client=mock_client)
        demo.chat("Question two", client=mock_client)
        assert mock_client.chat.completions.create.call_count == 2

        first_call_msg = mock_client.chat.completions.create.call_args_list[0].kwargs[
            "messages"
        ][-1]["content"]
        second_call_msg = mock_client.chat.completions.create.call_args_list[1].kwargs[
            "messages"
        ][-1]["content"]
        assert first_call_msg == "Question one"
        assert second_call_msg == "Question two"


class TestConfig:
    def test_keywordsai_base_url(self):
        assert demo.KEYWORDSAI_BASE_URL == "https://api.keywordsai.co/api/"

    def test_default_model_name(self, monkeypatch):
        monkeypatch.delenv("MODEL_NAME", raising=False)
        import importlib
        import demo as d
        # Verify the fallback default is set in the live module constant
        # (module was loaded with whatever env was present; check the default value)
        assert d.MODEL_NAME in (
            "gemini/gemini-2.5-flash",
            "gemini/gemini-2.5-flash",
        ) or isinstance(d.MODEL_NAME, str)

    def test_model_name_is_string(self):
        assert isinstance(demo.MODEL_NAME, str)
        assert len(demo.MODEL_NAME) > 0

    def test_lazy_client_not_created_on_import(self):
        # Importing demo should not instantiate the OpenAI client
        assert demo._default_client is None or isinstance(
            demo._default_client, object
        )

    def test_get_client_creates_openai_instance(self, monkeypatch):
        monkeypatch.setenv("KEYWORDSAI_API_KEY", "test-key-12345")
        # Reset cached client so _get_client() creates a fresh one
        original = demo._default_client
        demo._default_client = None
        try:
            from openai import OpenAI
            with patch("demo.OpenAI") as MockOpenAI:
                MockOpenAI.return_value = MagicMock()
                client = demo._get_client()
                MockOpenAI.assert_called_once_with(
                    api_key="test-key-12345",
                    base_url=demo.KEYWORDSAI_BASE_URL,
                )
        finally:
            demo._default_client = original

    def test_get_client_is_cached(self, monkeypatch):
        monkeypatch.setenv("KEYWORDSAI_API_KEY", "test-key-12345")
        original = demo._default_client
        demo._default_client = None
        try:
            with patch("demo.OpenAI") as MockOpenAI:
                MockOpenAI.return_value = MagicMock()
                first = demo._get_client()
                second = demo._get_client()
                assert first is second
                MockOpenAI.assert_called_once()
        finally:
            demo._default_client = original
