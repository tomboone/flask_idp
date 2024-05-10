import os
from flask import render_template, flash, redirect, url_for, current_app
from flask_security import auth_required, hash_password
from email_validator import validate_email, EmailNotValidError
from unicodedata import normalize
from base64 import b64encode
from flask_security.decorators import roles_required
from app.idp import bp
from app.idp import crud
from app.forms import (
    user, role, deleterole, institution, deleteinstitution, deleteuser, changepassword, userroles, status
)
from datetime import datetime
from flask_login import current_user


# Error handlers
@bp.errorhandler(404)
def not_found_error(error):
    return render_template("404.html", error=error)


# 500 error handler
@bp.errorhandler(500)
def internal_error(error):
    return render_template("500.html", error=error)


# 403 error handler
@bp.errorhandler(403)
def forbidden(error):
    return render_template("403.html", error=error)


# Home page
@bp.route("/")
@auth_required()
def home():
    uinst = crud.get_user_institution(current_user)
    return render_template("home.html", user_institution=uinst)


# Update current user's profile
@bp.route("/edit/", methods=["GET", "POST"])
@auth_required()
def edit_profile():
    form = user.UserForm(obj=current_user)
    allinsts = crud.read_institutions()
    form.institution.choices = [(inst.id, inst.name + ' (' + inst.code + ')') for inst in allinsts]
    if form.validate_on_submit():
        try:
            validate_email(form.email.data)
        except EmailNotValidError as e:
            flash(f"{form.email.data} is not a valid email address: {e}", "error")
            return redirect(url_for("idp.edit_profile"))
        updated_user = crud.update_user(
            current_user.id,
            form.username.data,
            form.email.data,
            form.first_name.data,
            form.last_name.data,
            form.institution.data
        )
        flash(f"Profile updated for {updated_user.username}", "info")
        return redirect(url_for("idp.home"))
    return render_template("edit_account.html", form=form, user=current_user)


@bp.route("/admin/")
@auth_required()
@roles_required("admin")
def admin():
    return render_template("admin.html", user=current_user)


# All users
@bp.route("/admin/users/")
@auth_required()
@roles_required("admin")
def users():
    active_users = crud.read_active_users()
    inactive_users = crud.read_inactive_users()
    all_institutions = crud.read_institutions()
    inst_list = []
    for inst in all_institutions:
        inst_list.append(inst)
    return render_template("users.html", active=active_users, inactive=inactive_users, institutions=inst_list)


# Create user
@bp.route("/admin/users/add/", methods=["GET", "POST"])
@auth_required()
@roles_required("admin")
def add_user():
    user_role = current_app.extensions["security"].datastore.find_role(os.getenv("USER_ROLE"))
    form = user.UserForm()
    allinsts = crud.read_institutions()
    form.institution.choices = [(inst.id, inst.name + ' (' + inst.code + ')') for inst in allinsts]
    if form.validate_on_submit():
        try:
            validate_email(form.email.data)
        except EmailNotValidError as e:
            flash(f"{form.email.data} is not a valid email address: {e}", "error")
            return redirect(url_for("idp.add_user"))
        else:
            email = form.email.data
        try:
            password = normalize("NFKD", b64encode(os.urandom(16)).decode("utf-8"))
        except Exception as e:
            flash(f"Error generating password: {e}", "error")
            return redirect(url_for("idp.add_user"))
        new_user = current_app.extensions["security"].datastore.create_user(
            username=form.username.data,
            email=email,
            password=hash_password(password),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            institution=form.institution.data,
            roles=[user_role],
            created=datetime.now()
        )
        current_app.extensions["security"].datastore.commit()
        flash(f"{new_user.email} added", "info")
        return redirect(url_for("idp.users"))
    return render_template("add_user.html", form=form)


# Read user
@bp.route("/admin/users/<username>/")
@auth_required()
@roles_required("admin")
def user_detail(username):
    user_details = current_app.extensions["security"].datastore.find_user(username=username)
    all_institutions = crud.read_institutions()
    inst_obj = (inst_item for inst_item in all_institutions if inst_item.id == user_details.institution)
    user_details.institution = next(inst_obj, None)
    return render_template("user.html", user=user_details)


