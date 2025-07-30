from croniter import croniter
from Checks.base import BaseCheck
from Query_builder.PSQL_queries import QueryBuilder
import time
import datetime
import uuid


class FreshnessCheck(BaseCheck):
    def __init__(self, config_obj, connector, check_config):
        self.connector = connector
        self.config = config_obj
        self.table = check_config["table"]
        self.database = check_config["database"]
        self.schema = check_config["schema"]
        self.check_name = "freshness_check"
        self.cron_schedule = check_config["expected_cron_schedule"]
        self.check_window = check_config["time_tolerance_minutes"]

    def get_row_count(self):
        try:
            query = QueryBuilder.row_count_check_query(self.database, self.schema, self.table)
            row_cnt = self.connector.run_query(query)[0]['row_cnt']
            return row_cnt if row_cnt else 0
        except Exception as e:
            print(e)
            raise e

    def get_next_cron_window(self):
        try:
            now = datetime.datetime.now()
            iter = croniter(self.cron_schedule, now)
            
            # Get previous and next runs
            prev_run = iter.get_prev(datetime.datetime)
            next_run = iter.get_next(datetime.datetime)
            
            # If previous run + check window is still in the future, use that
            prev_run_end = prev_run + datetime.timedelta(minutes=self.check_window)
            if now < prev_run_end:
                # We're still within the check window of the previous run
                start_window = prev_run - datetime.timedelta(minutes=self.check_window)
                end_window = prev_run_end
            else:
                # Otherwise use next run's window
                start_window = next_run - datetime.timedelta(minutes=self.check_window)
                end_window = next_run + datetime.timedelta(minutes=self.check_window)
            
            return start_window, end_window
        except Exception as e:
            print(e)
            raise e

    def run(self, check_id, alerting_enabled):
        try:
            start_window, end_window = self.get_next_cron_window()
            print(f"{self.database}.{self.schema}.{self.table} Monitoring for refresh between {start_window} and {end_window}")

            # Metadata before
            before_row_count = self.get_row_count()
            print(f"Initial row count for {self.database}.{self.schema}.{self.table} at {datetime.datetime.now()} found to be {before_row_count}")

            # Wait until start of monitoring window
            while datetime.datetime.now() < start_window:
                time.sleep(30)

            refreshed = False
            check_interval = 30

            while datetime.datetime.now() < end_window:
                print("Within monitoring window. Polling for row count changes..")
                time.sleep(check_interval)

                current_row_count = self.get_row_count()
                print(f"Row count for {self.database}.{self.schema}.{self.table} at {datetime.datetime.now()} found to be {current_row_count}")

                if current_row_count != before_row_count:
                    print(f"{self.database}.{self.schema}.{self.table} found to be refreshed around {datetime.datetime.now()} as seen in row count difference.")
                    refreshed = True

                if refreshed:
                    break
            
            status = "fail" if not refreshed else "pass"
            alert_status = "enabled" if (alerting_enabled and status == "fail") else "disabled"

            if refreshed:        
                result = {
                    "check_name": self.check_name,
                    "table": self.table,
                    "database": self.database,
                    "cron_schedule": self.cron_schedule,
                    "check_status" : status,
                    "alert_status" : alert_status,
                    "previous_row_count": before_row_count,
                    "current_row_count": current_row_count if refreshed else before_row_count,
                    "checked_at": datetime.datetime.now().isoformat(),
                    "run_id": check_id
                }
            else:
                print(f"{self.database}.{self.schema}.{self.table} was not found to be refreshed within {start_window} and {end_window}!")
                result = {
                "check_name": self.check_name,
                "table": self.table,
                "database": self.database,
                "cron_schedule": self.cron_schedule,
                "check_status" : status,
                "alert_status" : alert_status,
                "previous_row_count": before_row_count,
                "current_row_count": current_row_count if refreshed else before_row_count,
                "checked_at": datetime.datetime.now().isoformat(),
                "run_id": check_id
                }

            return [result]
        except Exception as e:
            print(e)
            raise e