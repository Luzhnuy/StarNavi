# Generated by Django 2.1.7 on 2019-03-27 18:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete='CASCADE', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete='CASCADE', related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
