# Generated by Django 3.1.7 on 2022-02-13 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_admingroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(max_length=128, unique=True)),
                ('type', models.CharField(choices=[('private', 'private'), ('group', 'group'), ('supergroup', 'supergroup'), ('channel', 'channel')], max_length=128)),
                ('title', models.CharField(blank=True, max_length=512, null=True)),
                ('username', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='admingroup',
            name='chat_id',
            field=models.ForeignKey(max_length=256, on_delete=django.db.models.deletion.CASCADE, to='product.telegramchat', verbose_name='Чат id'),
        ),
    ]
