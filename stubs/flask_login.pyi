from datetime import timedelta
from typing import Callable, Dict, Optional

from flask import Flask, Response
from werkzeug.local import LocalProxy
from werkzeug.wrappers import Response as BaseResponse

current_user: LocalProxy

class UserMixin:
    @property
    def is_active(self) -> bool: ...
    @property
    def is_authenticated(self) -> bool: ...
    @property
    def is_anonymous(self) -> bool: ...
    def get_id(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class AnonymousUserMixin:
    """
    This is the default object for representing an anonymous user.
    """

    @property
    def is_authenticated(self) -> bool: ...
    @property
    def is_active(self) -> bool: ...
    @property
    def is_anonymous(self) -> bool: ...
    def get_id(self) -> None: ...

class LoginManager:
    #: A class or factory function that produces an anonymous user, which
    #: is used when no one is logged in.
    anonymous_user: AnonymousUserMixin

    #: The name of the view to redirect to when the user needs to log in.
    #: (This can be an absolute URL as well, if your authentication
    #: machinery is external to your application.)
    login_view: Optional[str]

    #: Names of views to redirect to when the user needs to log in,
    #: per blueprint. If the key value is set to None the value of
    #: :attr:`login_view` will be used instead.
    blueprint_login_views: Dict[str, str]

    #: The message to flash when a user is redirected to the login page.
    login_message: str

    #: The message category to flash when a user is redirected to the login
    #: page.
    login_message_category: str

    #: The name of the view to redirect to when the user needs to
    #: reauthenticate.
    refresh_view = Optional[str]

    #: The message to flash when a user is redirected to the 'needs
    #: refresh' page.
    needs_refresh_message: str

    #: The message category to flash when a user is redirected to the
    #: 'needs refresh' page.
    needs_refresh_message_category: str

    #: The mode to use session protection in. This can be either
    #: ``'basic'`` (the default) or ``'strong'``, or ``None`` to disable
    #: it.
    session_protection: Optional[str]

    #: If present, used to translate flash messages ``login_message``
    #: and ``needs_refresh_message``
    localize_callback: Optional[Callable[[str], BaseResponse]]

    unauthorized_callback: Optional[Callable[[], BaseResponse]]

    needs_refresh_callback: Optional[Callable[[], BaseResponse]]

    id_attribute: str

    _user_callback: Optional[Callable[[str], Optional[object]]]

    _header_callback: Optional[Callable[[str], Optional[object]]]

    _request_callback: Optional[Callable[[object], Optional[object]]]

    _session_identifier_generator: Callable[[], str]

    def __init__(self, app: Optional[Flask] = ..., add_context_processor: bool = ...) -> None: ...
    def setup_app(self, app: Optional[Flask], add_context_processor: bool = ...) -> None: ...
    def init_app(self, app: Optional[Flask], add_context_processor: bool = ...) -> None: ...
    def unauthorized(self) -> BaseResponse: ...
    def user_loader(
        self, callback: Optional[Callable[[str], Optional[object]]]
    ) -> Optional[Callable[[str], Optional[object]]]: ...
    @property
    def user_callback(self) -> Optional[Callable[[str], Optional[object]]]: ...
    def request_loader(
        self, callback: Optional[Callable[[object], Optional[object]]]
    ) -> Optional[Callable[[object], Optional[object]]]: ...
    @property
    def request_callback(self) -> Optional[Callable[[object], Optional[object]]]: ...
    def unauthorized_handler(
        self, callback: Optional[Callable[[], BaseResponse]]
    ) -> Optional[Callable[[], BaseResponse]]: ...
    def needs_refresh_handler(
        self, callback: Optional[Callable[[], BaseResponse]]
    ) -> Optional[Callable[[], BaseResponse]]: ...
    def needs_refresh(self) -> BaseResponse: ...
    def header_loader(
        self, callback: Optional[Callable[[str], Optional[object]]]
    ) -> Optional[Callable[[str], Optional[object]]]: ...
    def _update_request_context_with_user(self, user: Optional[object] = ...) -> None: ...
    def _load_user(self) -> None: ...
    def _session_protection_failed(self) -> bool: ...
    def _load_user_from_remember_cookie(self, cookie: str) -> Optional[object]: ...
    def _load_user_from_header(self, header: str) -> Optional[object]: ...
    def _load_user_from_request(self, request: str) -> Optional[object]: ...
    def _update_remember_cookie(self, response: Response) -> Response: ...
    def _set_cookie(self, response: Response) -> None: ...
    def _clear_cookie(self, response: Response) -> None: ...
    @property
    def _login_disabled(self) -> bool: ...
    @_login_disabled.setter
    def _login_disabled(self, newvalue: bool) -> bool: ...

def login_required(func: Callable) -> Callable: ...
def login_user(
    user: object, remember: bool = ..., duration: Optional[timedelta] = ..., force: bool = ..., fresh: bool = ...
) -> bool: ...
def logout_user() -> bool: ...
