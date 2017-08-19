
from super_models.database import SessionContext


def get_user_id():
    with SessionContext() as session:
        session.execute('UPDATE id_box SET value=LAST_INSERT_ID(value+1) WHERE name="UserID";')
        new_id = session.execute('SELECT LAST_INSERT_ID();').scalar()
        session.commit()
        return new_id


def get_banner_id():
    with SessionContext() as session:
        session.execute('UPDATE id_box SET value=LAST_INSERT_ID(value+1) WHERE name="BannerID";')
        new_id = session.execute('SELECT LAST_INSERT_ID();').scalar()
        session.commit()
        return new_id


def get_store_id():
    with SessionContext() as session:
        session.execute('UPDATE id_box SET value=LAST_INSERT_ID(value+1) WHERE name="StoreID";')
        new_id = session.execute('SELECT LAST_INSERT_ID();').scalar()
        session.commit()
        return new_id


def get_article_id():
    with SessionContext() as session:
        session.execute('UPDATE id_box SET value=LAST_INSERT_ID(value+1) WHERE name="ArticleID";')
        new_id = session.execute('SELECT LAST_INSERT_ID();').scalar()
        session.commit()
        return new_id


def get_comment_id():
    with SessionContext() as session:
        session.execute('UPDATE id_box SET value=LAST_INSERT_ID(value+1) WHERE name="CommentID";')
        new_id = session.execute('SELECT LAST_INSERT_ID();').scalar()
        session.commit()
        return new_id
