import pytest


class TestUnregisterEndpoint:
    """Tests for the DELETE /activities/{activity_name}/signup endpoint."""

    def test_unregister_success(self, client, mock_activities):
        """
        Test successful unregistration from an activity
        
        Arrange: Prepare to remove an existing participant
        Act: DELETE /activities/{activity_name}/signup with participant email
        Assert: Response status is 200, participant removed from activity
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"  # Exists in mock data
        initial_count = len(mock_activities[activity_name]["participants"])
        
        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={email_to_remove}")
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email_to_remove} from {activity_name}"
        assert email_to_remove not in mock_activities[activity_name]["participants"]
        assert len(mock_activities[activity_name]["participants"]) == initial_count - 1

    def test_unregister_nonexistent_participant_returns_400(self, client):
        """
        Test that unregistering a non-existent participant returns 400 error
        
        Arrange: Prepare to remove a participant not in the activity
        Act: DELETE /activities/{activity_name}/signup with non-existent email
        Assert: Response status is 400 with appropriate error message
        """
        # Arrange
        activity_name = "Chess Club"
        nonexistent_email = "nobody@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={nonexistent_email}")
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student not signed up for this activity"

    def test_unregister_nonexistent_activity_returns_404(self, client):
        """
        Test that unregister from non-existent activity returns 404 error
        
        Arrange: Prepare request with invalid activity name
        Act: DELETE /activities/{invalid_name}/signup
        Assert: Response status is 404 with error message
        """
        # Arrange
        activity_name = "NonExistentActivity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_response_contains_message(self, client):
        """
        Test that successful unregister returns expected response structure
        
        Arrange: Prepare valid unregister request
        Act: DELETE /activities/{activity_name}/signup
        Assert: Response contains 'message' field with success text
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")
        data = response.json()
        
        # Assert
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert email in data["message"]

    def test_unregister_all_participants_results_in_empty_list(self, client, mock_activities):
        """
        Test that unregistering all participants leaves an empty list
        
        Arrange: Identify an activity with exactly one participant
        Act: Unregister that one participant
        Assert: Participant list is empty
        """
        # Arrange
        activity_name = "Gym Class"
        participant = "john@mergington.edu"
        
        # Remove the other participants to have only one
        mock_activities[activity_name]["participants"] = [participant]
        
        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={participant}")
        
        # Assert
        assert response.status_code == 200
        assert len(mock_activities[activity_name]["participants"]) == 0
