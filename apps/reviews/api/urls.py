from django.urls import path

from . import views

urlpatterns = [
    path("locations/<uuid:location_id>/", views.location_reviews, name="location-reviews"),
    path("locations/<uuid:location_id>/create/", views.create_review, name="review-create"),
    path("reviews/<uuid:review_id>/delete/", views.delete_review, name="review-delete"),
    path("reviews/<uuid:review_id>/", views.update_review, name="update-review"),
]
