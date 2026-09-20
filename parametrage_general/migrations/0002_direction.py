from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parametrage_general', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('actif', models.BooleanField(default=True)),
                ('slug', models.SlugField(blank=True, max_length=191, unique=True)),
                ('nom', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Direction',
                'verbose_name_plural': 'Directions',
                'db_table': 'directions',
            },
        ),
    ]