import pytest
from fastapi.testclient import TestClient


class TestRootEndpoint:
    """Tests for the root GET / endpoint."""

    def test_root_redirect_to_static_html(self, client):
        """
        Test that GET / redirects to /static/index.html
        
        Arrange: TestClient is ready
        Act: Make GET request to /
        Assert: Response status is 307 (temporary redirect) and Location header points to /static/index.html
        """
        # Arrange
        # (client fixture already set up)
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
