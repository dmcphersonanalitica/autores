import requests
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.db.models import Sum, FloatField, Q
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, TemplateView, View, FormView

from Login.mixins import IsSuperuserMixin
from MECS_Autores.forms import EmailForm
from MECS_Autores.models import Ventas, Libros, Autores, Reporteventas
from core.settings import STATIC_URL
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime

month = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
         'Noviembre', 'Diciembre']


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def graph_sales_five_year(self):
        try:
            data = []
            year = self.graph_five_year()
            libros = Libros.objects.filter(autor_id=self.request.user.autores.id)

            for i in libros:
                data_value = []
                for m in year:
                    cantidad = 0
                    cantidad += Ventas.objects.filter(libro_id=i.id, fecha__year=m, estado='ACTIVO',
                                                      cobrado=1).aggregate(
                        c=Coalesce(Sum('cantidad'), 0)).get('c')
                    data_value.append(cantidad)
                data.append([i.titulo, data_value])
        except Exception as e:
            data['error'] = str(e)
        return data

    def graph_five_year(self):
        try:
            data = []
            year = self.last_ventas().year
            for m in range(4, -1, -1):
                data.append(year - m)
        except Exception as e:
            data['error'] = str(e)
        return data

    def graph_sales_month_last_year(self):
        try:
            data = []
            year = self.last_ventas().year
            libros = Libros.objects.filter(autor_id=self.request.user.autores.id)
            total_general = self.total_ventas()

            if len(libros) > 0:
                for m in range(1, 13):
                    total = 0
                    for i in libros:
                        total += Ventas.objects.filter(libro_id=i.id, fecha__year=year, fecha__month=m, estado='ACTIVO',
                                                       cobrado=1).only(
                            'totales').aggregate(t=Coalesce(
                            Sum('totales'), 0, output_field=FloatField())).get('t')
                    if total > 0:
                        porciento = total * float(100) / float(total_general)
                    else:
                        porciento = 0
                    data.append([month[m - 1], float(porciento)])
        except Exception as e:
            data['error'] = str(e)
        return data

    def graph_sales_month_last_year_general(self):
        try:
            data = []
            year = self.last_ventas().year
            total_general = self.total_ventas()

            for m in range(1, 13):
                total = 0
                total += Ventas.objects.filter(fecha__year=year, fecha__month=m, estado='ACTIVO', cobrado=1).only(
                    'totales').aggregate(t=Coalesce(
                    Sum('totales'), 0, output_field=FloatField())).get('t')
                porciento = total * float(100) / float(total_general)
                data.append([month[m - 1], float(porciento)])
        except Exception as e:
            data['error'] = str(e)
        return data

    def graph_gender_general(self):
        generos = Libros.objects.order_by('genero').values_list('genero', flat=True).distinct()

        return generos

    def graph_gender_five_year(self):
        try:
            data = []
            years = self.graph_five_year()
            generos = self.graph_gender_general()
            for g in generos:
                data_temp = []
                total_sum = 0
                for y in years:
                    total = 0
                    total += Ventas.objects.filter(libro__genero=g, fecha__year=y, estado='ACTIVO',
                                                   cobrado=1).aggregate(
                        c=Coalesce(Sum('cantidad'), 0)).get('c')
                    data_temp.append(total)
                    total_sum += total
                data.append([g, data_temp, total_sum])
            data = sorted(data, key=lambda gender: gender[2], reverse=True)
        except Exception as e:
            pass
        return data[:3]

    def count_libros(self):
        if self.request.user.is_superuser:
            libros = Libros.objects.all().only('id').count()
            return libros

        libros = Libros.objects.filter(autor_id=self.request.user.autores.id).only('id').count()
        return libros

    def count_autores(self):
        autores = Autores.objects.all().only('id').count()
        return autores

    def count_ventas(self):
        if self.request.user.is_superuser:
            ventas = Ventas.objects.filter(estado='ACTIVO', cobrado=1).only('idventas').count()
            return ventas

        libros = Libros.objects.filter(autor_id=self.request.user.autores.id).only('id')
        ventas = 0
        for i in libros:
            ventas += Ventas.objects.filter(libro_id=i.id, estado='ACTIVO', cobrado=1).only('idventas').count()
        return ventas

    def count_libros_ventas(self):
        if not self.request.user.is_superuser:
            libros = Libros.objects.filter(autor_id=self.request.user.autores.id).only('id')
            total = 0
            for i in libros:
                total += Ventas.objects.filter(libro_id=i.id, estado='ACTIVO', cobrado=1).aggregate(
                    c=Coalesce(Sum('cantidad'), 0)).get('c')
        return total

    def last_ventas(self):
        if not self.request.user.is_superuser:
            libros = Libros.objects.filter(autor_id=self.request.user.autores.id).only('id')
            if len(libros) > 0:
                ventas = Ventas.objects.filter(libro_id=libros.first().id, estado='ACTIVO', cobrado=1)
                if len(ventas) > 0:
                    last = Ventas.objects.filter(libro_id=libros.first().id, estado='ACTIVO', cobrado=1).first().fecha
                    for i in libros:
                        for j in Ventas.objects.filter(libro_id=i.id, estado='ACTIVO', cobrado=1):
                            if last < j.fecha:
                                last = j.fecha
                    return last
                else:
                    return date.today()
            else:
                return date.today()
        else:
            venta = Ventas.objects.filter(estado='ACTIVO', cobrado=1).only('fecha').order_by('fecha').last()
            last = venta.fecha
            return last

    def total_ventas(self):
        if self.request.user.is_superuser:
            total = Ventas.objects.filter(estado='ACTIVO', cobrado=1).only('totales').aggregate(
                t=Coalesce(Sum('totales'), 0, output_field=FloatField(.02))).get('t')
            return total

        libros = Libros.objects.filter(autor_id=self.request.user.autores.id).only('id')
        total = 0
        if len(libros) > 0:
            for i in libros:
                total += Ventas.objects.filter(libro_id=i.id, estado='ACTIVO', cobrado=1).only('totales').aggregate(
                    t=Coalesce(Sum('totales'), 0, output_field=FloatField(.02))).get('t')
        return total

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        context['action'] = 'get_graph_sales_year_month'
        if hasattr(self.request.user, 'autores') or self.request.user.is_superuser:
            context['book'] = self.count_libros()
            context['sales'] = self.count_ventas()
            context['total'] = self.total_ventas()
        else:
            context['book'] = 0
            context['sales'] = 0
            context['total'] = 0
        context['writer'] = self.count_autores()
        if not self.request.user.is_superuser and hasattr(self.request.user, 'autores') and self.count_ventas() > 0:
            context['sales_libros'] = self.count_libros_ventas()
        context['last_sale'] = self.last_ventas()
        context['father'] = 'dashboard'
        if hasattr(self.request.user, 'autores'):
            context['graph_sales_five_year'] = self.graph_sales_five_year()
            context['graph_five_year'] = self.graph_five_year()
            context['graph_sales_month_last_year'] = self.graph_sales_month_last_year()
        if self.request.user.is_superuser:
            context['graph_five_year'] = self.graph_five_year()
            context['graph_sales_month_last_year_general'] = self.graph_sales_month_last_year_general()
            context['graph_gender_five_year'] = self.graph_gender_five_year()
        return context


