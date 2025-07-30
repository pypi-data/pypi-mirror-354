import logging
import traceback
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from concurrent.futures import ThreadPoolExecutor
from Checks.Freshness_Check.freshness_check import FreshnessCheck
import signal
import sys
import time

class FreshnessMonitor:
    def __init__(self, config_loader, check_cfg, connector, check_id, alerting_enabled):
        self.connector = connector
        self.check_cfg = check_cfg
        self.check_id = check_id
        self.alerting_enabled = alerting_enabled
        self.config_loader = config_loader
        self.scheduler =   BackgroundScheduler({'apscheduler.timezone': 'Asia/Calcutta'})
        self.scheduler.add_listener(self._scheduler_listener, 
                          EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self.executor = ThreadPoolExecutor(max_workers=10)  # Adjust based on workload
        self.shutdown_flag = False

    def _run_check(self):
        try:
            check = FreshnessCheck(config_obj = self.config_loader, check_config=self.check_cfg, connector=self.connector)
            result = check.run(self.check_id,self.alerting_enabled)
            print(f"Freshness Check result: {result}")
        except Exception as e:
            print("Exception occurred in FreshnessCheck:")
            traceback.print_exc()


    def _scheduler_listener(self, event):
        if event.code == EVENT_JOB_EXECUTED:
            print(f"Job {event.job_id} executed successfully")
        elif event.code == EVENT_JOB_ERROR:
            print(f"Job {event.job_id} failed with exception: {event.exception}")

    def start(self):
        """Start the perpetual monitor."""
        try:
            signal.signal(signal.SIGINT, self.graceful_shutdown)
            signal.signal(signal.SIGTERM, self.graceful_shutdown)

            self.scheduler.add_job(
                self.executor.submit,
                'cron',
                args=[self._run_check],
                **self._parse_cron(self.check_cfg["expected_cron_schedule"])
            )

            for job in self.scheduler.get_jobs():
                print(f"Job: {job}")

            self.scheduler.start(paused=False)
            print("Freshness monitor started.")

            # Keep the main thread alive
            while not self.shutdown_flag:
                time.sleep(1)
        except Exception as e:
            print(e)
            raise e

    def _parse_cron(self, cron_expr: str):
        """Convert cron expression to APScheduler kwargs."""
        try:
            parts = cron_expr.split()
            return {
                "minute": parts[0],
                "hour": parts[1],
                "day": parts[2],
                "month": parts[3],
                "day_of_week": parts[4] if len(parts) > 4 else "*",
            }
        except Exception as e:
            print(e)
            raise e

    def graceful_shutdown(self, signum, frame):
        try:
            print("Shutting down gracefully...")
            self.shutdown_flag = True
            self.scheduler.pause()
            #self.executor.shutdown(wait=True)
            self.scheduler.shutdown()
            sys.exit(0)
        except Exception as e:
            print(e)
            raise e