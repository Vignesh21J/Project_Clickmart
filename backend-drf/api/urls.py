from django.urls import path
from users import views as UserViews

from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from products import views as ProductViews

from carts import views as CartViews


urlpatterns = [
    path('register/', UserViews.RegisterView.as_view()),

    # User APIs
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserViews.ProfileView.as_view()),

    # Product APIs
    
    # product list
    path('products/', ProductViews.ProductListView.as_view()),

    # product detail
    path('products/<int:pk>/', ProductViews.ProductDetailView.as_view()),

    
    # Cart APIs
    path('cart/', CartViews.CartView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)