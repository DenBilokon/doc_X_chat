# Generated by Django 4.2.6 on 2023-10-08 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat_llm', '0002_userdata_customprofile_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='pdf_document',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chat_llm.pdfdocument'),
        ),
    ]
