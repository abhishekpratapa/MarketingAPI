from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from pyvirtualdisplay import Display

display = Display(visible=False, size=(1024, 768))
display.start()

driver = webdriver.Chrome()
driver.get("https://www.google.com/")

html_code = driver.find_element_by_tag_name("body").get_attribute("innerHTML")

print(html_code)

driver.close()
display.stop()

exit()