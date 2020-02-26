from rest_framework import routers

from .viewsets import AdviceViewSet

router = routers.SimpleRouter()
router.register(r"advices", AdviceViewSet)
