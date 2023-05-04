import logging
from typing import Callable

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils import timezone as django_timezone
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError

LOGGER = logging.getLogger('django.server')


class TimezoneMiddleware:
    """
    Middleware that sets the time zone for the user based on the city they have chosen.
    """

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def _set_default_tz(self, request: HttpRequest) -> None:
        request.timezone = timezone(settings.TIME_ZONE)

    def __call__(self, request: HttpRequest) -> HttpResponse:
        logger = LOGGER
        user = request.user

        if user.is_authenticated:

            try:
                tz = timezone(user.profile.city.timezone)
                django_timezone.activate(tz)
                request.timezone = tz

                logger.info('"%s" timezone: %s', str(request.method), str(tz))

            except UnknownTimeZoneError:
                logger.warning('Unknown timezone error')
                django_timezone.deactivate()
                self._set_default_tz(request)

            except AttributeError:
                django_timezone.deactivate()
                self._set_default_tz(request)
        else:
            self._set_default_tz(request)

        response = self.get_response(request)
        return response
