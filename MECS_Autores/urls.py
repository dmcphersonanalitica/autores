from django.urls import path
from MECS_Autores.views import *

app_name = 'mecs'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('sales/list/', VentasListView.as_view(), name='sale_list'),
    path('sales/detail/<int:pk>/', VentasDetailView.as_view(), name='sale_detail'),
    path('reports/list/', ReporteVentasListView.as_view(), name='report_list'),
    path('reports/invoice/pdf/<int:pk>/', ReporteVentasInvoicePdfView.as_view(), name='report_invoice_pdf'),
    path('reports/mail/<int:pk>/', ReporteVentasSendEmail.as_view(), name='report_mail'),
]

handler404 = page_404
handler500 = page_500