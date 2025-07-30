import logging
import os
import sys
import io
import boto3
from datetime import datetime
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Required environment variables
LOG_DESTINATION = os.getenv("LOG_DESTINATION")
LOG_S3_BUCKET = os.getenv("LOG_S3_BUCKET")
LOG_S3_KEY_TEMPLATE = os.getenv("LOG_S3_KEY_TEMPLATE")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH")
MAX_LOG_FILE_SIZE_KB = os.getenv("MAX_LOG_FILE_SIZE_KB")
UPLOAD_INTERVAL_SECONDS = os.getenv("UPLOAD_INTERVAL_SECONDS")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

# Validate required environment variables
required_env_vars = {
    "LOG_DESTINATION": LOG_DESTINATION,
    "LOG_FILE_PATH": LOG_FILE_PATH,
    "MAX_LOG_FILE_SIZE_KB": MAX_LOG_FILE_SIZE_KB,
    "UPLOAD_INTERVAL_SECONDS": UPLOAD_INTERVAL_SECONDS,
    "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
    "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
    "AWS_REGION": AWS_REGION,
}

if LOG_DESTINATION and LOG_DESTINATION.lower() == "s3":
    required_env_vars.update({
        "LOG_S3_BUCKET": LOG_S3_BUCKET,
        "LOG_S3_KEY_TEMPLATE": LOG_S3_KEY_TEMPLATE,
    })

missing_vars = [key for key, value in required_env_vars.items() if not value]
if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Convert env vars to appropriate types
MAX_LOG_FILE_SIZE_KB = int(MAX_LOG_FILE_SIZE_KB)
UPLOAD_INTERVAL_SECONDS = int(UPLOAD_INTERVAL_SECONDS)


class S3StreamHandler(logging.Handler):
    def __init__(self, bucket_name, key_template):
        super().__init__()
        self.bucket = bucket_name
        self.key_template = key_template
        self.log_stream = io.StringIO()

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        self._generate_new_key()
        self.last_upload_time = datetime.utcnow()

    def _generate_new_key(self):
        now = datetime.utcnow()
        self.current_key = now.strftime(self.key_template)

    def emit(self, record):
        try:
            log_entry = self.format(record)
            self.log_stream.write(log_entry + "\n")

            now = datetime.utcnow()
            if (now - self.last_upload_time).total_seconds() >= UPLOAD_INTERVAL_SECONDS:
                self._upload_logs()
                self.last_upload_time = now
                self._generate_new_key()
        except Exception as e:
            sys.__stderr__.write(f"[ERROR] Failed to write log entry: {e}\n")

    def _upload_logs(self):
        try:
            content = self.log_stream.getvalue()
            if content:
                self.s3_client.put_object(
                    Bucket=self.bucket,
                    Key=self.current_key,
                    Body=content.encode("utf-8")
                )
                self.log_stream = io.StringIO()
        except Exception as e:
            sys.__stderr__.write(f"[ERROR] Failed to upload logs to S3: {e}\n")

    def close(self):
        try:
            self._upload_logs()
        finally:
            super().close()


class StreamToLogger:
    def __init__(self, logger, level=logging.INFO):
        self.logger = logger
        self.level = level

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass


class LoggerConfigurator:
    def __init__(self, name="custom_logger"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.s3_handler = None
        self.local_handler = None

        self._setup_handler()
        self._redirect_print_to_logger()

    def _setup_handler(self):
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')

        if LOG_DESTINATION.lower() == "s3":
            self.s3_handler = S3StreamHandler(
                bucket_name=LOG_S3_BUCKET,
                key_template=LOG_S3_KEY_TEMPLATE
            )
            self.s3_handler.setFormatter(formatter)
            self.logger.addHandler(self.s3_handler)
        else:
            os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
            self.local_handler = RotatingFileHandler(
                LOG_FILE_PATH,
                maxBytes=MAX_LOG_FILE_SIZE_KB * 1024,
                backupCount=5
            )
            self.local_handler.setFormatter(formatter)
            self.logger.addHandler(self.local_handler)

    def _redirect_print_to_logger(self):
        sys.stdout = StreamToLogger(self.logger, logging.INFO)
        sys.stderr = StreamToLogger(self.logger, logging.ERROR)

    def get_logger(self):
        return self.logger

    def shutdown(self):
        if self.s3_handler:
            self.s3_handler.close()
        if self.local_handler:
            self.local_handler.close()
