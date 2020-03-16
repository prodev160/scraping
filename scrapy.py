import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json

class ExtractMovies():

    def __init__(self):
        # set chrome webdriver
        self.browser = webdriver.Chrome()
        self.login_email = 'dtest-1984@gmail.com'
        self.login_pwd = 'Test!234'

    def wait_for(self, id, timeout=30):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((By.ID, id)))
        except TimeoutException:
            print("Loading took too much time!")

    def get_movies(self):
        self.login_url = 'https://www.disneyplus.com/login'
        self.browser.maximize_window()
        self.browser.get(self.login_url)

        self.wait_for('dssLogin')
        login_form = self.browser.find_element_by_id('dssLogin')
        login_form.find_element_by_id('email').send_keys(self.login_email)
        login_form.submit()
        self.wait_for('password')
        login_form = self.browser.find_element_by_id('dssLogin')
        login_form.find_element_by_id('password').send_keys(self.login_pwd)
        login_form.submit()
        self.wait_for('home-collection')
        # self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        # self.browser.execute_script("window.scrollTo(0,0)")
        
        home_collection = self.browser.find_element_by_id('home-collection')
        collections = home_collection.find_elements_by_xpath("./div")
        i = 2
        # cnt_collection = len(collections)
        cnt_collection = 2

        self.browser.implicitly_wait(10) # seconds
        sections = []

        while i < cnt_collection:
            section = {}
            collection = collections[i]
            collection_name = collection.find_element_by_tag_name('h4').text
            section['Name'] = collection_name
            section['Items'] = []

            slick_track = collection.find_element_by_class_name('slick-track')
            slick_next = collection.find_element_by_class_name('slick-next')

            while True:
                if slick_next:
                    try:
                        slick_next.click()
                    except:
                        break

            images = slick_track.find_elements_by_tag_name('img')
            print(len(images))
            for image in images:
                movie = {}
                movie['Name'] = image.get_attribute('alt')
                movie['Image'] = image.get_attribute('src')
                section['Items'].append(movie)
            sections.append(section)
            i = i + 1
        with open('movie.json', 'w') as json_file:
            json.dump(sections, json_file)
        print(sections)
if __name__ == "__main__":

    ExtractMovies = ExtractMovies()
    limit_row = ExtractMovies.get_movies()

    print("Task completed")