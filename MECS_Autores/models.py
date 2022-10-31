from django.contrib.auth.models import User
from django.db import models
from django.forms import model_to_dict

from core import settings


class Autores(models.Model):
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    apellidos = models.CharField(db_column='Apellidos', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # seudonimo = models.CharField(db_column='Seudonimo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # ci = models.CharField(db_column='CI', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # telefono = models.BigIntegerField(db_column='Telefono', blank=True, null=True)  # Field name made lowercase.
    # fechanacimiento = models.DateField(db_column='FechaNacimiento', blank=True, null=True)  # Field name made lowercase.
    # nopasaporte = models.CharField(db_column='NoPasaporte', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # direccion = models.CharField(db_column='Direccion', max_length=200, blank=True, null=True)  # Field name made lowercase.
    # direccion2 = models.CharField(db_column='Direccion2', max_length=200, blank=True, null=True)  # Field name made lowercase.
    correo = models.CharField(db_column='Correo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # tarjetab = models.BigIntegerField(db_column='TarjetaB', blank=True, null=True)  # Field name made lowercase.
    # tarjetamlc = models.BigIntegerField(db_column='TarjetaMLC', blank=True, null=True)  # Field name made lowercase.
    # cuentabancaria = models.CharField(db_column='CuentaBancaria', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # autobiografia = models.TextField(db_column='Autobiografia', blank=True, null=True)  # Field name made lowercase.
    # fechacreado = models.DateField(db_column='FechaCreado', blank=True, null=True)  # Field name made lowercase.
    # usuariocreado = models.CharField(db_column='UsuarioCreado', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # fechaeditado = models.DateField(db_column='FechaEditado', blank=True, null=True)  # Field name made lowercase.
    # usuarioeditado = models.CharField(db_column='UsuarioEditado', max_length=100, blank=True, null=True)  # Field name made lowercase.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nombre + " " + self.apellidos

    def toJson(self):
        item = model_to_dict(self)
        return item

    class Meta:
        managed = False
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        db_table = 'autores'
        ordering = ["id"]
        indexes = [models.Index(fields=['id', 'nombre', 'user', 'correo'])]


class Libros(models.Model):
    # isbn = models.CharField(db_column='ISBN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    titulo = models.CharField(db_column='Titulo', max_length=200, blank=True, null=True)  # Field name made lowercase.
    # subtitulo = models.CharField(db_column='Subtitulo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # autor = models.CharField(db_column='Autor', max_length=100, blank=True, null=True)  # Field name made lowercase.
    anticipo = models.DecimalField(db_column='Anticipo', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    pago = models.CharField(db_column='Pago', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # inedito = models.CharField(db_column='Inedito', max_length=10, blank=True, null=True)  # Field name made lowercase.
    genero = models.CharField(db_column='Genero', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # sinopsis = models.TextField(db_column='Sinopsis', blank=True, null=True)  # Field name made lowercase.
    # notificacion = models.DateField(db_column='Notificacion', blank=True, null=True)  # Field name made lowercase.
    # ilustrador = models.CharField(db_column='Ilustrador', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # editor = models.CharField(db_column='Editor', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # produccion = models.DecimalField(db_column='Produccion', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    # venta = models.DecimalField(db_column='Venta', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    # iva = models.DecimalField(db_column='IVA', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    # vendidos = models.IntegerField(db_column='Vendidos', blank=True, null=True)  # Field name made lowercase.
    # ideditores = models.ForeignKey('Editores', models.DO_NOTHING, db_column='ideditores', blank=True, null=True)
    # numeroc = models.CharField(db_column='NumeroC', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # nombrec = models.CharField(db_column='NombreC', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # encuadernacion = models.CharField(db_column='Encuadernacion', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # alto = models.DecimalField(db_column='Alto', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    # ancho = models.DecimalField(db_column='Ancho', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    # grosor = models.DecimalField(db_column='Grosor', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    # peso = models.DecimalField(db_column='Peso', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    # paginas = models.IntegerField(db_column='Paginas', blank=True, null=True)  # Field name made lowercase.
    # noedicion = models.IntegerField(db_column='NoEdicion', blank=True, null=True)  # Field name made lowercase.
    # fechap = models.DateField(db_column='FechaP', blank=True, null=True)  # Field name made lowercase.
    ebook = models.CharField(db_column='Ebook', max_length=10, blank=True, null=True)  # Field name made lowercase.
    # texto = models.CharField(db_column='Texto', max_length=10, blank=True, null=True)  # Field name made lowercase.
    # adeudo = models.DecimalField(db_column='Adeudo', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    # amazonisbn = models.CharField(db_column='AmazonISBN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # asin = models.CharField(db_column='ASIN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # multiautor = models.IntegerField(db_column='MultiAutor', blank=True, null=True)  # Field name made lowercase.
    # fechafirma = models.DateField(db_column='FechaFirma', blank=True, null=True)  # Field name made lowercase.
    xciento = models.IntegerField(blank=True, null=True)
    autor = models.ForeignKey('Autores', models.DO_NOTHING, db_column='idautores', blank=True, null=True)
    # idilustradores = models.ForeignKey('Ilustradores', models.DO_NOTHING, db_column='idilustradores', blank=True, null=True)
    # fechacreado = models.DateField(db_column='FechaCreado', blank=True, null=True)  # Field name made lowercase.
    # usuariocreado = models.CharField(db_column='UsuarioCreado', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # fechaeditado = models.DateField(db_column='FechaEditado', blank=True, null=True)  # Field name made lowercase.
    # usuarioeditado = models.CharField(db_column='UsuarioEditado', max_length=100, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.titulo

    def toJson(self):
        item = model_to_dict(self)
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
    # fechacreado = models.DateField(db_column='FechaCreado', blank=True, null=True)  # Field name made lowercase.
    # usuariocreado = models.CharField(db_column='UsuarioCreado', max_length=100, blank=True, null=True)  # Field name made lowercase.
    # fechaeditado = models.DateField(db_column='FechaEditado', blank=True, null=True)  # Field name made lowercase.
    # usuarioeditado = models.CharField(db_column='UsuarioEditado', max_length=100, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.fecha.__str__() + " --- " + self.libro.titulo

    def Cobrado(self):
        if self.cobrado == 1:
            return "Si"
        return "No"

    def Reporte(self):
        if self.reporte == 1:
            return "Si"
        return "No"

    def toJson(self):
        item = model_to_dict(self)
        #item['fecha'] = self.fecha.strftime('%B %Y')
        item['cobrado'] = self.Cobrado()
        item['reporte'] = self.Reporte()
        item['libro'] = self.libro.titulo
        return item

    class Meta:
        managed = False
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        db_table = 'ventas'
        ordering = ["fecha"]
        indexes = [models.Index(fields=['idventas', 'fecha', 'libro'])]
