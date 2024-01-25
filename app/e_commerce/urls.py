from django.urls import path, include
from e_commerce import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('register', views.RegisterViewSet)
router.register('product', views.ProductViewSet)
router.register('review', views.ReviewViewSet)
router.register('category', views.CategoryViewSet)
router.register('cart', views.CartViewSet)
router.register('cart_item', views.CartItemViewSet)
router.register('image', views.ImageViewSet)
router.register('color', views.ColorViewSet)
router.register('size', views.SizeViewSet)
router.register('quantity', views.QuantityViewSet)
router.register('checked_cart', views.CheckedCartViewSet)
router.register('checked_cart_item', views.CheckedCartItemViewSet)

urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls)),
]
