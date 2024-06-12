from django.shortcuts import render, get_object_or_404
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework.response import Response
from rest_framework import status

from base.models import (
    Task,
    Driver,
    Truck,
    Order,
    Customer,
    CustomerManager,
    Platform,
    PaymentType
)
from user.models import User
from base.serializers import (
    TaskSerializer,
    OrderSerializer,
)

from datetime import datetime



# ORDERS VIEWS


@api_view(["GET"])
def getOrders(request):
    # Fetch orders with prefetch_related for optimization
    orders = Order.objects.prefetch_related("tasks").all()

    # Prepare a list for serialized orders
    serialized_orders = []

    # Sorting tasks within each order and serialize
    for order in orders:
        # Ensure tasks are sorted; parse strings to datetime if necessary
        sorted_tasks = sorted(
            order.tasks.all(),
            key=lambda task: (
                datetime.strptime(task.start_date, "%Y-%m-%d")
                if isinstance(task.start_date, str)
                else task.start_date,
                datetime.strptime(task.start_time, "%H:%M:%S")
                if isinstance(task.start_time, str)
                else task.start_time,
            ),
        )

        # Use a modified order object or a dictionary to hold sorted tasks
        order_data = OrderSerializer(order).data
        order_data["tasks"] = TaskSerializer(sorted_tasks, many=True).data

        serialized_orders.append(order_data)

    return Response(serialized_orders)


@api_view(["GET"])
def getOrder(request, pk):
    # Fetch order with prefetch_related for optimization
    order = Order.objects.prefetch_related("tasks").get(id=pk)

    # Sorting tasks within the order; parse strings to datetime if necessary
    sorted_tasks = sorted(
        order.tasks.all(),
        key=lambda task: (
            datetime.strptime(task.start_date, "%Y-%m-%d")
            if isinstance(task.start_date, str)
            else task.start_date,
            datetime.strptime(task.start_time, "%H:%M:%S")
            if isinstance(task.start_time, str)
            else task.start_time,
        ),
    )

    # Serialize order and manually insert serialized, sorted tasks
    order_data = OrderSerializer(order).data
    order_data["tasks"] = TaskSerializer(sorted_tasks, many=True).data

    return Response(order_data)


@api_view(["POST"])
def createOrder(request):
    data = request.data
    user_id = data.get("user")
    customer_name = data.get("customer")
    customer_manager_name = data.get("customer_manager")
    truck_plates = data.get("truck")
    driver_name = data.get("driver")
    platform_name = data.get("platform")
    payment_type_name = data.get("payment_type")

    user = User.objects.get(id=user_id) if user_id else None
    platform = Platform.objects.filter(name=platform_name).first() if platform_name else None
    payment_type = PaymentType.objects.filter(name=payment_type_name).first() if payment_type_name else None
    customer = (
        Customer.objects.filter(name=customer_name).first() if customer_name else None
    )
    customer_manager = (
        CustomerManager.objects.filter(full_name=customer_manager_name).first()
        if customer_manager_name
        else None
    )

    truck = Truck.objects.filter(plates=truck_plates).first() if truck_plates else None
    driver = (
        Driver.objects.filter(full_name=driver_name).first() if driver_name else None
    )

    data["user"] = user
    data["platform"] = platform
    data["payment_type"] = payment_type
    data["customer"] = customer
    data["customer_manager"] = customer_manager
    data["truck"] = truck
    data["driver"] = driver

    # order = Order(customer=customer, customer_manager=customer_manager, truck=truck, driver=driver, **data)
    order = Order(**data)
    order.save()

    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
def editOrder(request, pk):
    order = get_object_or_404(Order, id=pk)
    print("Request data: ", request.data)
    serializer = OrderSerializer(instance=order, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    print("Serialized Data", serializer.data)
    return Response(serializer.data)


@api_view(["DELETE"])
def deleteOrder(request, pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        message = {"detail": "Order does not exist"}
        return Response(message, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order, many=False)
    orderData = serializer.data

    order.delete()

    # Optionally return the data of the deleted order
    message = {"detail": "Order deleted successfully", "data": orderData}
    return Response(message)

