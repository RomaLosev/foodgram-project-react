from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import IngredientsViewSet, RecipeViewSet, TagsViewSet

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
]
