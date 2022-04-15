import pytest
from django.urls import reverse
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
@pytest.mark.account
@pytest.mark.me
@pytest.mark.me_token_obtain_pair
def test_me_token_obtain_pair_success(tenant_test_api_client, user_credentials, user):
    response = tenant_test_api_client.post(
        path=reverse(viewname='v1:my_app.account:token_obtain_pair'),
        data={
            'username': user_credentials['username'],
            'password': user_credentials['password']
        },
        content_type='application/json'
    )
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert token_backend.decode(response.data['access'])['user_id'] == user.id


@pytest.mark.django_db
@pytest.mark.account
@pytest.mark.me
@pytest.mark.me_token_refresh
def test_me_token_refresh_success(tenant_test_api_client, user):
    refresh_token = RefreshToken.for_user(user)

    response = tenant_test_api_client.post(
        path=reverse(viewname='v1:my_app.account:token_refresh'),
        data={
            'refresh': str(refresh_token)
        },
        content_type='application/json'
    )
    assert response.status_code == 200
    assert 'access' in response.data
    assert token_backend.decode(response.data['access'])['user_id'] == user.id
