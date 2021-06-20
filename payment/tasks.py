from myshop import celery
from io import BytesIO
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@celery.app.task
def payment_completed(order_id):
    order = Order.objects.get(id=order_id)
    subject = f"My shop - EE Invoice no. {order.id}"
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject=subject, body=message, from_email='admin@myshop.com', to=[order.email])
    html = render_to_string('orders/order/pdf.html', context={"order": order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML().write_pdf(out, stylesheets=stylesheets)

    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    email.send()
