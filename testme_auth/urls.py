from rest_framework import routers

from . import views

app_name = 'testme_auth'

router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)
