"""The address book: which URL runs which view."""

from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from interfaces.views import ProposeCandidates, RequestList, SpecialistList

urlpatterns = [
    path("specialists/", SpecialistList.as_view()),
    path("requests/", RequestList.as_view()),
    path("requests/<int:pk>/propose/", ProposeCandidates.as_view()),
    # The API's own documentation: schema = machine-readable, docs = human page.
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
