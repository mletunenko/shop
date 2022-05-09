from django.utils import timezone

from marketplace.models import Sale
from django.contrib.auth.models import User

from shop.celery import app


@app.task()
def email_sender():
    sales = Sale.objects.filter(announcement_date__lte=timezone.now(),
                                end_date__gte=timezone.now(),
                                was_announced=False)
    users = User.objects.filter(is_active=True)
    for sale in sales:
        for user in users:
            with open('shop/announcement.csv', 'a') as file:
                subject = f'{sale.name} is staring!'
                file.write(f'{user.email}, {subject}\n')

        sale.was_announced = True
        sale.save()
