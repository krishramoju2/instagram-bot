from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

USERNAME = "your_dummy_username"
PASSWORD = "your_dummy_password"
TARGET_USER = "cbitosc"

def login(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
    time.sleep(5)

def search_and_open_profile(driver, user):
    search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
    search_box.send_keys(user)
    time.sleep(3)
    search_box.send_keys(Keys.DOWN)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

def follow_if_not_following(driver):
    try:
        button = driver.find_element(By.XPATH, "//button[text()='Follow']")
        button.click()
        print("Followed the account.")
    except:
        print("Already following.")

def extract_info(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul/li"))
        )
        stats = driver.find_elements(By.XPATH, "//ul/li")

        try:
            bio = driver.find_element(By.XPATH, "//section//div[contains(@class, '_aacl')]").text
        except:
            bio = "Bio not found"

        if len(stats) >= 3:
            followers = stats[1].text
            following = stats[2].text
        else:
            followers = "Not found"
            following = "Not found"

        return bio, followers, following
    except Exception as e:
        print("Error extracting profile info:", e)
        return "N/A", "N/A", "N/A"

def save_to_file(bio, followers, following):
    with open("account_info.txt", "w", encoding="utf-8") as f:
        f.write(f"Bio: {bio}\n")
        f.write(f"Followers: {followers}\n")
        f.write(f"Following: {following}\n")

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    try:
        login(driver, USERNAME, PASSWORD)
        search_and_open_profile(driver, TARGET_USER)
        follow_if_not_following(driver)
        bio, followers, following = extract_info(driver)
        save_to_file(bio, followers, following)
        print("Data saved to account_info.txt")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
