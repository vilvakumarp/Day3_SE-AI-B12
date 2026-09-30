import os
import time
import json
import random
from datetime import datetime
import pandas as pd

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Configuration constants
EXCEL_FILE = "contacts.xlsx"
SESSION_DIR = "whatsapp_session"

def create_sample_excel_if_missing():
    """Creates a sample contacts.xlsx file if it doesn't exist for easy testing."""
    if not os.path.exists(EXCEL_FILE):
        data = {
            "Name": ["John Doe", "Jane Smith"],
            "Phone": ["+919876543210", "+919123456789"],
            "Message": ["Hello {name}, this is an automated daily update.", "Hi {name}, checking in on your business inquiry."]
        }
        df = pd.DataFrame(data)
        df.to_excel(EXCEL_FILE, index=False)
        print(f"[INFO] Created sample '{EXCEL_FILE}' file. Please update it with real numbers before running production.")

def human_delay(min_sec=2, max_sec=5):
    """Introduces human-like random pauses to avoid being flagged or banned."""
    delay = random.uniform(min_sec, max_sec)
    time.sleep(delay)

def run_whatsapp_bot():
    create_sample_excel_if_missing()
    
    # Read contacts from Excel
    try:
        df_contacts = pd.read_excel(EXCEL_FILE)
    except Exception as e:
        print(f"[ERROR] Could not read {EXCEL_FILE}: {e}")
        return

    report_data = []
    today_str = datetime.now().strftime("%Y-%m-%d")

    with sync_playwright() as p:
        # Launch persistent context to save login session (avoids scanning QR code every time)
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False,
            args=["--start-maximized"],
            viewport=None
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        print("[INFO] Opening WhatsApp Web...")
        page.goto("https://web.whatsapp.com")
        
        # Wait for WhatsApp Web to load by checking for the main chat list pane
        print("[INFO] Please scan the QR code if prompted. Waiting for chat list...")
        try:
            page.wait_for_selector("div[contenteditable='true'][data-tab='3']", timeout=60000)
            print("[INFO] Successfully logged in to WhatsApp Web!")
        except PlaywrightTimeoutError:
            print("[ERROR] Login timeout. Please ensure you scan the QR code within the time limit.")
            browser.close()
            return

        for index, row in df_contacts.iterrows():
            name = str(row['Name'])
            phone = str(row['Phone'])
            template = str(row.get('Message', 'Hello {name}'))
            
            # Personalize message
            message = template.replace("{name}", name)
            
            status = "Failed"
            error_msg = ""
            screenshot_path = ""
            extracted_messages = []

            print(f"\n[PROCESSING] Contact {index+1}: {name} ({phone})")

            try:
                # 1. Search for contact using the search bar
                search_box = page.locator("div[contenteditable='true'][data-tab='3']")
                search_box.click()
                search_box.fill("")
                human_delay(1, 2)
                
                # Type phone number or name
                search_box.type(phone, delay=100)
                human_delay(2, 4)

                # Wait for search results / contact item to appear
                # WhatsApp Web usually displays the contact in a pane below search
                contact_selector = f"span[title='{phone}'], span[title='{name}'], div[role='gridcell']"
                
                try:
                    page.wait_for_selector(contact_selector, timeout=8000)
                    page.locator(contact_selector).first.click()
                    human_delay(2, 3)
                except PlaywrightTimeoutError:
                    raise Exception("Contact not found in search results.")

                # 2. Type and send the personalized message
                # Locate message input box (contenteditable div with data-tab="10")
                message_box_selector = "div[contenteditable='true'][data-tab='10']"
                page.wait_for_selector(message_box_selector, timeout=5000)
                message_box = page.locator(message_box_selector)
                
                message_box.click()
                message_box.fill(message)
                human_delay(1, 2)
                
                # Press Enter to send
                page.keyboard.press("Enter")
                human_delay(2, 3)
                print(f"[SUCCESS] Message sent to {name}")

                # 3. Take a screenshot of the sent message
                os.makedirs("screenshots", exist_ok=True)
                screenshot_path = f"screenshots/{phone.replace('+', '')}_{today_str}.png"
                page.screenshot(path=screenshot_path)

                # 4. Smart data extraction: Extract the last 3 messages from the active chat
                # Message bubbles can be queried using standard selector classes or selectable-text spans
                message_elements = page.locator("span.selectable-text").all()
                if message_elements:
                    # Get the last 3 text elements
                    last_three = message_elements[-3:] if len(message_elements) >= 3 else message_elements
                    extracted_messages = [el.inner_text() for el in last_three]

                status = "Success"

            except Exception as e:
                error_msg = str(e)
                print(f"[ERROR] Failed to process {name} ({phone}): {error_msg}")
                # Take error screenshot
                os.makedirs("screenshots", exist_ok=True)
                screenshot_path = f"screenshots/error_{phone.replace('+', '')}_{today_str}.png"
                page.screenshot(path=screenshot_path)

            # Record metrics for report
            report_data.append({
                "Name": name,
                "Phone": phone,
                "MessageSent": message,
                "Status": status,
                "Error": error_msg,
                "Screenshot": screenshot_path,
                "ExtractedMessages": json.dumps(extracted_messages),
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # Human-like delay between different contacts to prevent spam detection
            human_delay(3, 6)

        # 5. Save reports as JSON and Excel
        json_filename = f"whatsapp_report_{today_str}.json"
        excel_filename = f"whatsapp_report_{today_str}.xlsx"

        # Save JSON Report
        with open(json_filename, "w", encoding="utf-8") as jf:
            json.dump(report_data, jf, indent=4, ensure_ascii=False)
        print(f"\n[INFO] Saved full JSON report to {json_filename}")

        # Save Excel Summary Report
        df_report = pd.DataFrame(report_data)
        df_report.to_excel(excel_filename, index=False)
        print(f"[INFO] Saved summary Excel report to {excel_filename}")

        browser.close()
        print("[INFO] Automation run completed successfully.")

if __name__ == "__main__":
    run_whatsapp_bot()