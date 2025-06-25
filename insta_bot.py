from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
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
    bio = driver.find_element(By.XPATH, "//div[contains(@class, '_aacl _aacp _aacu _aacx _aad6 _aade')]").text
    stats = driver.find_elements(By.XPATH, "//ul/li")
    followers = stats[1].text
    following = stats[2].text
    return bio, followers, following

def save_to_file(bio, followers, following):
    with open("account_info.txt", "w", encoding="utf-8") as f:
        f.write(f"Bio: {bio}\n")
        f.write(f"Followers: {followers}\n")
        f.write(f"Following: {following}\n")

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # For Codespaces
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    
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
