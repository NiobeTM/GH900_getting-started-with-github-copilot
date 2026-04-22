import pytest


class TestActivitiesEndpoint:
    """Tests for the GET /activities endpoint."""

    def test_get_all_activities_success(self, client, mock_activities):
        """
        Test that GET /activities returns all activities with correct structure
        
        Arrange: TestClient ready with mocked activities database
        Act: Make GET request to /activities
        Assert: Response status is 200 and returns all activities
        """
        # Arrange
        expected_activities = mock_activities
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert set(data.keys()) == set(expected_activities.keys())

    def test_get_activities_response_structure(self, client):
        """
        Test that each activity in the response has the correct structure
        
        Arrange: TestClient ready
        Act: Make GET request to /activities
        Assert: Each activity has required fields
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_name, str)
            assert set(activity_data.keys()) == required_fields
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)

    def test_get_activities_participants_are_strings(self, client):
        """
        Test that all participants in activities are strings (email addresses)
        
        Arrange: TestClient ready with mock activities
        Act: Make GET request to /activities
        Assert: All participant entries are email strings
        """
        # Arrange
        # (client fixture already set up)
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant  # Basic email validation
