from django.urls import path, include

urlpatterns = [
        path('account/', include('my_app.api.v1.account.urls')),
]
