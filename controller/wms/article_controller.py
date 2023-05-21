from werkzeug.exceptions import NotFound
from sqlalchemy import func
from sqlalchemy.orm import aliased
from sqlalchemy.sql import and_
from models import db, Article, Rest, Warehouse


def get_wms_article_list():
    article = Article.query.order_by(Article.id_art).all()
    return article

def get_article_or_raise(id_art:int) -> Article:
    article = Article.query.get(id_art)
    if article:
        return article
    
    raise NotFound(f'Товар #{id_art} не найден!')


def wms_create_article(code:str, name:str, is_online:bool, price_buy:float, price_sale:float):
    article = Article(code=code, name=name, is_online=is_online, price_buy=price_buy, price_sale=price_sale)
    db.session.add(article)
    db.session.commit()
    return article

def wms_update_article(id_art:int, name:str, is_online:bool, price_buy:float, price_sale:float):
    article = Article.query.get(id_art)
    article.name = name
    article.is_online = is_online
    article.price_buy = price_buy
    article.price_sale = price_sale
    print(article.code)
    db.session.add(article)
    db.session.commit()
    return article


def wms_delete_article(id_art:int):
    article = Article.query.get(id_art)
    db.session.delete(article)
    db.session.commit()
    
    
def wms_show_article_rest(id_art:int):
    r = aliased(Rest)
    ws = aliased(Warehouse)
    artrest= Article.query.join(
            r,
            r.id_art == Article.id_art
        ).join(
            ws,
            ws.id_ws == r.id_ws
        ).filter(
            Article.id_art==id_art
        ).add_columns(
            Article.code,
            Article.name.label('artname'),
            ws.name.label('wsname'),
            r.quantity,
        ).all()
    return artrest