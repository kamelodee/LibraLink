from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import AuthorViewSet, BookViewSet, FavoriteViewSet, ShelfViewSet, WorkViewSet
from users.views import LoginView, RegisterView, UserViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorite')

router.register(r'users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
   path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

]




