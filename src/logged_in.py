from typing import Dict, List, Optional, Union, cast

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.wrappers import Response

from src.models.combined_kink import CombinedKink
from src.models.enums import Enjoyment, Experience, Frequency, Roles
from src.models.kink import Kink
from src.models.link import Link
from src.models.user import User

from . import db, kink_list

logged = Blueprint("logged", __name__)


@logged.context_processor
def inject_links() -> Dict[str, int]:
    return dict(new_links=db.no_link_requests(cast(User, current_user).id))


@logged.route("/profile")
@login_required
def profile() -> str:
    return render_template("profile.html", username=cast(User, current_user).username)


@logged.route("/kink-sub")
@login_required
def kinks_sub() -> str:
    user_kinks = cast(User, current_user).kinks.sub
    complete_kinks(user_kinks)
    return render_template(
        "kinks.html",
        kinks=sorted(user_kinks, key=lambda x: x.kink_name),
        state=Roles.SUB.value,
    )


@logged.route("/kink-dom")
@login_required
def kinks_dom() -> str:
    user_kinks = cast(User, current_user).kinks.dom
    complete_kinks(user_kinks)
    return render_template(
        "kinks.html",
        kinks=sorted(user_kinks, key=lambda x: x.kink_name),
        state=Roles.DOM.value,
    )


def complete_kinks(user_kinks: List[Kink]) -> None:
    user_kinks_names = [list(kink.dict(include={"kink_name"}).values())[0] for kink in user_kinks]
    for kink in kink_list:
        if kink not in user_kinks_names:
            user_kinks.append(Kink(kink_name=kink))


@logged.route("/kink-sub", methods=["POST"])
@login_required
def kinks_sub_post() -> Response:
    kinks_to_update = []
    for kink in kink_list:
        kink_name = kink
        kink_frequency = request.form.get(f"{kink_name}-frequency")
        kink_enjoyment = request.form.get(f"{kink_name}-enjoyment")
        kink_experience = request.form.get(f"{kink_name}-experience")
        kinks_to_update.append(get_updated_kinks(kink_name, kink_frequency, kink_enjoyment, kink_experience))
    db.update_kinks(cast(User, current_user).id, kinks_to_update, Roles.SUB)
    return jsonify(success=True)


@logged.route("/kink-dom", methods=["POST"])
@login_required
def kinks_dom_post() -> Response:
    kinks_to_update = []
    for kink in kink_list:
        kink_name = kink
        kink_frequency = request.form.get(f"{kink_name}-frequency")
        kink_enjoyment = request.form.get(f"{kink_name}-enjoyment")
        kink_experience = request.form.get(f"{kink_name}-experience")
        kinks_to_update.append(get_updated_kinks(kink_name, kink_frequency, kink_enjoyment, kink_experience))
    db.update_kinks(cast(User, current_user).id, kinks_to_update, Roles.DOM)
    return jsonify(success=True)


def get_updated_kinks(
    kink_name: str, kink_frequency: Optional[str], kink_enjoyment: Optional[str], kink_experience: Optional[str]
) -> Kink:
    if kink_enjoyment:
        enjoyment = Enjoyment[kink_enjoyment]
    else:
        enjoyment = None
    if kink_frequency:
        frequency = Frequency[kink_frequency]
    else:
        frequency = None
    if kink_experience:
        experience = Experience[kink_experience]
    else:
        experience = None
    return Kink(
        kink_name=kink_name,
        experience=experience,
        frequency=frequency,
        enjoyment=enjoyment,
    )


@logged.route("/links")
@login_required
def links() -> str:
    user_links = cast(User, current_user).links
    return render_template("links.html", links=sorted(user_links, key=lambda x: x.username))


@logged.route("/links", methods=["POST"])
@login_required
def links_post() -> Response:
    username = request.form.get("username")
    links = request.form.getlist("kink_lists")
    if not db.check_username_in_use(username):
        flash("Unable to locate user")
        return redirect(url_for("logged.links"))
    current_links = [link.username for link in cast(User, current_user).links]
    if username in current_links:
        flash("Already linked with user")
        return redirect(url_for("logged.links"))
    user_to_link = db.get_user_by_username(username)
    if not user_to_link:
        raise NotImplementedError
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

    db.update_links(
        cast(User, current_user).id,
        Link(
            user_id=str(user_to_link.id),
            username=username,
            pending=True,
            mutual_required=True,
            requested=False,
            relationships=link_user_relationships,
        ),
    )
    db.update_links(
        user_to_link.id,
        Link(
            user_id=str(cast(User, current_user).id),
            username=cast(User, current_user).username,
            pending=True,
            mutual_required=True,
            requested=True,
            relationships=current_user_relationships,
        ),
    )
    return redirect(url_for("logged.links"))


@logged.route("/links-kinks", methods=["POST"])
@login_required
def update_link() -> Union[str, Response]:
    user_id = request.form.get("user_id")
    action = request.form.get("update_link")
    if not action:
        raise NotImplementedError
    if action == "Approve":
        db.approve_link(cast(User, current_user).id, user_id)
        return redirect(url_for("logged.links"))
    if action[0:4] == "view":
        link = db.get_user_by_id(user_id)
        if not link:
            raise NotImplementedError
        kink_list_action = action[5:]
        link_kinks = link.get_kinks_for_role(kink_list_action)
        link_kinks_names = [list(kink.dict(include={"kink_name"}).values())[0] for kink in link_kinks]
        relationships = [lin.relationships for lin in cast(User, current_user).links if lin.user_id == user_id][0]
        for kink in kink_list:
            if kink not in link_kinks_names:
                link_kinks.append(Kink(kink_name=kink))
        print(relationships)
        return render_template(
            "links_kinks.html",
            role=kink_list_action,
            link=link,
            links=sorted(link_kinks, key=lambda x: x.kink_name),
            relationships=relationships,
            kink_list_action=kink_list_action,
        )
    raise NotImplementedError


@logged.route("/combined-kinks", methods=["POST"])
@login_required
def view_combined_kinks() -> str:
    user = cast(User, current_user)
    user_id = request.form.get("user_id")
    link_kinks = get_kinks(user_id, request.form.get("link_role"))
    user_kinks = user.get_kinks_for_role(request.form.get("view_relationship"))
    data: List[CombinedKink] = []
    print(len(kink_list))
    print(len(link_kinks))
    for kink in kink_list:
        user_kink = user_kinks.pop(0) if len(user_kinks) > 0 and user_kinks[0].kink_name == kink else None
        link_kink = link_kinks.pop(0) if len(link_kinks) > 0 and link_kinks[0].kink_name == kink else None
        if kink == "Cages (locked inside of)":
            print(kink)
            print(link_kink)
            print(link_kinks[0])
        if link_kink:
            assert link_kink.kink_name == kink
        data.append(CombinedKink(kink_name=kink, user_kink=user_kink, link_kink=link_kink))
    return render_template(
        "kinks_combined.html", user=user.username, link_user=cast(User, db.get_user_by_id(user_id)).username, kinks=data
    )


def get_kinks(user_id: Optional[str], role: Optional[str]) -> List[Kink]:
    if not user_id:
        raise NotImplementedError
    user = cast(User, db.get_user_by_id(user_id))
    return user.get_kinks_for_role(role)
