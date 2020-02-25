from rest_framework import routers

from .viewsets import AccountViewset

router = routers.SimpleRouter()
router.register(r"accounts", AccountViewset)
