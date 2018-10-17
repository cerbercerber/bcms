from rest_framework import routers
from fo.viewsets import EleveViewSet

router = routers.DefaultRouter()
router.register(r'eleve', EleveViewSet)