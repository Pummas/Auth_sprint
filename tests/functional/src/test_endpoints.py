import pytest

from tests.settings import TestSettings

settings = TestSettings()


class BaseData:
    username = 'test'
    email = 'test@mail.ru'
    password = 'test'
    signup_data = {
        'username': username,
        'email': email,
        'password': password
    }
    login_data = {'email': email, 'password': password}
    invalid_login_data = {'email': email, 'password': 'invalid'}


@pytest.fixture(scope="session")
async def setup_function(user):
    user = es_indexes.MovieIndex(settings.es_url, settings.es_port)
    await es_index.create_index('movies')
    data = ''
    for genre_index in films_bulk.data:
        for row in genre_index:
            data += f"{json.dumps(row)}\n"
    await es_client.bulk(data, 'movies', refresh=True)
    yield None
    await es_index.delete_index('movies')


class TestEndpoints:
    def test_sign_up(self, make_post_request):
        """Тест на регистрирование нового пользователя,
        если пользователь уже есть, то сообщить об этом"""
        response = make_post_request("/signup", data=BaseData.signup_data)
        assert response.status_code == 201 or 202
        # 201 - зарегистрировать пользователя,
        # 202 - такой пользователь уже есть

    def test_success_login(self, make_post_request):
        """Тест на login пользователя и обмен
        email+пароль на access token и refresh token"""
        response = make_post_request("/login", BaseData.login_data)
        assert response.status_code == 201
        data = response.json()
        assert data[0].get('access_token') is not None
        assert data[1].get('refresh_token') is not None

    def test_failed_login(self, make_post_request):
        """Тест на ввод неверных данных в login"""
        response = make_post_request(
            "/login", BaseData.invalid_login_data
        )
        assert response.status_code == 403

    def test_refresh(self, make_post_request):
        """Тест на login юзера и обмен его refresh_token
        на новую пару refresh+access"""
        response = make_post_request("/login", BaseData.login_data)
        assert response.status_code == 201
        data = response.json()
        refresh = data[1]
        refresh_response = make_post_request("/refresh", headers=refresh)
        tokens = refresh_response.json()
        assert tokens[0].get('new_access_token') is not None
        assert tokens[1].get('new_refresh_token') is not None

    def test_check_history(self, make_get_request, make_post_request):
        response = make_post_request("/login", BaseData.login_data)
        assert response.status_code == 201
        data = response.json()
        access_token = data[0]
        response = make_get_request("/history", headers=access_token)
        assert response.status_code == 200
        data = response.json()
        login_info = data.get('history')
        assert len(login_info) > 0

    def test_change_password(self, make_post_request):
        """Тест на изменение пароля:
        Залогиниться -> получить токен -> изменить пароль ->
        залогиниться еще раз -> вернуть все обратно"""
        response = make_post_request("/login", BaseData.login_data)
        assert response.status_code == 201

        data = response.json()
        access_token = data[0]
        assert access_token is not None

        email = BaseData.email
        old_password = BaseData.password
        password = 'change'
        change_data = {
            'email': email,
            'old_password': old_password,
            'new_password': password
        }
        change = make_post_request(
            "/change_password", data=change_data, headers=access_token
        )
        assert change.status_code == 200

        response = make_post_request(
            "/login", {'email': email, 'password': password}
        )
        assert response.status_code == 201

        return_old_password = {
            'email': email,
            'old_password': password,
            'new_password': old_password
        }
        change = make_post_request(
            "/change_password", data=return_old_password, headers=access_token
        )
        assert change.status_code == 200

    def test_change_personal_data(self, make_post_request):
        """Тест на изменение username и email:
        Залогиниться -> получить токен -> поменять данные ->
        залогиниться еще раз -> вернуть все обратно"""
        response = make_post_request("/login", BaseData.login_data)
        assert response.status_code == 201

        data = response.json()
        access_token = data[0]
        assert access_token is not None

        new_email = 'change@mail.ru'
        new_username = 'change'
        change_data = {
            'new_email': new_email,
            'new_username': new_username}
        change = make_post_request(
            "/change_data", data=change_data, headers=access_token
        )
        assert change.status_code == 200

        response = make_post_request(
            "/login", {'email': new_email, 'password': BaseData.password}
        )
        assert response.status_code == 201

        change_data = {
            'new_email': BaseData.email,
            'new_username': BaseData.username
        }
        change = make_post_request(
            "/change_data", data=change_data, headers=access_token
        )
        assert change.status_code == 200
