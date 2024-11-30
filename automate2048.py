from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
# adblock
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait




# Define the URL of the 2048 game
url = "https://2048game.com/"

# Define the keys for moving in the game
keys = [Keys.UP, Keys.RIGHT, Keys.DOWN, Keys.LEFT]

# Function to check if the game is over
def is_game_over(driver):
    try:
        # Find the game over message element
        game_over_message = driver.find_element("css selector", ".game-message.game-over")
        # Check if the game over message is displayed
        if game_over_message.is_displayed():
            return True
        else:
            return False
    except NoSuchElementException:
        return False

# Function to check if the game is won
def is_game_won(driver):
    try:
        game_won_message = driver.find_element("css selector", ".game-message.game-won")
        if game_won_message.is_displayed():
            return True
        else:
            return False
    except NoSuchElementException:
        return False

# Function to play the game
def play_game(driver):
    game_container = driver.find_element("class name", "container")
    actions = ActionChains(driver)
    actions.click(game_container)
    while not is_game_over(driver) and not is_game_won(driver):  # Check if game is over or won
        try:
            for key in keys:
                actions.send_keys(key)
                actions.perform()
                # time.sleep(0.05)  
                time.sleep(0.5)  
        except Exception as e:
            print(f"An error occurred: {e}")
            break

# Function to restart the game
def restart_game(driver):
    if is_game_won(driver):
        print("Game won!")
        return
    try:
        retry_button = driver.find_element("class name", "retry-button")
        if retry_button.is_displayed() and retry_button.is_enabled():
            retry_button.click()
            print("Clicked on retry button.")
        else:
            print("Retry button not clickable.")
    except NoSuchElementException:
        print("Retry button not found.")





def adblock():
    wait = WebDriverWait(driver, 10)
    driver.get(
        "https://chromewebstore.google.com/detail/adblock-%E2%80%94-block-ads-acros/gighmmpiobklfepjocnamgkkbiglidom?hl=en-US")
    WebDriverWait(driver, 15).until(
        EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "dd-Va g-c-wb g-eg-ua-Uc-c-za g-c-Oc-td-jb-oa g-c"))).click()
    alert = driver.switch_to_alert()
    alert.accept()


# adblock()

# Main function
def main():
    # Start the browser
    driver = webdriver.Firefox() # For Chrome, download chromedriver, then change to: driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

    # Open the game
    driver.get(url)

    try:
        while True:
            # Play the game
            play_game(driver)

            # Game over, restart
            restart_game(driver)

    except KeyboardInterrupt:
        print("Script stopped by the user")
    finally:
        # Quit the browser session
        driver.quit()

if __name__ == "__main__":
    main()
