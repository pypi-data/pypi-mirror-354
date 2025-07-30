# notification/notification_service.py
import smtplib
import requests
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Connectors.credential_manager import CredentialManager
from typing import Dict, List
from Error.errorHandler import (
    NotificationError,
    ChannelValidationError
)

class NotificationChannel:
    """Base class for notification channels"""
    
    def __init__(self, config: Dict, credential_manager: CredentialManager):
        self.config = config
        self.credential_manager = credential_manager
    
    def send(self, check_result: Dict) -> Dict:
        """Send notification for a check result"""
        raise NotImplementedError()
    
    def _should_send(self, check_result: Dict) -> bool:
        """Determine if notification should be sent"""
        return (check_result.get('check_status') == 'fail' and 
                check_result.get('alert_status') == 'enabled')

    def _get_database_info(self, check_result: Dict) -> str:
        """Format database information for notifications"""
        db_info = []
        if check_result.get('database'):
            db_info.append(f"Database: {check_result['database']}")
        if check_result.get('schema'):
            db_info.append(f"Schema: {check_result['schema']}")
        if check_result.get('table'):
            db_info.append(f"Table: {check_result['table']}")
        if check_result.get('column'):
            db_info.append(f"Column: {check_result['column']}")
        return "\n".join(db_info) if db_info else "Location: Unknown"
    
    def _mask_string(self, s: str) -> str:
        """Mask a string to show only first and last characters"""
        if len(s) <= 2:
            return s
        return s[0] + '*' * (len(s) - 2) + s[-1]

    def _mask_matches(self, matches: List[str]) -> List[str]:
        """Mask all matches using _mask_string"""
        return [self._mask_string(match) for match in matches]


class EmailNotificationChannel(NotificationChannel):
    """Email notification channel implementation"""
    
    def __init__(self, config: Dict, credential_manager: CredentialManager):
        super().__init__(config, credential_manager)
        self.recipients = config.get('recipients', [])
        
        if not isinstance(self.recipients, list):
            raise ChannelValidationError("Recipients must be a list")
        if not self.recipients:
            raise ChannelValidationError("No recipients configured")
        
    def send(self, check_result: Dict) -> Dict:
        """Send email notification"""
        if not self._should_send(check_result):
            return {
                'sent': False,
                'channel': 'email',
                'reason': 'Notification not required'
            }
        
        try:
            # Use the credential manager to get SMTP credentials
            smtp_creds = self.credential_manager.get_smtp_credentials('email')
            
            msg = MIMEMultipart()
            msg["Subject"] = f"Data Quality Alert: Failed {check_result.get('check_name')} Check"
            msg["From"] = smtp_creds['username']
            msg["To"] = ", ".join(self.recipients)
            
            body = self._format_message(check_result)
            msg.attach(MIMEText(body, "plain"))
            
            with smtplib.SMTP(smtp_creds['server'], smtp_creds['port']) as server:
                server.starttls()
                server.login(smtp_creds['username'], smtp_creds['password'])
                server.send_message(msg)
            
            return {
                'sent': True,
                'channel': 'email',
                'recipients': self.recipients
            }
        except Exception as e:
            raise NotificationError("Failed to send email notification") from e

            
    
    def _format_message(self, check_result: Dict) -> str:
        """Format check result into email message"""
        message = [
            "A data quality check has failed with the following details:\n",
            f"Check: {check_result.get('check_name', 'Unknown')}",
            self._get_database_info(check_result),
            f"Status: {check_result.get('check_status', 'Unknown')}",
            f"Run ID: {check_result.get('run_id', 'Unknown')}",
            f"Checked At: {check_result.get('checked_at', 'Unknown')}\n"
        ]
        
        # Add check-specific details
        check_name = check_result.get('check_name')
        if check_name == 'null_check':
            message.extend([
                f"Null Percentage: {check_result.get('null_percentage')}%",
                f"Threshold: {check_result.get('threshold_value')}%"
            ])
        elif check_name == 'pii_check':
            message.append(f"PII Type: {check_result.get('pii_type', 'Unknown')}")
            if 'matches' in check_result:
                message.append(f"Matches: {', '.join(self._mask_matches(check_result['matches']))}")
        elif check_name == 'row_count_check':
            threshold = check_result.get('threshold_value', {})
            message.extend([
                f"Current Row Count: {check_result.get('current_row_count')}",
                f"Threshold: Min {threshold.get('min', 'N/A')}, Max {threshold.get('max', 'N/A')}"
            ])
        elif check_name == 'custom_sql_check':
            message.extend([
                f"Violation Count: {check_result.get('result_summary', {}).get('violation_count', 0)}",
                f"Query: {check_result.get('query', 'N/A')}",
                f"Condition: {check_result.get('threshold_condition', 'N/A')}"
            ])
        elif check_name == 'freshness_check':
            message.extend([
                f"Previous Row Count: {check_result.get('previous_row_count', 'N/A')}",
                f"Current Row Count: {check_result.get('current_row_count', 'N/A')}",
                f"Cron Schedule: {check_result.get('cron_schedule', 'N/A')}"
            ])
        
        message.append("\nThis is an automated notification from the Data Quality monitoring system.")
        return "\n".join(message)


