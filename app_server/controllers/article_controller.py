
import json
from app_server.models.user_model import User

def article_to_dict(article,session):
    dict = {}
    for key, value in vars(article).items():
        if key == 'id' or key == '_sa_instance_state':
            continue
        if key == 'imgs' and value:
            dict[key] = json.loads(value)
            continue
        dict[key] = value

    poster_id = article.poster_id
    anonymous = article.anonymous
    if poster_id and not anonymous:
        poster = session.query(User).filter_by(user_id=poster_id).first()
        dict['poster_id'] = poster_id
        dict['poster_name'] = poster.name
        dict['icon'] = poster.icon
    else:
        dict['poster_id'] = 0
        dict['poster_name'] = 'anonymous'
        dict['icon'] = 'anonymous png'

    return dict

