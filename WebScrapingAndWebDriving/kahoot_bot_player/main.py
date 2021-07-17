# using these libraries, please download before using this script
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# change this to the path of your chrome driver
CHROME_DRIVER_PATH = "/Users/LucasZ/Documents/chromedriver"
# change this number to the PIN of the kahoot
KAHOOT_PIN = "9261160"
# change this to the name of your bot
BOT_NAME = "Bot1000"

# initialize
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get("https://kahoot.it/")

# enter the game pin
game_pin_input = driver.find_element_by_css_selector('input[data-functional-selector="game-pin-input"]')
game_pin_input.send_keys(KAHOOT_PIN)
game_pin_input.send_keys(Keys.ENTER)

# wait for next screen to appear
time.sleep(2)

# enter the username
name_input = driver.find_element_by_css_selector('input[data-functional-selector="username-input"]')
name_input.send_keys(BOT_NAME)
name_input.send_keys(Keys.ENTER)

end_game = False
# the game loop
while True:
    # wait for the gameblock screen(the screen where you choose your answer)
    while driver.current_url != "https://kahoot.it/v2/gameblock":
        # while waiting, if the screen becomes the ending screen break the loop
        if driver.current_url == "https://kahoot.it/v2/ranking":
            end_game = True
            break
        # else print the current screen and wait
        else:
            print("currently on", driver.current_url)
            time.sleep(1)

    # if game has ended during the waiting loop, break the loop
    if end_game:
        break

    # else wait and select the red button on the screen
    time.sleep(1)
    red_button = driver.find_element_by_css_selector('button[data-functional-selector="answer-0"]')
    red_button.click()

    # wait for the "question answered" screen to show first
    # this prevents double triggering of the red-button click code
    time.sleep(1.5)

# game has ended
driver.quit()
print("Script finished, game ended!")

