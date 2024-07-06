from rest_framework.routers import SimpleRouter

from .views import JournalEntryViewSet

router = SimpleRouter()
router.register("", JournalEntryViewSet, basename="journal_entries")

urlpatterns = router.urls
