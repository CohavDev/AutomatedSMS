from selenium import webdriver
from src.pages.conversations import ConversationsPage
from selenium.webdriver.chrome.options import Options
from termcolor import colored
import time, csv, sys, os
import schedule

URL = "https://messages.google.com/web/conversations"
FILE_PATH = "./sims.csv"
BROWSER_CHROME_PROFILE_PATH = os.path.abspath("./custom_profile_chrome")
BROWSER_EDGE_PROFILE_PATH = os.path.abspath("./custom_profile_edge")
DEFAULT_COMMAND = "(o2w,4,0100)"
DEFAULT_RETRIES = 3
MAX_RUN_COUNT = 10
CHUNK_SIZE = 50

run_count = 0

def is_chrome_installed():
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.getenv('LOCALAPPDATA') +r"\Google\Chrome\Application\chrome.exe"
    ]
    return any(os.path.isfile(path) for path in paths)

def is_edge_installed():
    paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    return any(os.path.isfile(path) for path in paths)

def get_text_command():
    if len(sys.argv) > 1:
        try:
            retries = int(sys.argv[1])
        except:
            raise SystemExit("'Retries' is not a valid number !")
        if len(sys.argv) > 2:
            command = sys.argv[2] # command to send in sms
            return command, retries
        return DEFAULT_COMMAND, retries
    else:
        return DEFAULT_COMMAND, DEFAULT_RETRIES
def get_text_command_via_input():
    argv1 = input(f"Enter number of messages to send / Press ENTER for default ({DEFAULT_RETRIES})")
    if argv1 == "":
        retries = DEFAULT_RETRIES
    else:
        try:
            retries = int(argv1)
        except:
            raise SystemExit("Your input is not a valid number")
    argv2 = input(f"Enter command to send via SMS: (default = {DEFAULT_COMMAND})")
    if argv2 == "":
        command = DEFAULT_COMMAND
    else:
        command = argv2
    return command, retries
def get_csv_rows():
    with open(FILE_PATH, mode='r',newline='') as file:
        reader = csv.reader(file)
        header = next(reader) # if there is a header
        filtered_rows = [row for row in reader if len(row) > 0]
        rows = list(reader)
        return filtered_rows
def init_browser() -> webdriver.Chrome:
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    print(colored("--- starting test case ---","blue"))
    if is_chrome_installed():
        options.add_argument(f"user-data-dir={BROWSER_CHROME_PROFILE_PATH}")
        driver = webdriver.Chrome(options=options)
    elif is_edge_installed():
        options.add_argument(f"user-data-dir={BROWSER_EDGE_PROFILE_PATH}")
        driver = webdriver.Edge(options=options)
    else:
        raise FileNotFoundError("Could not find Chrome or Edge browsers installed on your system.")
    driver.set_window_size(1920,1080)
    driver.set_page_load_timeout(120)
    driver.set_script_timeout(120)
    driver.get(URL)
    time.sleep(5)
    if driver.current_url != URL:
        input("press ENTER after you scanned the QR code on the web browser")
    return driver

def test(driver:webdriver, reader:csv.reader, command, retries):
    # --- user flow start ---
    conPage = ConversationsPage(driver)
    
    conPage.click_new_conversation()
    time.sleep(2)
    conPage.click_group_conversation()
    time.sleep(2)
    for row in reader:
        print(row[0])
        conPage.select_phone_number(row[0])

    conPage.click_next_button()
    for i in range(retries):
        conPage.set_text_message(command)
        conPage.send_text_message()

    time.sleep(5)

def finish_test(driver):
    driver.quit()
    print(colored("--- finished SMS sender procedure ---","blue"))



def split_list(lst, chunck_size):
    return [lst[i:i + chunck_size] for i in range(0, len(lst),chunck_size)]

def run_sms_sender():
    global run_count
    run_count += 1
    if run_count > MAX_RUN_COUNT:
        raise SystemExit(colored(f"Finished {MAX_RUN_COUNT} runs of SMS sender\n---DONE---","red"))
    print(colored("Running 'SMS-sender' procedure...", "blue"))
    try:
        command, retries = get_text_command_via_input()
        print(command)
        print(retries)
        reader = get_csv_rows()
        rows_by_groups = split_list(reader, CHUNK_SIZE)
        driver = init_browser()
        for group in rows_by_groups:
            retry_operation(driver,group, command, retries)
        finish_test(driver)
    except Exception as e:
        print(colored(f"\nAn error occured: {e}", "red"))

def retry_operation(driver,group, command, retries):
    for i in range(3):
        try:
            test(driver,group, command, retries)
            break
        except Exception as e:
            print(colored(f"\nAn error occured, trying again from the same point: {e}", "red"))



def test_split():
    reader = get_csv_rows()
    rows_by_groups = split_list(reader, CHUNK_SIZE)
    for group in rows_by_groups:
       print("---group---")
       for item in group:
           print(item)

# test_split()
run_sms_sender()
schedule.every(45).minutes.do(run_sms_sender)
while True:
    schedule.run_pending()
    time.sleep(3)
# print(is_chrome_installed())
# print(is_edge_installed())