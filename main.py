# AI is coming for your job
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Var
TARGET_WPM = 420  # Results will not be exact ~+6
TEST_TIME = 30
# Get WPM, get percentage of test time, multiply WPM by test time percentage and multiply that by test time to get total words needed for target WPM
TYPING_SPEED = (TARGET_WPM / 60) * abs(60 - TEST_TIME) - 6  # Seems to be 6 words off on average, this is because I am using the onscreen timer.... EC or start timer on typing()
TYPED_WORD_COUNT = 0.0
print(TYPING_SPEED)

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
    global TYPED_WORD_COUNT
    typing_input.send_keys(get_active_word())
    typing_input.send_keys(" ")
    TYPED_WORD_COUNT += 1


# FIXME: Make timer rather than using timer
def get_timer():
    timer_div = driver.find_element(By.ID, "miniTimerAndLiveWpm")
    return timer_div.find_element(By.CLASS_NAME, "time").get_attribute("textContent")


# Typing input
typing_input = driver.find_element(By.ID, "wordsInput")


while True:
    if TYPED_WORD_COUNT != TYPING_SPEED:
        typing()
    else:
        break

# Print WPM, with explicit wait
wpm = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "bottom"))).text

input(f"wpm: {wpm}\nPress enter to quit: ")
driver.quit()
