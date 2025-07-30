import os
import boto3
import json
from dotenv import load_dotenv

class CredentialManager:
    def __init__(self, credential_config):
        self.config = credential_config

    def get_credentials(self):
        try:
            method = self.config['connection']['environment']
            print(f"Getting db credentials from {method}")
            if method == "env_variable":
                load_dotenv()
                return {
                    "host": os.getenv(self.config['connection']['host']),
                    "port": int(os.getenv(self.config['connection']['port'])),
                    "dbname": os.getenv(self.config['connection']['database']),
                    "username": os.getenv(self.config['connection']['user']),
                    "password": os.getenv(self.config['connection']['password']),
                }

            elif method == "secrets_manager":
                return self._get_secret_manager_creds(self.config['connection'])
            else:
                raise ValueError(f"Unknown credential type: {method}")
        except Exception as e:
            print(e)
            raise e

    def get_smtp_credentials(self, channel_type='email'):
        """Get SMTP credentials from configured source"""
        try:
            smtp_config = None
            for channel in self.config['alerts']['channels']:
                if channel.get('type') == 'email' and 'sender_creds' in channel:
                    smtp_config = channel['sender_creds']
                    break
                
            if not smtp_config:
                raise ValueError("SMTP configuration not found in alerts channels")
                
            method = smtp_config['environment']
            print(f"Getting SMTP credentials from {method}")
            
            if method == "env_variable":
                load_dotenv()
                return {
                    "server": os.getenv(smtp_config['server']),
                    "port": int(os.getenv(smtp_config['port'])),
                    "username": os.getenv(smtp_config['username']),
                    "password": os.getenv(smtp_config['password'])
                }
            elif method == "secrets_manager":
                secret = self._get_secret_manager_creds(smtp_config)
                return {
                    "server": secret[smtp_config['server']],
                    "port": int(secret[smtp_config['port']]),
                    "username": secret[smtp_config['username']],
                    "password": secret[smtp_config['password']]
                }
            else:
                raise ValueError(f"Unknown SMTP credential type: {method}")
        except Exception as e:
            print(f"Error getting SMTP credentials: {e}")
            raise e

    def get_slack_webhook_url(self, channel_type='slack'):
        """Get Slack webhook URL from configured source (env vars or Secrets Manager)"""
        try:
            # Look for Slack config in alerts channels
            slack_config = None
            if 'alerts' in self.config and 'channels' in self.config['alerts']:
                for channel in self.config['alerts']['channels']:
                    if channel.get('type') == 'slack' and 'slack_webhook' in channel:
                        slack_config = channel['slack_webhook']
                        break
                
            if not slack_config:
                raise ValueError("Slack configuration not found in credentials config")
                
            method = slack_config['environment']
            print(f"Getting Slack webhook URL from {method}")
            
            if method == "env_variable":
                load_dotenv()
                return os.getenv(slack_config.get('url', 'SLACK_WEBHOOK_URL'))
            elif method == "secrets_manager":
                secret = self._get_secret_manager_creds(slack_config)
                return secret[slack_config.get('url', 'slack_webhook_url')]
            else:
                raise ValueError(f"Unknown Slack credential type: {method}")
        except Exception as e:
            print(f"Error getting Slack webhook URL: {e}")
            raise e

    def _get_secret_manager_creds(self, config):
        """Helper method to get credentials from Secrets Manager"""
        try:
            secret_arn = config["secret_arn"]
            region = config["region"]
            client = boto3.client("secretsmanager", region_name=region)
            secret_value = client.get_secret_value(SecretId=secret_arn)
            return json.loads(secret_value["SecretString"])
        except Exception as e:
            print(f"Error retrieving from Secrets Manager: {e}")
            raise e