# Update user
@bp.route("/admin/users/<username>/edit/", methods=["GET", "POST"])
@auth_required()
@roles_required("admin")
def edit_user(username):
    user_details = current_app.extensions["security"].datastore.find_user(username=username)
    form = user.UserForm(obj=user_details)
    allinsts = crud.read_institutions()
    form.institution.choices = [(inst.id, inst.name + ' (' + inst.code + ')') for inst in allinsts]
    if form.validate_on_submit():
        try:
            validate_email(form.email.data)
        except EmailNotValidError as e:
            flash(f"{form.email.data} is not a valid email address: {e}", "error")
            return redirect(url_for("idp.edit_user", username=username))
        updated_user = crud.update_user(
            user_details.id,
            form.username.data,
            form.email.data,
            form.first_name.data,
            form.last_name.data,
            form.institution.data
        )
        flash(f"{form.email.data} updated", "info")
        return redirect(url_for("idp.user_detail", username=updated_user.username))
    return render_template("edit_user.html", form=form, user=user_details)


# Change user roles
@bp.route("/admin/users/<username>/roles/", methods=["GET", "POST"])
@auth_required()
@roles_required("admin")
def change_roles(username):
    user_details = current_app.extensions["security"].datastore.find_user(username=username)
    form = userroles.UserRolesForm(obj=user_details)
    all_roles = crud.read_roles()
    form.roles.choices = [(urole, urole.description) for urole in all_roles]
    user_role = current_app.extensions["security"].datastore.find_role(os.getenv("USER_ROLE"))
    if form.validate_on_submit():
        all_roles = crud.read_roles()
        for urole in all_roles:
            if urole.name == os.getenv("USER_ROLE"):
                continue
            if '<Role ' + urole.name + '>' in form.roles.data:
                current_app.extensions["security"].datastore.add_role_to_user(user_details, urole)
                current_app.extensions["security"].datastore.commit()
                crud.update_user_updated(user_details.id)
            elif '<Role ' + urole.name not in form.roles.data:
                current_app.extensions["security"].datastore.remove_role_from_user(user_details, urole)
                current_app.extensions["security"].datastore.commit()
                crud.update_user_updated(user_details.id)
        flash("Roles updated", "info")
        return redirect(url_for("idp.user_detail", username=username))
    return render_template("change_roles.html", form=form, user=user_details, user_role=user_role)


# Change user password
@bp.route("/admin/users/<username>/password/", methods=["GET", "POST"])
@auth_required()
@roles_required("admin")
def change_password(username):
    user_details = current_app.extensions["security"].datastore.find_user(username=username)
    form = changepassword.ChangePasswordForm(obj=user_details)
    if form.validate_on_submit():
        password = hash_password(form.new_password.data)
        crud.update_password(user_details.id, password)
        flash("Password updated", "info")
        return redirect(url_for("idp.user_detail", username=username))
    for item in form.errors.items():
        flash(f"{item[0]}: {item[1]}", "error")
    return render_template("change_password.html", form=form, user=user_details)


# Change user status
@bp.route("/admin/users/<username>/status/", methods=["GET", "POST"])
@auth_required()
@roles_required("admin")
def user_status(username):
    user_details = current_app.extensions["security"].datastore.find_user(username=username)
    form = status.UserStatusForm(obj=user_details)
    if form.validate_on_submit():
        current_app.extensions["security"].datastore.toggle_active(user_details)
        current_app.extensions["security"].datastore.commit()
        crud.update_user_updated(user_details.id)
        action = "activated" if user_details.active else "deactivated"
        flash(f"{username} {action}", "info")
        return redirect(url_for("idp.user_detail", username=username))
    return render_template("status.html", form=form, user=user_details)


# Delete user
@bp.route("/admin/users/<username>/delete/", methods=["GET", "POST"])
@auth_required()
@roles_required("admin")
def delete_user(username):
    user_details = current_app.extensions["security"].datastore.find_user(username=username)
    form = deleteuser.DeleteUserForm(obj=user_details)
    if form.validate_on_submit():
        current_app.extensions["security"].datastore.delete_user(user_details)
        current_app.extensions["security"].datastore.commit()
        flash(f"{username} deleted", "info")
        return redirect(url_for("idp.users"))
    return render_template("delete_user.html", form=form, user=user_details)


