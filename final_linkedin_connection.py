import time, random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from duckduckgo_search import DDGS

# --- CREDENTIALS ---
LINKEDIN_EMAIL = "5pszqchzyc@privaterelay.appleid.com"
LINKEDIN_PASSWORD = "Exiled@NK123"


def human_delay(min_sec=2, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))


def ddg_lookup(query):
    ddgs = DDGS()
    for r in ddgs.text(f"{query} site:linkedin.com/in", max_results=1):
        href = r.get("href", "")
        if "/in/" in href:
            return href
    return None


def login_linkedin(driver):
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "username"))
    ).send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD + Keys.RETURN)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@aria-label,'Search')]"))
    )
    print("[+] Logged in.")
    human_delay(1, 7)


def click_first_search_result(driver, query):
    wait = WebDriverWait(driver, 20)
    search_input = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "input.search-global-typeahead__input")
    ))
    search_input.clear()
    search_input.send_keys(query, Keys.RETURN)
    human_delay(2, 4)

    try:
        people_tab = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(.,'People')]")
        ))
        people_tab.click()
        human_delay(1, 2)
    except:
        print("[!] People tab not found.")

    profile_xpath = "(//a[contains(@href, '/in/') and @data-test-app-aware-link])[1]"
    first_profile = wait.until(EC.visibility_of_element_located((By.XPATH, profile_xpath)))

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_profile)
    human_delay(1, 2)
    try:
        first_profile.click()
    except:
        driver.execute_script("arguments[0].click();", first_profile)

    human_delay(3, 6)
    return True


def connect_via_button(driver):
    wait = WebDriverWait(driver, 10)
    try:
        connect_btn = wait.until(EC.presence_of_element_located((
            By.XPATH, "//button[contains(@aria-label, 'Invite') and .//span[text()='Connect']]"
        )))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", connect_btn)
        human_delay(1, 2)
        driver.execute_script("arguments[0].click();", connect_btn)
        human_delay(1, 2)

        # Add note
        add_note_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[.//span[text()='Add a note']]"
        )))
        add_note_btn.click()
        human_delay(1, 2)

        # Get the first text file in the directory
        directory = "/Users/samreedhbhuyan/Desktop/MIT_HACKATHON/juris_AI/personalised_message/"
        txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]

        if txt_files:
            file_path = os.path.join(directory, txt_files[0])  # Get the first text file
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()[1:]  # Skip the first line
                note_text = ''.join(lines).strip()
        else:
            print("[!] No text files found in the directory.")
            return False

        message_box = wait.until(EC.visibility_of_element_located((
            By.XPATH, "//textarea[@name='message']"
        )))
        message_box.send_keys(note_text)
        human_delay(1, 2)

        send_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[.//span[text()='Send']]"
        )))
        send_btn.click()
        print("[+] Connection request sent with personalized note.")
        return True
    except Exception as e:
        print(f"[!] Connect button with note failed: {e}")
        return False


def connect_via_more_menu(driver):
    wait = WebDriverWait(driver, 10)
    try:
        more = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(@aria-label,'More actions')]"
        )))
        more.click()
        human_delay(1, 2)

        connect_item = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//div[@role='menuitem']//span[text()='Connect']"
        )))
        connect_item.click()
        human_delay(1, 2)

        send_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[.//span[text()='Send']]"
        )))
        send_btn.click()
        print("[+] Connection request sent via More menu.")
        return True
    except Exception as e:
        print(f"[!] More menu Connect failed: {e}")
        return False


def follow_as_final_fallback(driver):
    try:
        follow = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Follow']]"))
        )
        follow.click()
        print("[+] Followed as fallback.")
        return True
    except:
        print("[!] No Connect or Follow option available.")
        return False


def send_request_flow(query):
    chrome_opts = Options()
    chrome_opts.add_argument("--start-maximized")
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_opts)

    try:
        login_linkedin(driver)

        if not click_first_search_result(driver, query):
            url = ddg_lookup(query)
            if not url:
                print("[!] Profile not found.")
                return
            print(f"[+] Using DDG fallback URL: {url}")
            driver.get(url)
            human_delay(3, 5)

        if not connect_via_button(driver):
            if not connect_via_more_menu(driver):
                follow_as_final_fallback(driver)

        time.sleep(5)  # Keep short for testing
    finally:
        driver.quit()


if __name__ == "__main__":
    name_company = input("Enter name and company: ").strip()
    send_request_flow(name_company)
