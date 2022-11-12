from flask import Blueprint, flash, render_template, request, redirect, url_for, jsonify

from src.models.link import Link
from . import db, kink_list
from flask_login import login_required, current_user
from src.models.kink import Kink
from src.models.enums import Experience, Frequency, Enjoyment

logged = Blueprint('logged', __name__)

@logged.context_processor
def inject_links():
  return dict(new_links=db.no_link_requests(current_user.id))

@logged.route('/profile')
@login_required
def profile():
  return render_template('profile.html', username=current_user.username)


@logged.route('/kink')
@login_required
def kinks():
  user_kinks = current_user.kinks
  user_kinks_names = [list(kink.dict(include={'kink_name'}).values())[0] for kink in user_kinks]
  for kink in kink_list:
    if kink not in user_kinks_names:
      user_kinks.append(Kink(kink_name=kink))
  return render_template('kinks.html', kinks=sorted(user_kinks, key=lambda x: x.kink_name))

@logged.route('/kink', methods=['POST'])
@login_required
def kinks_post():
  kinks_to_update = []
  for kink in kink_list:
    kink_name = kink
    kink_frequency = request.form.get(f"{kink_name}-frequency")
    kink_enjoyment = request.form.get(f"{kink_name}-enjoyment")
    kink_experience = request.form.get(f"{kink_name}-experience")
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
  db.update_kinks(current_user.id, kinks_to_update)
  return jsonify(success=True)

@logged.route('/links')
@login_required
def links():
  user_links = current_user.links  
  return render_template('links.html', links=sorted(user_links, key=lambda x: x.username))

@logged.route('/links', methods=['POST'])
@login_required
def links_post():
  username = request.form.get("username")
  if not db.check_username_in_use(username):
    flash('Unable to locate user')
    return redirect(url_for('logged.links'))
  current_links = [link.username for link in current_user.links]
  if username in current_links:
    flash('Already linked with user')
    return redirect(url_for('logged.links'))
  user_to_link = db.get_user_by_username(username)
  db.update_links(current_user.id, Link(user_id=str(user_to_link.id), username=username, pending=True, mutual_required=True, requested=False))
  db.update_links(user_to_link.id, Link(user_id=str(current_user.id), username=current_user.username, pending=True, mutual_required=True, requested=True))
  return redirect(url_for('logged.links'))
  
@logged.route('/combined-kinks', methods=["POST"])
@login_required
def update_link():
  user_id = request.form.get("user_id")
  action = request.form.get("update_link")
  if action == "Approve":
    db.approve_link(current_user.id, user_id)
    return redirect(url_for('logged.links'))
  if action == "View":
    link = db.get_user_by_id(user_id)
    user_kinks = current_user.kinks
    user_kinks_names = [list(kink.dict(include={'kink_name'}).values())[0] for kink in user_kinks]
    link_kinks = link.kinks
    link_kinks_names = [list(kink.dict(include={'kink_name'}).values())[0] for kink in link_kinks]
    for kink in kink_list:
      if kink not in link_kinks_names:
        link_kinks.append(Kink(kink_name=kink))
      if kink not in user_kinks_names:
        user_kinks.append(Kink(kink_name=kink))
    return render_template('kinks_combined.html', user=current_user.username, link_user=link.username, kinks=sorted(user_kinks, key=lambda x: x.kink_name), links=sorted(link_kinks, key=lambda x: x.kink_name))