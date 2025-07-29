from batch_executor.custom_logger import setup_logger

logger = setup_logger(
    name="batch_executor",
    log_file=None,  # Set to None to disable file logging
    console=True,
    log_level="INFO",
    file_log_level=None,
    console_log_level="INFO",
    format_type="detailed",
    file_mode="w",
    encoding="utf-8",
    colored=True
)