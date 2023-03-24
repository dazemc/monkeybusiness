# AI is coming for your job
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Options
options = Options()
# Go fast
options.page_load_strategy = 'eager'
# Disable notifications
options.add_argument("--disable-notifications")
# Enable location
# options.add_experimental_option("prefs", {"profile.default_content_setting_values.geolocation": 1})


service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://monkeytype.com/")
# Explicit wait (Conditional wait)
wait = WebDriverWait(driver, 70)

# Accept all cookies to become clickable, with explicit wait
wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "button, active, acceptAll"))).click()


# Wait for words
wait.until(EC.visibility_of_element_located((By.ID, "words")))


# Get words
def get_active_word():
    word = driver.find_element(By.CSS_SELECTOR, "div.word.active")
    letters = word.find_elements(By.TAG_NAME, "letter")
    return [letter.get_attribute("textContent") for letter in letters]


def typing():
    typing_input.send_keys(get_active_word())
    typing_input.send_keys(" ")


def get_timer():
    timer_div = driver.find_element(By.ID, "miniTimerAndLiveWpm")
    return timer_div.find_element(By.CLASS_NAME, "time").get_attribute("textContent")


# Typing input
typing_input = driver.find_element(By.ID, "wordsInput")


while True:
    # Final count is for the last 1 second since there is no tenths of a second and zero never shows
    final_count = 0
    if get_timer() != "1":
        final_count += 1
        if final_count < 6:
            typing()
    else:
        break

# Print WPM, with explicit wait
wpm = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "bottom"))).text

input(f"wpm: {wpm}\nPress enter to quit: ")
driver.close()
