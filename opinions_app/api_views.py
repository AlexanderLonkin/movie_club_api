from flask import jsonify, request

from . import app, db
from .models import Opinion
from .views import random_opinion


@app.route('/api/opinions/', methods=['GET'])
def get_opinions():
    """Вернуть список мнений с необязательным фильтром по названию.

    Фильтр title ищет подстроку без учёта регистра. Ответ содержит JSON
    с ключом opinions и HTTP-статус 200.
    """
    title = request.args.get('title')
    if title:
        opinions = Opinion.query.filter(
            Opinion.title.ilike(f'%{title}%')
        ).all()
    else:
        opinions = Opinion.query.all()
    opinions_list = [opinion.to_dict() for opinion in opinions]
    return jsonify({'opinions': opinions_list}), 200


@app.route('/api/opinions/', methods=['POST'])
def add_opinion():
    """Создать мнение из JSON с обязательными полями title и text.

    Вернуть созданное мнение с HTTP-статусом 201 или ошибку со статусом
    400, если JSON не является объектом или отсутствуют обязательные поля.
    """
    data = request.get_json()
    if (
        not isinstance(data, dict)
        or 'title' not in data
        or 'text' not in data
    ):
        return jsonify({'error': 'Поля title и text обязательны'}), 400
    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201


@app.route('/api/opinions/<int:id>/', methods=['GET'])
def get_opinion(id):
    """Вернуть мнение по id со статусом 200 или ошибку со статусом 404."""
    opinion = db.session.get(Opinion, id)
    if opinion is None:
        return jsonify({'error': 'Мнение не найдено'}), 404
    return jsonify({'opinion': opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['PATCH'])
def update_opinion(id):
    """Обновить переданные в JSON поля мнения с указанным id.

    Разрешены поля title, text, source и added_by. Вернуть обновлённое
    мнение со статусом 200 или ошибку со статусом 404, если его нет.
    """
    data = request.get_json()
    opinion = db.session.get(Opinion, id)
    if opinion is None:
        return jsonify({'error': 'Мнение не найдено'}), 404
    opinion.title = data.get('title', opinion.title)
    opinion.text = data.get('text', opinion.text)
    opinion.source = data.get('source', opinion.source)
    opinion.added_by = data.get('added_by', opinion.added_by)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['DELETE'])
def delete_opinion(id):
    """Удалить мнение по id и вернуть пустой ответ со статусом 204.

    Если мнение не найдено, вернуть ошибку с HTTP-статусом 404.
    """
    opinion = db.session.get(Opinion, id)
    if opinion is None:
        return jsonify({'error': 'Мнение не найдено'}), 404
    db.session.delete(opinion)
    db.session.commit()
    return '', 204


@app.route('/api/opinions/random/', methods=['GET'])
def get_random_opinion():
    """Вернуть случайное мнение со статусом 200 или ошибку 404.

    Ошибка возвращается, если в базе данных нет мнений.
    """
    opinion = random_opinion()
    if opinion is not None:
        return jsonify({'opinion': opinion.to_dict()}), 200
    return jsonify({'error': 'В базе нет мнений'}), 404