# All roles
@bp.route("/admin/roles/")
@auth_required()
@roles_required("admin")
def roles():
    all_roles = crud.read_roles()
    return render_template("roles.html", roles=all_roles)


# Create role
@bp.route("/admin/roles/add/", methods=["GET", "POST"])
@auth_required()
@roles_required("admin")
def add_role():
    form = role.RoleForm()
    if form.validate_on_submit():
        current_app.extensions["security"].datastore.create_role(
            name=form.name.data,
            description=form.description.data
        )
        current_app.extensions["security"].datastore.commit()
        flash("Role added", "info")
        return redirect(url_for("idp.roles"))
    return render_template("add_role.html", form=form)


# Read role
@bp.route("/admin/roles/<role_name>/")
@auth_required()
@roles_required("admin")
def role_detail(role_name):
    role_details = current_app.extensions["security"].datastore.find_role(role_name)
    return render_template("role.html", role=role_details)


# Update role
@bp.route("/admin/roles/<role_name>/edit/", methods=["GET", "POST"])
@auth_required()
@roles_required("admin")
def edit_role(role_name):
    role_details = current_app.extensions["security"].datastore.find_role(role_name)
    form = role.RoleForm(obj=role_details)
    if form.validate_on_submit():
        crud.update_role(role_details.id, form.name.data, form.description.data)
        flash("Role updated", "info")
        return redirect(url_for('idp.roles', role=role_details))
    return render_template(
        "edit_role.html",
        form=form,
        role=role_details,
        admin=os.getenv("ADMIN_ROLE"),
        user=os.getenv("USER_ROLE")
    )


# Delete role
@bp.route("/admin/roles/<role_name>/delete/", methods=["GET", "POST"])
@auth_required()
@roles_required("admin")
def delete_role(role_name):
    role_details = current_app.extensions["security"].datastore.find_role(role_name)
    form = deleterole.DeleteRoleForm(obj=role_details)
    if form.validate_on_submit():
        current_app.extensions["security"].datastore.delete_role(role_details)
        current_app.extensions["security"].datastore.commit()
        flash("Role deleted", "info")
        return redirect(url_for("idp.roles"))
    return render_template(
        "delete_role.html",
        form=form,
        role=role_details,
        admin=os.getenv("ADMIN_ROLE"),
        user=os.getenv("USER_ROLE")
    )


# Read institutions
@bp.route("/admin/institutions/")
@auth_required()
@roles_required("admin")
def institutions():
    all_institutions = crud.read_institutions()
    return render_template("institutions.html", institutions=all_institutions)


# Create institution
@bp.route("/admin/institutions/add/", methods=["GET", "POST"])
@auth_required()
@roles_required("admin")
def add_institution():
    form = institution.InstitutionForm()
    if form.validate_on_submit():
        crud.create_institution(form.code.data, form.name.data)
        flash("Institution added", "info")
        return redirect(url_for("idp.institutions"))
    return render_template("add_institution.html", form=form)


# Read institution
@bp.route("/admin/institutions/<code>/")
@auth_required()
@roles_required("admin")
def institution_detail(code):
    institution_details = crud.read_institution(code)
    return render_template("institution.html", institution=institution_details)


# Update institution
@bp.route("/admin/institutions/<code>/edit/", methods=["GET", "POST"])
@auth_required()
@roles_required("admin")
def edit_institution(code):
    institution_details = crud.read_institution(code)
    form = institution.InstitutionForm(obj=institution_details)
    if form.validate_on_submit():
        crud.update_institution(institution_details.id, form.code.data, form.name.data)
        flash("Institution updated", "info")
        return redirect(url_for("idp.institutions"))
    return render_template("edit_institution.html", form=form, institution=institution_details)


# Delete institution
@bp.route("/admin/institutions/<code>/delete/", methods=["GET", "POST"])
@auth_required()
@roles_required("admin")
def delete_institution(code):
    institution_details = crud.read_institution(code)
    form = deleteinstitution.DeleteInstitutionForm(obj=institution_details)
    if form.validate_on_submit():
        crud.delete_institution(institution_details.id)
        flash("Institution deleted", "info")
        return redirect(url_for("idp.institutions"))
    return render_template("delete_institution.html", form=form, institution=institution_details)
