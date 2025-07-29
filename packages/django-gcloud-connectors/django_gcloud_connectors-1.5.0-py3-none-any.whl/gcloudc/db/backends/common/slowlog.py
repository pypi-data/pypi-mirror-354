import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def log_unscalable_query(query, additional_message=None):
    if not settings.DEBUG:
        return

    logger.warning(
        "Query is not scalable: %s. "
        "This will not scale and should be avoided in production if possible. Consider providing a limit to the query.",
        query,
    )

    if additional_message:
        logger.warning(additional_message)
