# Generated by Django 3.2.9 on 2022-10-17 21:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bids_category_comments_listings'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='wishlist', to=settings.AUTH_USER_MODEL),
        ),
    ]