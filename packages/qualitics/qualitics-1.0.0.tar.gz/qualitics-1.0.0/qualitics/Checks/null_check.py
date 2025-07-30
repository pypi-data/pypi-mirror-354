from qualitics.Checks.base import BaseCheck
from qualitics.Query_builder.PSQL_queries import QueryBuilder
from qualitics.Error.errorHandler import ThresholdConfigValidationError
import datetime

class NullCheck(BaseCheck):
    def run(self,check_id,alerting_enabled):
        try:
            results = []
            for column in self.config['columns']:
                query = QueryBuilder.null_check_query(self.config['database'], self.config['schema'], self.config['table'], column)
                null_pct = self.connector.run_query(query)[0]['null_pct']
                threshold_value = float(self.config.get('threshold')['max_null_percentage'])
                status = "fail" if null_pct > threshold_value else "pass"
                alert_status = "enabled" if (alerting_enabled and status == "fail") else "disabled"
                results.append({
                    "check_name": "null_check",
                    "database": self.config['database'],
                    "schema": self.config['schema'],
                    "table": self.config['table'],
                    "column": column,
                    "null_percentage": float(null_pct),
                    "threshold_value": threshold_value,
                    "check_status" : status,
                    "alert_status" : alert_status,
                    "checked_at": datetime.datetime.now().isoformat(),
                    "run_id": check_id
                })
            return results
        except Exception as e:
            print(e)
            raise e
