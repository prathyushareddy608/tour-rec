import imp
from django.contrib import admin
from django.urls import path
from qrscan import views
from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers
from django.contrib.auth.views import LogoutView  
from django.conf.urls.static import static
from django.conf import settings
from qrscan import payment
from qrscan import views as qrscan_views
# from qrscan import tour_views as tour_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', payment.book,name="homepage"),
    path('', views.homepage,name="home"),
    path('scan/<monuments>/', qrscan_views.ScanQR, name='scan'),
    path('Call_Scan/<monuments>/', qrscan_views.Call_Scan, name='Call_Scan'),
    path('payment-status', payment.payment_status, name='payment-status'),
    path("logout/",LogoutView.as_view(next_page="react_app"),name="logout"),
    path('Ticket/',views.Ticket_display,name='ticket'),
    path('display/<monuments>/',views.display,name='display'),
    path("react", views.MyReactView.as_view(), name='react_app'),
    path('select/', qrscan_views.selectMonument, name='selectMonument'),  
    path('cancel-booking/', views.cancel_booking, name='cancel_booking'),
    # this route catches any url below the main one, so the path can be passed to the front end
    path(r'react/<path:path>', views.MyReactView.as_view(), name='react_app_with_path'),
    path('lcd_display/', qrscan_views.lcd_display, name='lcd_display'),
    path('tour-recommendation/', views.tour_recommendation_view, name='tour_recommendation'),
    path('destination-overview/<int:pk>/', views.destination_overview, name='destination_overview'),
    path('book-destination/<int:pk>/', views.book_destination_view, name='book_destination'),
    path('all-destinations/', views.all_destinations, name='all_destinations'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)