# Generated by Django 5.1.5 on 2025-06-27 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chandana', '0010_alter_student_phonenumber_alter_student_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='password',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
