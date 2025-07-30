import yaml
import boto3
from io import StringIO
from botocore.exceptions import NoCredentialsError, ClientError, BotoCoreError
from typing import Dict, List, Optional, Any
from  qualitics.Error.errorHandler import (
    ConfigLoadError,
    ConfigValidationError,
    MissingSectionError,
    InvalidChecksError

)
import sys

class ConfigLoader:
    _instance = None
    _config = None

    REQUIRED_STRUCTURE = {
                            "data_source": {
                                "required_keys": ["type", "connection", "query"],
                                "nested": {
                                    "connection": {
                                        "required_keys": ["environment", "host", "port", "database", "user", "password"]
                                    }
                                }
                            },
                            "checks": {
                                "validation_function": "validate_checks"  # Special handling
                            }
                        }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance

    def load_config(self, file_path, aws_access_key=None, aws_secret_key=None):
        def is_s3_path(path):
            return path.startswith("s3://")

        def read_local_yaml(path):
            try:
                with open(path, 'r') as file:
                    return yaml.safe_load(file)
            except Exception as e:
                raise ConfigLoadError(f"Error reading local YAML file: {e}")

        def read_s3_yaml(path):
            try:
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key
                ) if aws_access_key else boto3.client('s3')

                bucket, key = path.replace("s3://", "").split("/", 1)
                obj = s3.get_object(Bucket=bucket, Key=key)
                return yaml.safe_load(StringIO(obj['Body'].read().decode('utf-8')))
            except (ClientError, NoCredentialsError, BotoCoreError) as e:
                raise ConfigLoadError(f"Error reading S3 YAML file: {e}")

        try:
            self._config = read_s3_yaml(file_path) if is_s3_path(file_path) else read_local_yaml(file_path)
            self._validate_yaml_config()
            return self._config
        except (ConfigLoadError, ConfigValidationError, MissingSectionError, InvalidChecksError) as e:
            print(e)
            sys.exit(0)
            #self._config = {}

    def get_config(self):
        return self._config if self._config is not None else {}

    def _validate_config_section(self, section_path, requirements):
        """Validate a single configuration section"""
        errors = []
        current = self._config

        # Navigate through nested sections
        for section in section_path.split('.'):
            if section not in current:
                raise MissingSectionError(section_path)
            current = current[section]

        # Check required keys
        for key in requirements.get("required_keys", []):
            if key not in current:
                raise MissingSectionError(section_path + "." + key)

        # Recursively check nested sections
        for nested_section, nested_reqs in requirements.get("nested", {}).items():
            if nested_section in current:
                nested_path = f"{section_path}.{nested_section}" if section_path else nested_section
                self._validate_config_section(nested_path, nested_reqs)

    @staticmethod
    def _validate_checks(checks_config):
        """Special validation for checks section"""
        CHECK_REQUIREMENTS = {
            "null_check": {"required": ["columns", "threshold"], "threshold": ["max_null_percentage"]},
            "pii_check": {"required": ["columns"]},
            "row_count_check": {"required": ["threshold"], "threshold": ["expected_range"]},
            "custom_sql_check": {"required": ["query", "threshold"], "threshold": ["acceptable_condition"]},
            "freshness_check": {"required": ["expected_cron_schedule", "time_tolerance_minutes"]}
        }
        for i, check in enumerate(checks_config, 1):
            check_name = check.get("name")
            if not check_name:
                raise InvalidChecksError(f"Name is not defined in config for check {i}!")

            if check_name not in CHECK_REQUIREMENTS:
                raise InvalidChecksError(f"{check_name} is not valid, please check the allowed check names!")

            # Validate common fields
            common_fields = ["database", "schema", "table"]
            for field in common_fields:
                if field not in check:
                    raise InvalidChecksError(f"{field} is missing or misspelt for {check_name} in config!")

            # Validate type-specific fields
            for field in CHECK_REQUIREMENTS[check_name]["required"]:
                if field not in check:
                    raise InvalidChecksError(f"{field} is missing or misspelt for {check_name} in config!")

            # Validate threshold fields if present
            if "threshold" in CHECK_REQUIREMENTS[check_name]:
                for field in CHECK_REQUIREMENTS[check_name]["threshold"]:
                    if field not in check["threshold"]:
                        raise InvalidChecksError(
                            f"{field} is missing or misspelt in threshold section for {check_name} in config!")

    def _validate_yaml_config(self):
        """Main validation function"""
        # Validate top-level sections
        for section, requirements in self.REQUIRED_STRUCTURE.items():
            if section == "checks" and "validation_function" in requirements:
                if section in self._config:
                    checks_confg = self._config[section]
                    self._validate_checks(checks_confg)
                else:
                    raise MissingSectionError(section)
            else:
                self._validate_config_section(section, requirements)
        
        #Audit section (optional, but if present, must have required keys)
        if 'audit' in self._config:
            audit = self._config['audit']
            required_audit_keys = ['enabled', 'database']
            for key in required_audit_keys:
                if key not in audit:
                    raise MissingSectionError("audit"+"."+key)
            if 'database' in audit:
                db_keys = ['type', 'connection']
                for key in db_keys:
                    if key not in audit['database']:
                        raise MissingSectionError("database"+"."+key)
                if 'connection' in audit['database']:
                    conn_keys = ['host', 'port', 'database', 'user', 'password']
                    for key in conn_keys:
                        if key not in audit['database']['connection']:
                            raise MissingSectionError("database"+"."+"connection"+"."+key)

        #Alerts section (optional, but if present, must have email or slack with required keys)
        if 'alerts' in self._config:
            alerts = self._config['alerts']
            if 'enabled' not in alerts:
                raise MissingSectionError("alerts.enabled")
            if 'channels' not in alerts or not alerts['channels']:
                raise MissingSectionError("alerts.channels")
            else:
                for channel in alerts['channels']:
                    if 'type' not in channel:
                        raise MissingSectionError("alerts.channels.type")
                    elif channel['type'] == 'email':
                        if 'recipients' not in channel or not channel['recipients']:
                            raise MissingSectionError("alerts.channels.email.recipients")
                    elif channel['type'] == 'slack':
                        # Check slack webhook configuration
                        if 'slack_webhook' not in channel:
                            raise MissingSectionError("alerts.channels.slack.slack_webhook")
                        else:
                            webhook = channel['slack_webhook']
                            if 'environment' not in webhook or 'url' not in webhook:
                                raise MissingSectionError("alerts.channels.slack.slack_webhook.environment or url")
                            
                        # Check channel name
                        if 'channel_name' not in channel:
                            raise MissingSectionError("alerts.channels.slack.channel_name")
                        
                        ''' slack_keys = ['webhook_url', 'channel_name']
                        for key in slack_keys:
                            if key not in channel:
                                raise MissingSectionError("alerts.channels.slack"+"."+key)'''
 
        #Profiling section (optional, but if present, must have required keys)
        if 'profiling' in self._config:
            profiling = self._config['profiling']
            profiling_keys = ['profiling_schema', 'profiling_database']
            for key in profiling_keys:
                if key not in profiling:
                    raise MissingSectionError("profiling"+"."+key)

