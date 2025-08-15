from app.schema import DoctorRead


def test_get_doctors_returns_json_list(client, seeded_doctors):
    resp = client.get("/api/doctors/")
    assert resp.status_code == 200

    data = resp.get_json()
    doctors = [DoctorRead(**item) for item in data]
    assert len(doctors) == len(seeded_doctors)

    got = {(d["first_name"], d["last_name"], d["email"]) for d in data}
    expected = {(d.first_name, d.last_name, d.email) for d in seeded_doctors}
    assert got == expected
