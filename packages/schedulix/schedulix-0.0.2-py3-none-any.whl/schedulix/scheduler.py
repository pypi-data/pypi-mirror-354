import schedule
import time
import pytz
import threading
import logging

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Define the log message format
    handlers=[
        logging.FileHandler("app.log"),  # Log messages to a file
        logging.StreamHandler()          # Log messages to the console
    ]
)

# Create a logger object
logger = logging.getLogger(__name__)

class Scheduler():

    def __init__(self, start_watering_cycle_thread, mode:str = 'dev'):
        self.activation_status = False
        self.start_watering_cycle_thread = start_watering_cycle_thread
        self.mode = mode


    timezone = pytz.timezone("Europe/Berlin")
    # Mapping days to schedule methods

    day_to_method = {
        'Monday': lambda: schedule.every().monday,
        'Tuesday': lambda: schedule.every().tuesday,
        'Wednesday': lambda: schedule.every().wednesday,
        'Thursday': lambda: schedule.every().thursday,
        'Friday': lambda: schedule.every().friday,
        'Saturday': lambda: schedule.every().saturday,
        'Sunday': lambda: schedule.every().sunday,
    }

    # To control the scheduling and interrupt it
    stop_scheduling = False


    def job(self):
        now = datetime.now(self.timezone).strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"{now}: Watering Cycle Started from Scheduler")
        self.start_watering_cycle_thread()

    # Function to schedule jobs based on the activation status and day

    def schedule_jobs(self, schedule_settings: list):

        if self.mode in ['live', 'dev-live']:
            for item in schedule_settings:
                if item["activation_status"] == 1:
                    day_method = self.day_to_method.get(item['day'])()
                    if day_method:
                        day_method.at(item['time'], self.timezone).do(self.job)
                        logger.debug(f"Job scheduled for {item['day']} at {item['time']}")
                    else:
                        raise ValueError(f"methode not existing for {item}")

        elif self.mode == 'dev':
            schedule.every(1).minutes.do(self.job)
        else:
            raise ValueError(f"Unknown mode in schedule_jobs()")



    def deactivate_schedule(self):
        schedule.clear()
        self.stop_scheduling = True
        logger.info("Schedules cleared")

    def activate_schedule(self, schedule_settings: list):
        self.schedule_jobs(schedule_settings)
        self.stop_scheduling = False
        threading.Thread(target=self.run_schedule).start()
        logger.info(schedule.get_jobs())

    def run_schedule(self):
        while not self.stop_scheduling:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    from datetime import datetime, timedelta
    def plustime(add: int):
        current_time = datetime.now()
        t_plus = current_time + timedelta(seconds=add)
        t_plus = t_plus.strftime("%H:%M:%S")
        return t_plus


    schedule_settings = [
        {"day": "Friday", "time": plustime(2), "activated": 1},
        {"day": "Friday", "time": plustime(3), "activated": 0},
        {"day": "Friday", "time": plustime(5), "activated": 1},
        {"day": "Friday", "time": plustime(7), "activated": 1}
        # Add other entries as needed
    ]
    scheduler = Scheduler()
    scheduler.activate_schedule(schedule_settings)
    time.sleep(7)
    scheduler.deactivate_schedule()
