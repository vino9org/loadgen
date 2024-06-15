from api_tasks import _random_characters_


def test_random_characters():
    assert len(_random_characters_(10)) == 10