class VentasListView(LoginRequiredMixin, ListView):
    model = Ventas
    template_name = "list.html"

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = []
        try:
            action = request.POST['action']
            if action == 'list':
                position = 1
                if request.user.is_superuser:
                    ventas = Ventas.objects.filter(estado='ACTIVO').select_related('libro')
                    for i in ventas:
                        item = i.toJson()
                        item['libro'] = i.libro.titulo
                        date = month[i.fecha.month - 1] + ' ' + i.fecha.strftime('%Y')
                        item['fecha_format'] = date
                        data.append(item)
                else:
                    if hasattr(request.user, 'autores'):
                        libros = Libros.objects.filter(autor_id=request.user.autores.id)
                        for i in libros:
                            ventas = Ventas.objects.filter(libro_id=i.id, estado='ACTIVO').select_related('libro')
                            for j in ventas:
                                item = j.toJson()
                                item['libro'] = j.libro.titulo
                                date = month[j.fecha.month - 1] + ' ' + j.fecha.strftime('%Y')
                                item['fecha_format'] = date
                                data.append(item)
                        data = sorted(data, key=lambda venta: venta['fecha'])
                for d in data:
                    d['position'] = position
                    position += 1
            else:
                data['error'] = '¡Ha ocurrido un error!'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de ventas'
        context['action'] = 'list'
        context['father'] = 'sale'
        return context