class SlackNotificationChannel(NotificationChannel):
    """Slack notification channel implementation"""
    
    def __init__(self, config: Dict, credential_manager: CredentialManager):
        super().__init__(config, credential_manager)
        self.channel_name = config.get('channel_name', 'all-dqalerts')
        
    def send(self, check_result: Dict) -> Dict:
        """Send Slack notification"""
        if not self._should_send(check_result):
            return {
                'sent': False,
                'channel': 'slack',
                'reason': 'Notification not required'
            }
        
        try:
            # Use the credential manager to get Slack webhook URL
            webhook_url = self.credential_manager.get_slack_webhook_url('slack')
            payload = self._build_slack_payload(check_result)
            
            response = requests.post(
                webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code != 200:
                raise NotificationError(f"Slack API error: {response.text}")
            
            return {
                'sent': True,
                'channel': 'slack',
                'recipients': self.channel_name
            }
        except Exception as e:
            raise NotificationError("Failed to send Slack notification") from e
    
    def _build_slack_payload(self, check_result: Dict) -> Dict:
        """Build Slack message payload"""
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f":warning: Data Quality Alert: {check_result.get('check_name')}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": self._get_database_info(check_result)
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Status:*\n{check_result.get('check_status', 'Unknown')}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Run ID:*\n{check_result.get('run_id', 'Unknown')}"
                    }
                ]
            }
        ]
        
        # Add check-specific details
        details = []
        check_name = check_result.get('check_name')
        if check_name == 'null_check':
            details.extend([
                f"*Null Percentage:* {check_result.get('null_percentage')}%",
                f"*Threshold:* {check_result.get('threshold_value')}%"
            ])
        elif check_name == 'pii_check':
            details.append(f"*PII Type:* {check_result.get('pii_type', 'Unknown')}")
            if 'matches' in check_result:
                details.append(f"*Matches:* {', '.join(self._mask_matches(check_result['matches']))}")
        elif check_name == 'row_count_check':
            threshold = check_result.get('threshold_value', {})
            details.extend([
                f"*Row Count:* {check_result.get('current_row_count')}",
                f"*Threshold:* Min {threshold.get('min', 'N/A')}, Max {threshold.get('max', 'N/A')}"
            ])
        elif check_name == 'custom_sql_check':
            details.extend([
                f"*Violations:* {check_result.get('result_summary', {}).get('violation_count', 0)}",
                f"*Query:* {check_result.get('query', 'N/A')}"
            ])
        elif check_name == 'freshness_check':
            details.extend([
                f"*Previous Count:* {check_result.get('previous_row_count', 'N/A')}",
                f"*Current Count:* {check_result.get('current_row_count', 'N/A')}",
                f"*Schedule:* {check_result.get('cron_schedule', 'N/A')}"
            ])
        
        if details:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "\n".join(details)
                }
            })
        
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Checked At: {check_result.get('checked_at', 'Unknown')}"
                }
            ]
        })
        
        return {
            "channel": self.channel_name,
            "blocks": blocks,
            "text": f"Data Quality Alert: Failed {check_result.get('check_name')} Check"
        }


class NotificationService:
    """Service to handle notifications for data quality check results"""
    
    def __init__(self, full_config: Dict, credential_manager: CredentialManager):
        """
        Initialize NotificationService with complete configuration and credential manager.
        
        Args:
            full_config: Complete YAML configuration containing alerts section
            credential_manager: Pre-initialized CredentialManager instance
        """
        self.config = full_config
        self.alerts_config = full_config.get("alerts", {})
        # Use the passed credential manager instead of creating a new one
        self.credential_manager = credential_manager
        self.channels = self._initialize_channels()
    
    def _initialize_channels(self) -> List[NotificationChannel]:
        """Initialize notification channels based on config"""
        channels = []
        
        for channel_config in self.alerts_config.get("channels", []):
            channel_type = channel_config.get("type")
            if channel_type == "email":
                channels.append(EmailNotificationChannel(channel_config, self.credential_manager))
            elif channel_type == "slack":
                channels.append(SlackNotificationChannel(channel_config, self.credential_manager))
        
        return channels
    
    def notify(self, check_result: Dict) -> Dict:
        """Send notifications through all configured channels"""
        if not self.alerts_config.get("enabled", False):
            return {
                **check_result,
                'alert_sent': 'no',
                'alerted_via': None
            }
        
        notification_results = []
        updated_check_result = check_result.copy()
        
        for channel in self.channels:
            try:
                result = channel.send(check_result)
                if result.get('sent'):
                    notification_results.append({
                        'channel': result['channel'],
                        'recipients': result.get('recipients', result.get('recipient'))
                    })
            except NotificationError as e:
                print(f"Notification error ({channel.__class__.__name__}): {str(e)}")
                if e.__cause__:
                    print(f"Original error: {str(e.__cause__)}")
                continue

        if notification_results:
            updated_check_result.update({
                'alert_sent': 'yes',
                'alerted_via': {r['channel']: r['recipients'] for r in notification_results}
            })
        else:
            updated_check_result.update({
                'alert_sent': 'no',
                'alerted_via': None
            })
        
        return updated_check_result