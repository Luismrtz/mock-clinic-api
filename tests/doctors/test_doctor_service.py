from app.services import list_doctors


def test_service_list_doctors(seeded_doctors):
    docs = list_doctors()
    assert len(docs) == len(seeded_doctors)

    assert {(d.first_name, d.last_name, d.email) for d in docs} == {
        (m.first_name, m.last_name, m.email) for m in seeded_doctors
    }
