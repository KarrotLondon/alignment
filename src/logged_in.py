from flask import Blueprint, flash, render_template, request, redirect, url_for, jsonify

from src.models.link import Link
from . import db, kink_list
from flask_login import login_required, current_user
from src.models.kink import Kink
from src.models.enums import Experience, Frequency, Enjoyment, Roles

logged = Blueprint('logged', __name__)

@logged.context_processor
def inject_links():
  return dict(new_links=db.no_link_requests(current_user.id))

@logged.route('/profile')
@login_required
def profile():
  return render_template('profile.html', username=current_user.username)


@logged.route('/kink-sub')
@login_required
def kinks_sub():
  user_kinks = current_user.kinks.sub
  get_kinks(user_kinks)
  return render_template('kinks.html', kinks=sorted(user_kinks, key=lambda x: x.kink_name), state=Roles.SUB.value)

@logged.route('/kink-dom')
@login_required
def kinks_dom():
  user_kinks = current_user.kinks.dom
  get_kinks(user_kinks)
  return render_template('kinks.html', kinks=sorted(user_kinks, key=lambda x: x.kink_name), state=Roles.DOM.value)

def get_kinks(user_kinks):
    user_kinks_names = [list(kink.dict(include={'kink_name'}).values())[0] for kink in user_kinks]
    for kink in kink_list:
      if kink not in user_kinks_names:
        user_kinks.append(Kink(kink_name=kink))

@logged.route('/kink-sub', methods=['POST'])
@login_required
def kinks_sub_post():
  kinks_to_update = []
  for kink in kink_list:
    kink_name = kink
    kink_frequency = request.form.get(f"{kink_name}-frequency")
    kink_enjoyment = request.form.get(f"{kink_name}-enjoyment")
    kink_experience = request.form.get(f"{kink_name}-experience")
    get_updated_kinks(kinks_to_update, kink_name, kink_frequency, kink_enjoyment, kink_experience)
  db.update_kinks(current_user.id, kinks_to_update, Roles.SUB)
  return jsonify(success=True)

@logged.route('/kink-dom', methods=['POST'])
@login_required
def kinks_dom_post():
  kinks_to_update = []
  for kink in kink_list:
    kink_name = kink
    kink_frequency = request.form.get(f"{kink_name}-frequency")
    kink_enjoyment = request.form.get(f"{kink_name}-enjoyment")
    kink_experience = request.form.get(f"{kink_name}-experience")
    get_updated_kinks(kinks_to_update, kink_name, kink_frequency, kink_enjoyment, kink_experience)
  db.update_kinks(current_user.id, kinks_to_update, Roles.DOM)
  return jsonify(success=True)

def get_updated_kinks(kinks_to_update, kink_name, kink_frequency, kink_enjoyment, kink_experience):
    if kink_frequency != "" or kink_enjoyment != "" or kink_experience != "":
      if kink_enjoyment != "":
        enjoyment = Enjoyment[kink_enjoyment]
      else:
        enjoyment = None
      if kink_frequency != "":
        frequency = Frequency[kink_frequency]
      else: 
        frequency = None
      if kink_experience != "":
        experience = Experience[kink_experience]
      else: 
        experience = None
      kinks_to_update.append(Kink(kink_name=kink_name, experience=experience, frequency=frequency, enjoyment=enjoyment))

@logged.route('/links')
@login_required
def links():
  user_links = current_user.links  
  return render_template('links.html', links=sorted(user_links, key=lambda x: x.username))

@logged.route('/links', methods=['POST'])
@login_required
def links_post():
  username = request.form.get("username")
  links = request.form.getlist("kink_lists")
  if not db.check_username_in_use(username):
    flash('Unable to locate user')
    return redirect(url_for('logged.links'))
  current_links = [link.username for link in current_user.links]
  if username in current_links:
    flash('Already linked with user')
    return redirect(url_for('logged.links'))
  user_to_link = db.get_user_by_username(username)
  current_user_relationships = []
  if "share-sub" in links:
    current_user_relationships.append(Roles.SUB)
  if "share-dom" in links:
    current_user_relationships.append(Roles.DOM)
  link_user_relationships = []
  if "request-sub" in links:
    link_user_relationships.append(Roles.SUB)
  if "request-dom" in links:
    link_user_relationships.append(Roles.DOM)
  
  db.update_links(current_user.id, Link(user_id=str(user_to_link.id), username=username, pending=True, mutual_required=True, requested=False, relationships=link_user_relationships))
  db.update_links(user_to_link.id, Link(user_id=str(current_user.id), username=current_user.username, pending=True, mutual_required=True, requested=True, relationships=current_user_relationships))
  return redirect(url_for('logged.links'))
  
@logged.route('/combined-kinks', methods=["POST"])
@login_required
def update_link():
  user_id = request.form.get("user_id")
  action = request.form.get("update_link")
  if action == "Approve":
    db.approve_link(current_user.id, user_id)
    return redirect(url_for('logged.links'))
  if action[0:4] == "view":
    link = db.get_user_by_id(user_id)
    kink_list_action = action[5:]
    # user_kinks = current_user.kinks.sub if kink_list=
    # user_kinks_names = [list(kink.dict(include={'kink_name'}).values())[0] for kink in user_kinks]
    link_kinks = link.kinks.sub if kink_list_action == "sub" else link.kinks.dom
    link_kinks_names = [list(kink.dict(include={'kink_name'}).values())[0] for kink in link_kinks]
    for kink in kink_list:
      if kink not in link_kinks_names:
        link_kinks.append(Kink(kink_name=kink))
      # if kink not in user_kinks_names:
      #   user_kinks.append(Kink(kink_name=kink))
    # return render_template('kinks_combined.html', user=current_user.username, link_user=link.username, kinks=sorted(user_kinks, key=lambda x: x.kink_name), links=sorted(link_kinks, key=lambda x: x.kink_name))
    return render_template('links_kinks.html', role=kink_list_action, link_user=link.username, links=sorted(link_kinks, key=lambda x: x.kink_name))


