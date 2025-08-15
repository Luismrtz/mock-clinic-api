from app.repositories import get_all_doctors


def test_repo_get_all_returns_seeded(seeded_doctors):
    docs = get_all_doctors()
    assert len(docs) == len(seeded_doctors)

    expected = {(d.first_name, d.last_name, d.email) for d in seeded_doctors}
    got = {(d.first_name, d.last_name, d.email) for d in docs}
    assert got == expected
