from DrissionPage import ChromiumOptions, ChromiumPage
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

soup = use_soup(driver, 'xpath://div[@class="box-category__list-news"]')
tagsElem = soup.select('h4.item-tag > a')
print('tagsElems', tagsElem)


i want to apply WebDriverWait for tagsElem exist, how to do that?

class WebDriverWait:
    def __init__(
        self,
        driver,
        timeout: float,
        poll_frequency: float = POLL_FREQUENCY,
        ignored_exceptions: typing.Optional[WaitExcTypes] = None,
    ):
        """Constructor, takes a WebDriver instance and timeout in seconds.

        :Args:
         - driver - Instance of WebDriver (Ie, Firefox, Chrome or Remote) or a WebElement
---

