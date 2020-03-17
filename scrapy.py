import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import json
import time

class ExtractMovies():

    def __init__(self):
        # set chrome webdriver
        self.browser = webdriver.Chrome('./chromedriver')
        self.login_email = 'dtest-1984@gmail.com'
        self.login_pwd = 'Test!234'

    def wait_for(self, id, timeout=30):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((By.ID, id)))
        except TimeoutException:
            print("Loading took too much time!")

    def login(self):
        self.browser.implicitly_wait(30) # seconds
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
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        self.browser.execute_script("window.scrollTo(0, 0)")

    def get_movie_urls(self):
        self.wait_for('home-collection')
        home_collection = self.browser.find_element_by_id('home-collection')
        collections = home_collection.find_elements_by_xpath('./div')
        cnt_collection = len(collections)
        sections = []
        i = 2
        while i < cnt_collection:
            self.wait_for('home-collection')
            home_collection = self.browser.find_element_by_id('home-collection')
            collections = home_collection.find_elements_by_xpath('./div')

            section = {}
            collection = collections[i]
            slick_next = collection.find_element_by_class_name('slick-next')
            slick_prev = collection.find_element_by_class_name('slick-prev')
            slick_next.click()
            slick_prev.click()
            time.sleep(0.5)

            collection_name = collection.find_element_by_tag_name('h4').text
            print("new section", collection_name)
            section['Name'] = collection_name
            section['Items'] = []
            
            slick_track = collection.find_element_by_class_name('slick-track')
            movie_cnt = len(slick_track.find_elements_by_xpath('./div'))
            j = 0
            print("movie_cnt", movie_cnt)
            while j < movie_cnt:
                self.wait_for('home-collection')
                home_collection = self.browser.find_element_by_id('home-collection')
                collections = home_collection.find_elements_by_xpath('./div')
                collection = collections[i]
                slick_track = collection.find_element_by_class_name('slick-track')
                slick_next = collection.find_element_by_class_name('slick-next')
                slick_prev = collection.find_element_by_class_name('slick-prev')
                links = collection.find_elements_by_tag_name('a')

                start = end = org_start = org_end = 0
                while j < start or j > end:
                    while start == org_start and end == org_end:
                        slick_divs = slick_track.find_elements_by_xpath("./div[@aria-hidden='false']")
                        showed_movie_cnt = len(slick_divs)
                        start = int(slick_divs[0].get_attribute('data-index'))
                        end = int(slick_divs[showed_movie_cnt - 1].get_attribute('data-index'))
                    org_start = start
                    org_end = end
                    try:
                        if j > end:
                            slick_next.click()
                        elif j < start:
                            slick_prev.click()
                    except:
                        print("All rendered")
                print("./div[@data-index=" + str(j) + "]")
                cur_movie = slick_track.find_element_by_xpath("./div[@data-index=" + str(j) + "]")
                print("find movie")
                while True:
                    try:
                        image = cur_movie.find_element_by_tag_name('img')
                        print("find image")
                        break
                    except:
                        print("don't find image, doing again")
                        time.sleep(0.01)
                movie = {}
                movie['Name'] = image.get_attribute('alt')
                movie['Image'] = image.get_attribute('src')
                links[j].click()
                movie['URL'] = self.browser.current_url
                section['Items'].append(movie)
                self.browser.back()
                j = j + 1
            with open(str(i) + '.json', 'w') as json_file:
                json.dump(section, json_file)
            sections.append(section)
            i = i + 1
        with open('movie.json', 'w') as json_file:
            json.dump(sections, json_file)
        self.browser.quit()
if __name__ == "__main__":
    ExtractMovies = ExtractMovies()
    ExtractMovies.login()
    ExtractMovies.get_movie_urls()
    # sections = []
    # i = 2
    # while i < 24:
    #     with open(str(i) + ".json", 'r') as jsonfile:
    #         data = jsonfile.read()
    #     section = json.loads(data)
    #     sections.append(section)
    #     i = i + 1
    # with open("movie.json", "w") as jsonfile:
    #     json.dump(sections, jsonfile)
    print("Task completed")