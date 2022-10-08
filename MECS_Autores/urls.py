from django.urls import path
from MECS_Autores.views import *

app_name = 'mecs'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('sales/list/', VentasListView.as_view(), name='sale_list'),
    path('sales/detail/<int:pk>/', VentasDetailView.as_view(), name='sale_detail'),
    path('sales/invoice/pdf/<int:pk>/', VentasInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    path('sales/mail/<int:pk>/', VentasSendEmail.as_view(), name='sale_mail'),
    #path('sales/mail/<int:pk>/', SendEmail, name='sale_mail'),
]

handler404 = page_404
handler500 = page_500