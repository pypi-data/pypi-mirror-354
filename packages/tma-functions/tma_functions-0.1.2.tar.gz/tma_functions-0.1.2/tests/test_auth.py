from tma_functions.auth import validate_auth_data


def test_validate_auth_data_valid():
    bot_token = "5768337691:AAH5YkoiEuPk8-FZa32hStHTqXiLPtAEhx8"
    auth_data = (
        "query_id=AAHdF6IQAAAAAN0XohDhrOrc&user=%7B%22id%22%3A279058397%2C%22first_name%22%3A%22Vladislav%22%2C"
        "%22last_name%22%3A%22Kibenko%22%2C%22username%22%3A%22vdkfrost%22%2C%22language_code%22%3A%22ru%22%2C"
        "%22is_premium%22%3Atrue%7D&auth_date=1662771648&hash=c501b71e775f74ce10e377dea85a7ea24ecd640b223ea86dfe453e0eaed2e2b2"
    )

    expected = {
        "id": 279058397,
        "first_name": "Vladislav",
        "last_name": "Kibenko",
        "username": "vdkfrost",
        "language_code": "ru",
        "is_premium": True,
    }
    assert validate_auth_data(bot_token, auth_data) == expected


def test_validate_auth_data_invalid_hash():
    bot_token = "5768337691:AAH5YkoiEuPk8-FZa32hStHTqXiLPtAEhx8"
    auth_data = (
        "query_id=AAHdF6IQAAAAAN0XohDhrOrc&user=%7B%22id%22%3A279058397%2C%22first_name%22%3A%22Vladislav%22%2C"
        "%22last_name%22%3A%22Kibenko%22%2C%22username%22%3A%22vdkfrost%22%2C%22language_code%22%3A%22ru%22%2C"
        "%22is_premium%22%3Atrue%7D&auth_date=1662771648&hash=invalid_hash"
    )
    assert validate_auth_data(bot_token, auth_data) is None


def test_validate_auth_data_missing_hash():
    bot_token = "123456:ABC-DEF1234ghIkl-799-jkm-o_o_o_o"
    auth_data = (
        'auth_date=1678886400\nquery_id=AAABAQABAAAAAQABAAAAAQAB\nuser={"id":123,"first_name":"John","last_name":"Doe",'
        '"username":"john_doe","language_code":"en","allows_write_to_pm":true,"photo_url":"https://example.com/photo.jpg"}'
    )
    assert validate_auth_data(bot_token, auth_data) is None


def test_validate_auth_data_invalid_data_format():
    bot_token = "123456:ABC-DEF1234ghIkl-799-jkm-o_o_o_o"
    auth_data = "not_a_valid_format"
    assert validate_auth_data(bot_token, auth_data) is None
