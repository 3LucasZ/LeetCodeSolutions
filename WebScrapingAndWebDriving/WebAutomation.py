from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "/Users/LucasZ/Documents/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# driver.get("https://en.wikipedia.org/wiki/Main_Page")

# all_portals = driver.find_element_by_link_text("All portals")

# search = driver.find_element_by_name("search")
# search.send_keys("Python")
# search.send_keys(Keys.ENTER)

driver.get("https://secure-retreat-92358.herokuapp.com/")

fname_input = driver.find_element_by_xpath("/html/body/form/input[1]")
fname_input.send_keys("gibberish")
lname_input = driver.find_element_by_xpath("/html/body/form/input[2]")
lname_input.send_keys("gibberish")
email_input = driver.find_element_by_xpath("/html/body/form/input[3]")
email_input.send_keys("gibberish@gmail.com")

send_button = driver.find_element_by_xpath("/html/body/form/button")
send_button.click()


# driver.quit()
