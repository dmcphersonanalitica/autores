from django.contrib.auth.models import User
from django.db import models
from django.forms import model_to_dict

from core import settings


class Autores(models.Model):
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    apellidos = models.CharField(db_column='Apellidos', max_length=50, blank=True, null=True)  # Field name made lowercase.
    correo = models.CharField(db_column='Correo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nombre + " " + self.apellidos

    def toJson(self):
        item = model_to_dict(self, fields=['id', 'nombre', 'apellidos', 'correo'])
        return item

    class Meta:
        managed = False
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        db_table = 'autores'
        ordering = ["id"]
        indexes = [models.Index(fields=['id', 'nombre', 'user', 'correo'])]


class Libros(models.Model):
    titulo = models.CharField(db_column='Titulo', max_length=200, blank=True, null=True)  # Field name made lowercase.
    anticipo = models.DecimalField(db_column='Anticipo', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    pago = models.CharField(db_column='Pago', max_length=100, blank=True, null=True)  # Field name made lowercase.
    genero = models.CharField(db_column='Genero', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ebook = models.CharField(db_column='Ebook', max_length=10, blank=True, null=True)  # Field name made lowercase.
    xciento = models.IntegerField(blank=True, null=True)
    autor = models.ForeignKey('Autores', models.DO_NOTHING, db_column='idautores', blank=True, null=True)

    def __str__(self):
        return self.titulo

    def toJson(self):
        item = model_to_dict(self, fields=['id', 'titulo', 'genero'])
        return item

    class Meta:
        managed = False
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        db_table = 'libros'
        ordering = ["id"]
        indexes = [models.Index(fields=['id', 'titulo', 'genero', 'autor'])]


class Ventas(models.Model):
    idventas = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=15, blank=True, null=True)
    mercado = models.CharField(max_length=50, blank=True, null=True)
    libro = models.ForeignKey('Libros', models.DO_NOTHING, db_column='id', blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    totales = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    reporte = models.IntegerField(db_column='Reporte', blank=True, null=True)  # Field name made lowercase.
    cobrado = models.IntegerField(db_column='Cobrado', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.fecha.__str__() + " --- " + self.libro.titulo

    def toJson(self):
        item = model_to_dict(self, fields=['idventas', 'fecha', 'mercado', 'cantidad', 'precio', 'totales'])

        if self.cobrado == 1:
            item['cobrado'] = 'Si'
        else:
            item['cobrado'] = 'No'

        return item

    class Meta:
        managed = False
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        db_table = 'ventas'
        ordering = ["fecha"]
        indexes = [models.Index(fields=['idventas', 'fecha', 'libro'])]


class Reporteventas(models.Model):
    titulo = models.CharField(db_column='Titulo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    autor = models.CharField(db_column='Autor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isbn = models.CharField(db_column='ISBN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    precioventa = models.DecimalField(db_column='PrecioVenta', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cantidad = models.IntegerField(db_column='Cantidad', blank=True, null=True)  # Field name made lowercase.
    anticipo = models.DecimalField(db_column='Anticipo', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    adeudo = models.DecimalField(db_column='Adeudo', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mercado = models.CharField(db_column='Mercado', max_length=50, blank=True, null=True)  # Field name made lowercase.
    regalias = models.DecimalField(db_column='Regalias', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    totalventas = models.DecimalField(db_column='TotalVentas', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    planpago = models.CharField(db_column='PlanPago', max_length=50, blank=True, null=True)  # Field name made lowercase.
    porciento = models.DecimalField(db_column='Porciento', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    enviado = models.IntegerField(db_column='Enviado', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.fecha.__str__() + " --- " + self.titulo

    def toJson(self):
        item = model_to_dict(self, fields=['id', 'titulo', 'autor', 'fecha'])

        if self.enviado == 1:
            item['enviado'] = 'Si'
        else:
            item['enviado'] = 'No'

        return item

    class Meta:
        managed = False
        verbose_name = "Reporteventa"
        verbose_name_plural = "Reporteventas"
        db_table = 'reporteventas'
        ordering = ["id"]
        indexes = [models.Index(fields=['id', 'fecha', 'titulo'])]
