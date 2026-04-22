import pytest


class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client, mock_activities):
        """
        Test successful signup for an activity
        
        Arrange: Prepare a new email not yet registered for an activity
        Act: POST to /activities/{activity_name}/signup with email
        Assert: Response status is 200, participant added to activity
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "new_student@mergington.edu"
        initial_count = len(mock_activities[activity_name]["participants"])
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={new_email}")
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
        assert new_email in mock_activities[activity_name]["participants"]
        assert len(mock_activities[activity_name]["participants"]) == initial_count + 1

    def test_signup_duplicate_email_rejected(self, client, mock_activities):
        """
        Test that duplicate signup is rejected with 400 error
        
        Arrange: Use an email already registered for an activity
        Act: POST to /activities/{activity_name}/signup with duplicate email
        Assert: Response status is 400 with appropriate error message
        """
        # Arrange
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already in participants
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={existing_email}")
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is already signed up"

    def test_signup_nonexistent_activity_returns_404(self, client):
        """
        Test that signup for non-existent activity returns 404 error
        
        Arrange: Prepare request with invalid activity name
        Act: POST to /activities/{invalid_name}/signup
        Assert: Response status is 404 with error message
        """
        # Arrange
        activity_name = "NonExistentActivity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_with_hyphen_in_email(self, client, mock_activities):
        """
        Test that email with hyphen can be signed up
        
        Arrange: Prepare email with hyphen character
        Act: POST to /activities/{activity_name}/signup with hyphenated email
        Assert: Response status is 200 and participant added
        """
        # Arrange
        activity_name = "Programming Class"
        hyphenated_email = "student-name@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={hyphenated_email}")
        
        # Assert
        assert response.status_code == 200
        assert hyphenated_email in mock_activities[activity_name]["participants"]

    def test_signup_response_contains_message(self, client):
        """
        Test that successful signup returns expected response structure
        
        Arrange: Prepare valid signup request
        Act: POST to /activities/{activity_name}/signup
        Assert: Response contains 'message' field with success text
        """
        # Arrange
        activity_name = "Gym Class"
        email = "athlete@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        data = response.json()
        
        # Assert
        assert "message" in data
        assert "Signed up" in data["message"]
        assert email in data["message"]
