import logging
import os

from utf_queue_client.custom_exporter import CustomSpansExporter

DISABLE_SSL_VERIFICATION_DEFAULT = "true"
disable_utf_queue_client_traces = os.environ.get(
    "DISABLE_UTF_QUEUE_CLIENT_TRACES", "false"
).lower()
if disable_utf_queue_client_traces == "true":
    logger = logging.getLogger()
    default_custom_exporter = (
        f"{CustomSpansExporter.__module__}.{CustomSpansExporter.__name__}"
    )
    logger.info(
        f"Disabling the queue client traces for performance - {default_custom_exporter}"
    )
    os.environ["OTEL_EXPORTER_CUSTOM_SPAN_EXPORTER_TYPE"] = default_custom_exporter
