from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

class ConversationsPage(PageFactory):
    def __init__(self, driver:webdriver):
        self.driver = driver
        
    locators = {
        'input':('CSS','input[type="text"]'),
        'textarea':('CSS','textarea'),
        'new_conversation':('CSS','a[href="/web/conversations/new"]'),
        'group_conv_btn':('CSS','mw-new-conversation-start-group-button'),
        'add_contact':('CSS','mw-contact-selector-button'),
        'next_btn':('CSS','button.next-button'),
        'send_sms_btn':('CSS','mw-message-send-button')
    }
    def click_button(self, locator:str):
        wait = WebDriverWait(self.driver, timeout=30)
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
        element.click()

    def click_new_conversation(self):
        print("click new conversation")
        self.click_button(self.locators['new_conversation'][1])

    def click_group_conversation(self):
        print("click group conversation")
        self.click_button(self.locators['group_conv_btn'][1])

    def select_phone_number(self,phone_number:str):
        print("selecting phone number")
        wait = WebDriverWait(self.driver, timeout=30)
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.locators['input'][1])))
        element.send_keys(phone_number)
        print("searched for phone number")
        self.click_button(self.locators['add_contact'][1])

    def click_next_button(self):
        print("click next button")
        self.click_button(self.locators['next_btn'][1])
    
    def set_text_message(self, message:str):
        print("setting text message")
        wait = WebDriverWait(self.driver, timeout=30)
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.locators['textarea'][1])))
        element.send_keys(message)

    def send_text_message(self):
        print("sending sms")
        wait = WebDriverWait(self.driver, timeout=30)
        elements_lst = self.driver.find_elements(By.CSS_SELECTOR, self.locators['send_sms_btn'][1])
        for item in enumerate(elements_lst):
            print("entered for loop in send text message")
            if item[1].is_displayed() and item[1].is_enabled():
                element = wait.until(EC.visibility_of(item[1]))
                element.click()
                print("clicked")
        print("sms sent")
        
        



