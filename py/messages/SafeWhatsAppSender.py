import pywhatkit as kit
from datetime import datetime, timedelta
import time
import json
import os
import random

class SafeWhatsAppSender:
    def __init__(self):
        """
        Initialize the Safe WhatsApp Sender with advanced settings.
        """
        # Session statistics to track usage
        self.session_stats = {
            'messages_sent': 0,          # Total messages sent in the session
            'last_session_time': None,   # Timestamp of the last message sent
            'daily_count': 0,            # Messages sent today
            'last_reset_date': datetime.now().date().isoformat()  # Date of the last reset
        }
        
        # Load previous session stats if available
        self.load_session_stats()

    def load_session_stats(self):
        """
        Load session statistics from a file if it exists.
        """
        if os.path.exists('session_stats.json'):
            with open('session_stats.json', 'r') as f:
                self.session_stats = json.load(f)
                
            # Reset daily count if it's a new day
            if self.session_stats['last_reset_date'] != datetime.now().date().isoformat():
                self.session_stats['daily_count'] = 0
                self.session_stats['last_reset_date'] = datetime.now().date().isoformat()

    def save_session_stats(self):
        """
        Save session statistics to a file.
        """
        with open('session_stats.json', 'w') as f:
            json.dump(self.session_stats, f)

    def smart_delay(self):
        """
        Apply intelligent delays between messages to avoid detection.
        """
        # Longer delay after every 10 messages
        if self.session_stats['messages_sent'] % 10 == 0:
            time.sleep(random.uniform(30, 60))
        else:
            # Random normal delay
            time.sleep(random.uniform(8, 15))
            
        # Additional delay if daily limit is exceeded
        if self.session_stats['daily_count'] > 50:
            time.sleep(random.uniform(60, 120))

    def check_limits(self):
        """
        Check and enforce message sending limits.
        """
        current_time = datetime.now()
        
        # Reset daily count if it's a new day
        if self.session_stats['last_reset_date'] != current_time.date().isoformat():
            self.session_stats['daily_count'] = 0
            self.session_stats['last_reset_date'] = current_time.date().isoformat()
            
        # Check daily and session limits
        if self.session_stats['daily_count'] >= 200:  # Daily limit
            raise Exception("Daily message limit exceeded.")
            
        if self.session_stats['messages_sent'] >= 30:  # Session limit
            waiting_time = random.uniform(3600, 7200)  # Wait 1-2 hours
            time.sleep(waiting_time)
            self.session_stats['messages_sent'] = 0

    def send_message_safely(self, phone_number, message, retries=1):
        """
        Send a message safely with all safety measures applied.
        """
        for attempt in range(retries):
            try:
                self.check_limits()
                
                # Send the message instantly
                kit.sendwhatmsg_instantly(phone_number, message)
                
                # Update session statistics
                self.session_stats['messages_sent'] += 1
                self.session_stats['daily_count'] += 1
                self.session_stats['last_session_time'] = datetime.now().isoformat()
                
                # Save stats and apply smart delay
                self.save_session_stats()
                self.smart_delay()
                
                return  # Exit the function if the message was sent successfully
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                time.sleep(10)  # Wait before retrying
                
        raise Exception("Failed to send message after retries.")

    def handle_error(self, error):
        """
        Handle errors intelligently.
        """
        if "block" in str(error).lower():
            # Wait for a long time if a potential block is detected
            waiting_hours = random.uniform(4, 8)
            print(f"Potential block detected. Waiting for {waiting_hours} hours...")
            time.sleep(waiting_hours * 3600)

    def send_bulk_messages_safely(self, numbers, message, max_per_day=50):
        """
        Send multiple messages safely with daily limits.
        """
        for i, number in enumerate(numbers):
            if i >= max_per_day:
                print("Daily limit reached.")
                break
                
            try:
                self.send_message_safely(number, message)
                
                # Distribute messages throughout the day
                if i % 10 == 0:
                    time.sleep(random.uniform(900, 1800))  # Wait 15-30 minutes
                    
            except Exception as e:
                print(f"Error sending message to {number}: {str(e)}")
                break

