from apscheduler.schedulers.blocking import BlockingScheduler
from rec import run_purchase_rec
import pytz
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

print("********************************************")
print("****************** START *******************")
print("********************************************")

def main():
    # Version log
    print("Version: 1.0.0")

    # Test env log
    db_connection = os.getenv("DB_CONNECTION")
    print(f"db_connection set to: {db_connection}")

    # Create a scheduler
    scheduler = BlockingScheduler()
    
    # Define the timezone (UTC+8)
    timezone = pytz.timezone('Asia/Shanghai')
    print(f"Timezone set to: {timezone}")
   
    # Get current time and add 1 minute
    current_time = datetime.now(timezone)
    run_time = current_time + timedelta(minutes=1)
    pHour = run_time.hour
    pMinute = run_time.minute
    print(f"Current time is: {current_time.strftime('%H:%M')}")
    print(f"Scheduled hour and minute set to: {pHour}:{pMinute}")

    # Schedule the run_recommendation function to run every day at 14:29 (2:29 PM) UTC+8
    scheduler.add_job(run_purchase_rec, 'cron', hour=pHour, minute=pMinute, timezone=timezone)

    # Start the scheduler
    print("Scheduler started. Waiting for jobs to run...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")
        pass

if __name__ == '__main__':
    main()
