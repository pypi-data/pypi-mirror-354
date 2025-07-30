from qualitics.Checks.null_check import NullCheck
from qualitics.Checks.pii_check import PiiChecker
from qualitics.Checks.row_count_check import RowCountCheck
from qualitics.Checks.custom_sql_check import CustomSQLCheck


CHECK_MAPPING = {
     "null_check": NullCheck,
    "pii_check": PiiChecker,
     "row_count_check" : RowCountCheck,
     "custom_sql_check" : CustomSQLCheck
}

class CheckRunner:
    def __init__(self, full_config, connector, check_id, alerting_enabled):
        self.full_config = full_config
        self.connector = connector
        self.check_id = check_id
        self.alerting_enabled = alerting_enabled

    def run_all(self):
        results = []
        for check_cfg in self.full_config['checks']:
            check_name = check_cfg['name']

            check_class = CHECK_MAPPING.get(check_name)

            if check_class:
                print(f"{check_class} is configured based on config file")
                check_instance = check_class(self.connector, check_cfg)
                results.extend(check_instance.run(self.check_id, self.alerting_enabled))
            else:
                print(f"No mapping configured for specified check - {check_name}!")
        return results

    def run_selected(self, selected_check_names):
            # print("running selected checks.........")
            results = []
            for check_cfg in self.full_config['checks']:
                check_name = check_cfg['name']
                if check_name in selected_check_names:
                    check_class = CHECK_MAPPING.get(check_name)
                    # print(f"{check_class} is configured based on config file")
                    if check_class:
                        check_instance = check_class(self.connector, check_cfg)
                        results.extend(check_instance.run(self.check_id, self.alerting_enabled))
                    else:
                        print(f"No mapping configured for specified check - {check_name}!")
            return results



