from django.urls import path

from .views import IndexView, BaseView, AboutView, ProductDetailView, CartView, AddToCartView, DelFromCartView, ChangeQTYVIEW, CheckoutView, MakeOrderView, LoginView, RegistrationView, ProfileView

from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('base/', BaseView.as_view(), name='base'),
    path('about', AboutView.as_view(), name='about'),
    path('products/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-card/<str:slug>/', DelFromCartView.as_view(), name='del_from_cart'),
    path('change-qty/<str:slug>/', ChangeQTYVIEW.as_view(), name='change_qty'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order', MakeOrderView.as_view(), name='make_order'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/base'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile')


]
