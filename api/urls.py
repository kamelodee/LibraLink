from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import AuthorViewSet, BookViewSet, FavoriteViewSet, ShelfViewSet, WorkViewSet
from users.views import UserRegistrationView, UserDetailView

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router = DefaultRouter()
router.register(r'works', WorkViewSet)
router.register(r'shelves', ShelfViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
]

