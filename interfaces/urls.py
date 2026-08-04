"""The address book: which URL runs which view."""

from django.urls import path

from interfaces.views import ProposeCandidates, RequestList, SpecialistList

urlpatterns = [
    path("specialists/", SpecialistList.as_view()),
    path("requests/", RequestList.as_view()),
    path("requests/<int:pk>/propose/", ProposeCandidates.as_view()),
]
