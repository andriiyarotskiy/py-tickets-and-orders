import datetime
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from services.movie_session import get_movie_session_by_id

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.datetime = None
) -> None:
    user = get_user_model().objects.get(username=username)
    new_order = Order.objects.create(user=user)

    if date is not None:
        new_order.created_at = date
        new_order.save(update_fields=["created_at"])

    for ticket in tickets:
        session = get_movie_session_by_id(ticket["movie_session"])
        Ticket.objects.create(
            order=new_order,
            movie_session=session,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
