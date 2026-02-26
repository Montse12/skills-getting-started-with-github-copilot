def test_root_redirect(client):
    # Arrange
    # (nothing to setup beyond fixture)

    # Act - prevent TestClient from following the redirect so we can inspect it
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (307, 308)
    assert "/static/index.html" in response.headers["location"]


def test_get_activities_returns_expected_structure(client):
    # Arrange
    # default state is provided by fixture

    # Act
    resp = client.get("/activities")
    data = resp.json()

    # Assert
    assert resp.status_code == 200
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_new_student(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    post = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert post.status_code == 200
    assert email in post.json()["message"]

    # verify that GET shows participant now present
    get = client.get("/activities")
    assert email in get.json()[activity]["participants"]


def test_signup_duplicate_fails(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already in initial data

    # Act
    post = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert post.status_code == 400
    assert post.json()["detail"] == "Student already signed up"


def test_remove_existing_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    delete = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert delete.status_code == 200
    assert email in delete.json()["message"]

    # follow-up GET should not include email
    get = client.get("/activities")
    assert email not in get.json()[activity]["participants"]


def test_remove_nonexistent_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "nobody@mergington.edu"

    # Act
    delete = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert delete.status_code == 404
    assert delete.json()["detail"] == "Participant not found"
