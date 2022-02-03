import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from orders.forms import OrderForm
from orders.models import Order, Payment


# Create your views here.


class PlaceOrderView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        if not request.cart:
            return redirect('store')
        else:
            return render(request, 'orders/payments.html')

    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = request.user
            for f in form.fields.keys():
                data.__setattr__(f, form.cleaned_data[f])
            data.order_total = request.cart.grand_total()
            data.tax = request.cart.tax()
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # generate order_id based on pk
            today = datetime.date.today().strftime('%Y%m%d')
            data.order_number = f'{today}-{data.pk}'
            data.save()
            return render(request, 'orders/payments.html', {
                'order': data
            })
        else:
            redirect('checkout')


class PaymentsView(LoginRequiredMixin, View):
    login_url = '/accounts/login'

    def get(self, request):
        return render(request, 'orders/payments.html')

    def post(self, request):
        order_id = request.POST.get('order_id')
        circuit_payment_id = request.POST.get('circuit_payment_id')
        payment_method = request.POST.get('payment_method')

        order = Order.objects.get(pk=order_id)
        order.status = "Accepted"
        order.is_ordered = True

        payment = Payment()
        payment.user = request.user
        payment.payment_id = f'PAYPAL-{circuit_payment_id}'
        payment.payment_method = payment_method
        payment.amount_paid = request.cart.grand_total()
        payment.status = 'Completed'

        payment.save()
        order.payment = payment
        order.save()

        cart = request.cart

        for cart_item in request.cart.cart_items.all():
            qty = cart_item.quantity
            cart_item.product.decrease_availability(qty)

        cart.status = 'completed'
        cart.save()

        return render(request, 'orders/order_complete.html', {
            "order": order,
            "payment": payment,
            "order_cart": cart

        })
