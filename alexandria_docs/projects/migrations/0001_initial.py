# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 23:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import projects.utils
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', verbose_name='slug')),
            ],
            options={
                'verbose_name': 'organization',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=b'title', verbose_name='slug')),
                ('repo', models.CharField(max_length=255, verbose_name='Repository URL')),
                ('project_url', models.URLField(verbose_name='Project url')),
                ('author', models.ForeignKey(help_text='Project author', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('organization', models.ForeignKey(help_text='Project organization', on_delete=django.db.models.deletion.CASCADE, to='projects.Organization', verbose_name='organization')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'project',
            },
        ),
        migrations.CreateModel(
            name='ProjectArchive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('archive', models.FileField(upload_to=projects.utils.projects_upload_to, verbose_name='Archive')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project', verbose_name='project')),
                ('uploaded_by', models.ForeignKey(help_text='Who uploaded the documentation', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='who uploaded')),
            ],
            options={
                'verbose_name': 'project archive',
            },
        ),
    ]