class VentasDetailView(LoginRequiredMixin, DetailView):
    model = Ventas
    template_name = "detail.html"

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        id = self.get_object().libro.autor.user.id
        if self.request.user.id == id or self.request.user.is_superuser:
            self.object = self.get_object()
        else:
            return redirect('mecs:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def generate_request(self, url, params={}):
        try:
            response = requests.get(url, verify=False)

            if response.status_code == 200:
                return response.json()
        except Exception as ex:
            pass

    def get_book_image(self, params={}):
        countBlankSpace = self.object.libro.titulo.count(' ')
        lowerNames = self.object.libro.titulo.lower().replace(' ', '-', countBlankSpace)

        response = self.generate_request(
            'https://dmcphersoneditorial.com:3001/api/product/frontend/lower-title?lowerTitle=' +
            lowerNames, params)
        if response:
            imageUrl = response.get('picture_address')
            return imageUrl

        return '{}{}'.format(STATIC_URL, 'image/Book.jpg')

    def get_date(self):
        month = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
                 'Noviembre', 'Diciembre']
        date = month[self.object.fecha.month - 1] + ' ' + self.object.fecha.strftime('%Y')
        return date

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle de venta'
        context['action'] = 'detail'
        context['listUrl'] = reverse_lazy('mecs:sale_list')
        context['imageUrl'] = self.get_book_image()
        context['fecha'] = self.get_date()
        context['father'] = 'sale'
        return context


class ReporteVentasListView(LoginRequiredMixin, ListView):
    model = Reporteventas
    template_name = "relist.html"

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = []
        try:
            action = request.POST['action']
            if action == 'list':
                position = 1
                if request.user.is_superuser:
                    reportes = Reporteventas.objects.all()
                    for i in reportes:
                        item = i.toJson()
                        date = month[i.fecha.month - 1] + ' ' + i.fecha.strftime('%Y')
                        item['fecha_format'] = date
                        data.append(item)
                else:
                    if hasattr(request.user, 'autores'):
                        libros = Libros.objects.filter(autor_id=request.user.autores.id)
                        for i in libros:
                            reportes = Reporteventas.objects.filter(
                                Q(titulo=i.titulo) | Q(autor__contains=i.autor.nombre and i.autor.apellidos))
                            for j in reportes:
                                item = j.toJson()
                                date = month[j.fecha.month - 1] + ' ' + j.fecha.strftime('%Y')
                                item['fecha_format'] = date
                                data.append(item)
                        data = sorted(data, key=lambda reporte: reporte['fecha'])
                for d in data:
                    d['position'] = position
                    position += 1
            else:
                data['error'] = '¡Ha ocurrido un error!'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de reportes'
        context['action'] = 'list'
        context['father'] = 'report'
        return context


