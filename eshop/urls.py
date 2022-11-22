from django.urls.conf import path
from . import views

app_name="eshop"

urlpatterns = [
    path('', views.eshop, name="eshop"),
    path('login/',views.login_user, name='login'),
    path('customer_user/',views.customer_user,name='customer_user'),
    
    path('logout/',views.logout,name='logout'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    path('<int:id>/', views.view_product, name='view_product'),
    path('customer_user/<int:id>/', views.view_product_log, name='view_product_log'),
    path('customer_registration/', views.customer_registration, 
        name='customer_registration'),
    path('search/', views.search, name='search'),
    


    path('mens_hoodies_list_base_page/',views.mens_hoodies_list_base_page,name='mens_hoodies_list_base_page'),
    path('mens_tshirt_list_base_page/',views.mens_tshirt_list_base_page,name='mens_tshirt_list_base_page'),
    path('mens_jean_list_base_page/',views.mens_jean_list_base_page,name='mens_jean_list_base_page'),
    path('mens_coat_list_base_page/',views.mens_coat_list_base_page,name='mens_coat_list_base_page'),

    path('women_hoodies_list_base_page/',views.women_hoodies_list_base_page,name='women_hoodies_list_base_page'),
    path('women_tshirt_list_base_page/',views.women_tshirt_list_base_page,name='women_tshirt_list_base_page'),
    path('women_jean_list_base_page/',views.women_jean_list_base_page,name='women_jean_list_base_page'),
    path('women_coat_list_base_page/',views.women_coat_list_base_page,name='women_coat_list_base_page'),

    path('mens_hoodies_list/',views.mens_hoodies_list,name='mens_hoodies_list'),
    path('mens_tshirt_list/',views.mens_tshirt_list,name='mens_tshirt_list'),
    path('mens_jean_list/',views.mens_jean_list,name='mens_jean_list'),
    path('mens_coat_list/',views.mens_coat_list,name='mens_coat_list'),

    path('women_hoodies_list/',views.women_hoodies_list,name='women_hoodies_list'),
    path('women_tshirt_list/',views.women_tshirt_list,name='women_tshirt_list'),
    path('women_jean_list/',views.women_jean_list,name='women_jean_list'),
    path('women_coat_list/',views.women_coat_list,name='women_coat_list'),



    
    
       
]