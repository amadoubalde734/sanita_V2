import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametrage_general', '0002_direction'),
    ]

    operations = [
        migrations.AddField(
            model_name='departement',
            name='direction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='departements', to='parametrage_general.direction', verbose_name='Direction'),
        ),
    ]