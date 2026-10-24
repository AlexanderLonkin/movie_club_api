from random import randrange

from .models import Opinion


def random_opinion():
    """Вернуть случайное мнение из базы или None, если база пуста."""
    quantity = Opinion.query.count()
    if quantity:
        offset_value = randrange(quantity)
        opinion = Opinion.query.offset(offset_value).first()
        return opinion
