from core.content_filter import ContentFilter

def test_sanitize_api_key():
    content = "api_key = '12345'"
    filter = ContentFilter()
    assert '[REDACTED]' in filter.sanitize(content)
