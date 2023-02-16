from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
driver = webdriver.Chrome(driver_path)