class ReporteVentasInvoicePdfView(LoginRequiredMixin, View):
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            data = []
            report = Reporteventas.objects.get(pk=self.kwargs['pk'])
            template = get_template('invoice.html')
            context = {
                'report': report,
                'logo': '{}{}'.format(settings.STATIC_URL, 'image/1.png'),
                'confirm': '{}{}'.format(settings.STATIC_URL, 'image/2.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response[
                'Content-Disposition'] = 'attachment; filename="' + report.titulo + ' -- ' + report.fecha.strftime(
                '%B %Y') + '.pdf"'
            pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response

        except Exception as ex:
            data['error'] = str(ex)
            return data
        return HttpResponseRedirect(reverse_lazy('mecs:dashboard'))


class ReporteVentasSendEmail(LoginRequiredMixin, IsSuperuserMixin, FormView):
    form_class = EmailForm
    template_name = 'mail.html'
    success_url = reverse_lazy('mecs:report_list')
    url_redirect = reverse_lazy('mecs:report_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                path + ' -- ' + uri + 'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        report = Reporteventas.objects.get(pk=kwargs['pk'])
        libros = Libros.objects.filter(titulo=report.titulo).select_related('autor')
        librosList = list(libros)
        if len(librosList) > 0:
            to = librosList[0].autor.correo
        else:
            to = ''
        month = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
                 'Noviembre', 'Diciembre']
        date = month[report.fecha.month - 1] + ' ' + report.fecha.strftime('%Y')
        initial_data = {'to': to, 'asunto': 'Nuevo reporte de pago.', 'mensaje': 'Estimado escritor: \n'
                                                                                 'Cumpliendo con lo establecido y '
                                                                                 'pactado en nuestro contrato, '
                                                                                 'nuestra editorial se complace en '
                                                                                 'enviarle el reporte de venta '
                                                                                 'correspondiente a la fecha '
                                                                                 + date + ' del libro '
                                                                                 + report.titulo +
                                                                                 '. Agradecemos una vez más su '
                                                                                 'presencia en nuestro catálogo. '
                                                                                 'Esperamos su acuse de recibo. '
                                                                                 '\nLe saluda cordialmente el equipo '
                                                                                 'de D´McPherson Editorial. '
                                                                                 '\nPD: Para revisar el archivo '
                                                                                 'adjunto debe hacerlo desde una '
                                                                                 'Computadora o Laptop.'}
        form = EmailForm(initial=initial_data)

        return render(request, 'mail.html', {'form': form})

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.method == 'POST':
                form = EmailForm(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    email = EmailMessage(cd['asunto'], cd['mensaje'],
                                         'Editorial D\'McPherson <contabilidad@dmcphersoneditorial.com>',
                                         [cd['to']])
                    file = self.Invoice_PDF(self.kwargs['pk'])
                    report = Reporteventas.objects.get(pk=self.kwargs['pk'])
                    report.enviado = 1
                    email.attach_file(file)
                    email.send()
                    report.save()
                    data['listUrl'] = reverse_lazy('mecs:report_list')
        except Exception as ex:
            data['error'] = str(ex)
        return JsonResponse(data)

    def Invoice_PDF(self, id):
        report = Reporteventas.objects.get(pk=id)
        template = get_template('invoice.html')
        context = {
            'report': report,
            'logo': '{}{}'.format(settings.STATIC_ROOT, '/image/1.png'),
            'confirm': '{}{}'.format(settings.STATIC_ROOT, '/image/2.png')
        }
        html = template.render(context)

        outputFilename = '{}{}'.format(settings.STATIC_ROOT, '/pdf/Reporte de venta.pdf')
        resultFile = open(outputFilename, "w+b")
        pisa.CreatePDF(html, dest=resultFile, link_callback=self.link_callback)
        resultFile.close()
        return outputFilename


# 404: página no encontrada
def page_404(request, exception):
    nombre_template = '404.html'

    return render(request, template_name=nombre_template, status=400)


# 500: error en el servidor
def page_500(request):
    nombre_template = '500.html'

    return render(request, template_name=nombre_template, status=500)
