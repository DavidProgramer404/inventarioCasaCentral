from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='hora_recibida',
            new_name='hora_salida',
        ),
        migrations.AlterField(
            model_name='producto',
            name='hora_salida',
            field=models.TimeField(verbose_name='Hora de salida'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='hora_llegada',
            field=models.TimeField(verbose_name='Hora de llegada'),
        ),
    ]