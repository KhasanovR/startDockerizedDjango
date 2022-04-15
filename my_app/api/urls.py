from django.urls import path, include

urlpatterns = [
        path('v1/', include('my_app.api.v1.urls')),
]
