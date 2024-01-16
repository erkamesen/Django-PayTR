# Generated by Django 4.2 on 2024-01-13 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('food', '0003_alter_cart_user'),
        ('users', '0002_remove_profile_location_profile_is_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=7)),
                ('is_paid', models.BooleanField(default=False)),
                ('order_state', models.CharField(choices=[('Ödeme Bekliyor', 'Ödeme Bekliyor'), ('Hazırlanıyor', 'Hazırlanıyor'), ('Yolda', 'Yolda'), ('Teslim Edildi', 'Teslim Edildi')], default='Ödeme Bekliyor', max_length=20)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]