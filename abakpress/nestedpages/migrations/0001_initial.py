# Generated by Django 3.1.6 on 2021-02-06 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(db_index=True, max_length=100, verbose_name='URL')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='name')),
                ('head', models.CharField(max_length=200, verbose_name='title')),
                ('content', models.TextField(blank=True, verbose_name='content')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nestedpages.page')),
            ],
        ),
    ]
