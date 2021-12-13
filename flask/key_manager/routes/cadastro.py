from key_manager import app
from key_manager.models import db
from key_manager.models.category import Category
from key_manager.models.key import Key
from key_manager.models.user import User
from key_manager.models.registry import Registry
from key_manager.forms.formUser import FormUser
from key_manager.forms.formReg import RegForm
from key_manager.forms.formKey import KeyForm
from key_manager.forms.formCat import CatForm
from flask import (
    Blueprint, render_template,
    request, url_for, redirect, 
    flash, session
)
import hashlib

cadastro = Blueprint("cadastro", __name__, url_prefix="/new")

@cadastro.route("/category", methods=["GET", "POST"])
def newCategory():
    catForm = CatForm()
    if session.get("user_auth", False) and session["user_auth"] == True:
        if request.method == "POST":
            name = request.form["name"]
            slug = request.form["slug"]
            
            if catForm.validate_on_submit():
                newCat = Category(name=name, slug=slug)
                db.session.add(newCat)
                db.session.commit()
                return redirect(url_for("admin.admHome"))
        return render_template("forms/cadastrar_categoria.html", form=catForm, action=url_for("cadastro.newCategory"), hidden_footer=True)
    return redirect(url_for('index'))

@cadastro.route("/key", methods=["GET", "POST"])
def newKey():
    if session.get("user_auth", False) and session["user_auth"] == True:
        keyForm = KeyForm()
        keyForm.key_category_id.choices = [(cat.id, cat.name) for cat in Category.query.order_by("name")]
        if request.method == "POST":
            name = request.form["name"]
            slug = request.form["slug"]

            key_category_id = int(request.form["key_category_id"])
            if keyForm.validate_on_submit():
                newKey = Key(name=name, slug=slug, key_category_id=key_category_id)
                db.session.add(newKey)
                db.session.commit()
                return redirect(url_for("admin.admHome"))
        return render_template("forms/cadastrar_chave.html", form=keyForm, action=url_for('cadastro.newKey'), hidden_footer=True)
    return redirect(url_for('index'))
@cadastro.route("/user", methods=["GET", "POST"])
def newUser():
    userform = FormUser()
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        hash_passsword = hashlib.md5(password.encode("utf8")).hexdigest()

        if userform.validate_on_submit():
            try:
                newuser = User(name=name, username=username, email=email, phone=phone, password=hash_passsword)
                db.session.add(newuser)
                db.session.commit()
            except:
                # já existe
                pass
            return redirect(url_for("view.viewUser",user_username=newuser.username))
    return render_template("forms/cadastrar_usuario.html", form=userform, action=url_for('cadastro.newUser'))
@cadastro.route('/registry', methods=['GET', 'POST'])
def newRegistry():
    if session.get("user_auth", False) and session["user_auth"] == True:    
        regForm = RegForm()
        regForm.user_id.choices = [(user.id, user.username) for user in User.query.order_by("username")]
        regForm.key_id.choices = [(key.id, key.name) for key in Key.query.order_by("name")]

        if request.method == "POST":
            user_id = int(request.form["user_id"])
            key_id = int(request.form["key_id"])
            name = request.form["holder_name"]
            email = request.form["holder_email"]
            
            if regForm.validate_on_submit():
                newRegistry = Registry(user_id=user_id, key_id=key_id, holder_name=name, holder_email=email)
                db.session.add(newRegistry)
                db.session.commit()
                return redirect(url_for("view.viewReg", reg_id=newRegistry.id))
        return render_template("forms/cadastrar_emprestimo.html", form=regForm, action=url_for('cadastro.newRegistry'), hidden_footer=True)
    return redirect(url_for('index'))
app.register_blueprint(cadastro)