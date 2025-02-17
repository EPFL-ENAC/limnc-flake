from apscheduler.schedulers.background import BackgroundScheduler
from tenacity import retry, stop_after_attempt, wait_fixed
import logging
import time

# Configure logging
logging.basicConfig(
    filename='data_processing.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Define the pipeline
@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def process_data():
    try:
        print("Step 1: Extracting data...")
        time.sleep(1)  # Simulate work
        print("Step 2: Transforming data...")
        time.sleep(1)
        # Simulate an error
        if time.time() % 2 < 1:  
            raise ValueError("Random simulated error!")
        print("Step 3: Loading data...")
        time.sleep(1)
        print("Pipeline finished successfully.")
    except Exception as e:
        logging.error("Pipeline failed", exc_info=True)
        raise

# Schedule the pipeline
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_data, 'interval', minutes=1)  # Run every minute
    scheduler.start()

    print("Scheduler started. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.")