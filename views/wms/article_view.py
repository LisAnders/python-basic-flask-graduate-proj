from http import HTTPStatus
from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required

from .forms import ArticleForm
from controller.wms.article_controller import (
    get_wms_article_list,
    get_article_or_raise,
    wms_create_article,
    wms_update_article,
    wms_delete_article,
    wms_show_article_rest, 
)
from controller.login_controller import chek_roles

article_app = Blueprint(
    'article_app',
    __name__,
    url_prefix='/article'
)


@article_app.get('/', endpoint='list')
@login_required
@chek_roles(['Admin','Manager'])
def get_article_list():
    article = get_wms_article_list()
    return render_template('wms/article/list.html', article=article)


@article_app.get('/<int:id_art>/', endpoint='details')
@login_required
@chek_roles(['Admin','Manager'])
def get_article_details(id_art:int):
    article = get_article_or_raise(id_art)
    return render_template('wms/article/details.html', article=article)


@article_app.route('/create/', methods=['GET', 'POST'], endpoint='create')
@login_required
@chek_roles(['Admin','Manager'])
def create_article():
    form = ArticleForm()
    
    if request.method == 'GET':
        return render_template('wms/article/create.html', form=form)
    if not form.validate_on_submit():
        return (render_template('wms/article/create.html', form=form), HTTPStatus.BAD_REQUEST)
    
    article = wms_create_article(
        code=str(form.data['code']), 
        name=str(form.data['name']), 
        is_online=bool(form.data['is_online']), 
        price_buy=float(form.data['price_buy']), 
        price_sale=float(form.data['price_sale']))
    return redirect(url_for('wms_app.article_app.details', id_art=article.id_art))


@article_app.route('/<int:id_art>/update/', methods=['GET', 'POST'], endpoint='update')
@login_required
@chek_roles(['Admin','Manager'])
def update_article_detail(id_art):
    article = get_article_or_raise(id_art)
    form = ArticleForm()
    if request.method == 'GET':
        return render_template('wms/article/update.html', form=form, article=article)
    
    if not form.validate_on_submit():
        return (render_template('wms/article/update.html', form=form, article=article), HTTPStatus.BAD_REQUEST)
    
    article = wms_update_article(
        id_art=id_art, 
        name=str(form.data['name']), 
        is_online=bool(form.data['is_online']),
        price_buy=float(form.data['price_buy']), 
        price_sale=float(form.data['price_sale'])
        )
    return redirect(url_for('wms_app.article_app.details', id_art=id_art))


@article_app.route('/<int:id_art>/delete/', methods=['GET', 'POST'], endpoint='delete')
@login_required
@chek_roles(['Admin','Manager'])
def delete_article(id_art):
    article = get_article_or_raise(id_art)
    if request.method == 'GET':
        return render_template('wms/article/delete.html', article=article)
    wms_delete_article(id_art=id_art)
    return redirect(url_for('wms_app.article_app.list'))


@article_app.route('/<int:id_art>/show_article_rest', methods=['GET'], endpoint='show_article_rest')
@login_required
@chek_roles(['Admin','Manager'])
def show_article_rest(id_art:int):
    article = get_article_or_raise(id_art)
    artrest= wms_show_article_rest(id_art)
    return render_template('wms/article/show_article_rest.html', artrest=artrest, article=article)
