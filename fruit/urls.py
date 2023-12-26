
from django.contrib import admin
from django.urls import path,include

from django.conf import settings # --------> this
from django.conf.urls.static import static
from myfruit.models import contactmodel

from myfruit.views import Add_to_cartView, Add_to_wishlistView, AllproductView, ChangePassView, CheckoutView, ClearcartView, ClearwishlistView, CustomerAddressView, HomeView, Minusquantity, ProfileView, SignupView,SigninView, UpdateaddressView, cartview, changequantity, contactview, deleteaddressview, deleteview, deletewishlishview, logoutView, orderview, serchview, wishlistview

from django.conf import settings # --------> this
from django.conf.urls.static import static# --------> this


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',HomeView),
    path('signup/',SignupView),
    path('signin/',SigninView),
    path('logout/',logoutView),
    path('chpass/',ChangePassView),
    path('profile/',ProfileView),
    path('cart/',cartview),
    path('addtocart/<int:id>/',Add_to_cartView),
    path('deletecart/<int:id>/',deleteview),
    path('changequantity/<int:id>/',changequantity),
    path('minusquantity/<int:id>/',Minusquantity),
    path('clearcart/',ClearcartView),
    path('addwish/<int:id>/',Add_to_wishlistView),
    path('wishlist/',wishlistview),
    path('deletewishlist/<int:id>/',deletewishlishview),
    path('clear/',ClearwishlistView),
    path('address/',CustomerAddressView),
    path('Addressdelete/<int:id>/',deleteaddressview),
    path('Addressupdate/<int:id>/',UpdateaddressView),
    path('allproduct/',AllproductView),
    path('checkout/',CheckoutView),
    path('orders/',orderview),
    path('contact/',contactview),
    path('searched/',serchview)
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # --------> this

