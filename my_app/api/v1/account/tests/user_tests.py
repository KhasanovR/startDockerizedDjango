import pytest
from django.contrib.auth.models import Group
from django.urls import reverse


@pytest.fixture(scope='module')
def group(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return Group.objects.create()


@pytest.mark.django_db
@pytest.mark.account
@pytest.mark.user
@pytest.mark.user_list
def test_user_list_success(tenant_test_api_client):
    response = tenant_test_api_client.get(
        path=reverse(viewname='v1:my_app.account:users-list'),
        content_type='application/json'
    )
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.account
@pytest.mark.user
@pytest.mark.user_create
def test_user_create_success(tenant_test_api_client):
    response = tenant_test_api_client.post(
        path=reverse(viewname='v1:my_app.account:users-list'),
        data={
            'password': '12345-Test',
            'username': 'Test',
        },
        content_type='application/json'
    )
    assert response.status_code == 201


@pytest.mark.django_db
@pytest.mark.account
@pytest.mark.user
@pytest.mark.user_retrieve
def test_user_retrieve_success(tenant_test_api_client, user):
    response = tenant_test_api_client.get(
        path=reverse(viewname='v1:my_app.account:users-detail', kwargs={'pk': user.id}),
        content_type='application/json'
    )
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.account
@pytest.mark.user
@pytest.mark.user_update
def test_user_update_success(tenant_test_api_client, user):
    response = tenant_test_api_client.put(
        path=reverse(viewname='v1:my_app.account:users-detail', kwargs={'pk': user.id}),
        data={
            'password': '12345-Demo',
            'username': 'Demo',
        },
        content_type='application/json'
    )
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.account
@pytest.mark.user
@pytest.mark.user_partial_update
def test_user_partial_update_success(tenant_test_api_client, user):
    response = tenant_test_api_client.patch(
        path=reverse(viewname='v1:my_app.account:users-detail', kwargs={'pk': user.id}),
        data={
            'username': 'DemoTester',
        },
        content_type='application/json'
    )
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.account
@pytest.mark.user
@pytest.mark.user_destroy
def test_user_delete_success(tenant_test_api_client, user):
    response = tenant_test_api_client.delete(
        path=reverse(viewname='v1:my_app.account:users-detail', kwargs={'pk': user.id}),
        content_type='application/json'
    )
    assert response.status_code == 204


@pytest.mark.django_db
@pytest.mark.account
@pytest.mark.user
@pytest.mark.user_activate
def test_user_activate_success(tenant_test_api_client, user):
    response = tenant_test_api_client.post(
        path=reverse(viewname='v1:my_app.account:users-activation', kwargs={'pk': user.id}),
        content_type='application/json'
    )
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.account
@pytest.mark.user
@pytest.mark.user_deactivate
def test_user_deactivate_success(tenant_test_api_client, user):
    response = tenant_test_api_client.delete(
        path=reverse(viewname='v1:my_app.account:users-activation', kwargs={'pk': user.id}),
        content_type='application/json'
    )
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.account
@pytest.mark.user
@pytest.mark.user_passport_change
def test_user_passport_change_success(tenant_test_api_client, user, user_credentials):
    response = tenant_test_api_client.post(
        path=reverse(viewname='v1:my_app.account:users-passport-change', kwargs={'pk': user.id}),
        data={
            'old_password': user_credentials['password'],
            'new_password': '{}_changed'.format(user_credentials['password'])
        },
        content_type='application/json'
    )
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.account
@pytest.mark.user
@pytest.mark.user_add_to_group
def test_user_add_to_group_success(tenant_test_api_client, user, group):
    response = tenant_test_api_client.post(
        path=reverse(viewname='v1:my_app.account:users-add-to-group', kwargs={'pk': user.id}),
        data={
            'group': group.id,
        },
        content_type='application/json'
    )
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.account
@pytest.mark.user
@pytest.mark.user_remove_to_group
def test_user_remove_to_group_success(tenant_test_api_client, user, group):
    user.groups.add(group)
    user.save()
    response = tenant_test_api_client.delete(
        path=reverse(viewname='v1:my_app.account:users-add-to-group', kwargs={'pk': user.id}),
        data={
            'group': group.id,
        },
        content_type='application/json'
    )
    assert response.status_code == 200
