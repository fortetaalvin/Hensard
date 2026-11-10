def test_home_page(client):
    assert client.get("/").status_code == 200


def test_submit_request(client):
    r = client.post("/request", data={"name": "Ada", "email": "ada@example.com", "matric": "U19/CS/001",
                                       "kind": "transcript", "copies": "1"})
    assert b"REQ-" in r.data


def test_missing_email_is_rejected(client):
    r = client.post("/request", data={"name": "Ada", "email": "", "matric": "U19/CS/001"})
    assert b"valid email" in r.data
