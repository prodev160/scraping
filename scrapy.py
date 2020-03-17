import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
        
        home_collection = self.browser.find_element_by_id('home-collection')
        collections = home_collection.find_elements_by_xpath('./div')
        i = 2
        cnt_collection = len(collections)

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
            slick_prev = collection.find_element_by_class_name('slick-prev')

            while True:
                try:
                    slick_next.click()
                except:
                    break
            while True:
                try:
                    slick_prev.click()
                except:
                    break

            images = slick_track.find_elements_by_tag_name('img')

            for image in images:
                movie = {}
                movie['Name'] = image.get_attribute('alt')
                movie['Image'] = image.get_attribute('src')
                section['Items'].append(movie)
            sections.append(section)
            i = i + 1

        # self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        self.browser.execute_script("window.scrollTo(0,0)")
        with open('movie.json', 'w') as json_file:
            json.dump(sections, json_file)        
        return sections
    def get_movie_urls(self, sections, start_section, end_section):
        i = start_section
        while i < end_section:
            if i == 2: # pass `Continue Watching`
                i = i + 1
                continue
            print(sections[i]['Name'])
            movie_cnt = len(sections[i]['Items'])
            print(movie_cnt)
            j = 0
            slick_next_cnt = 0
            while j < movie_cnt:
                try:
                    home_collection = self.browser.find_element_by_id('home-collection')
                    collections = home_collection.find_elements_by_xpath('./div')
                    collection = collections[i + 2]
                    slick_track = collection.find_element_by_class_name('slick-track')
                    slick_next = collection.find_element_by_class_name('slick-next')
                    slick_prev = collection.find_element_by_class_name('slick-prev')
                    links = collection.find_elements_by_tag_name('a')

                    start = end = org_start = org_end = 0
                    while True:
                        while start == org_start and end == org_end:
                            slick_divs = slick_track.find_elements_by_xpath("./div[@aria-hidden='false']")
                            showed_movie_cnt = len(slick_divs)
                            start = int(slick_divs[0].get_attribute('data-index'))
                            end = int(slick_divs[showed_movie_cnt - 1].get_attribute('data-index'))
                        print(start, end, j)
                        if j >= start and j <= end:
                            links[j].click()
                            sections[i]['Items'][j]['URL'] = self.browser.current_url
                            print(j, self.browser.current_url)
                            self.browser.execute_script("window.history.go(-1)")
                            break
                        org_start = start
                        org_end = end
                        try:
                            if j > end:
                                slick_next.click()
                            elif j < start:
                                slick_prev.click()
                        except:
                            break
                except:
                    print('****************')
                    self.browser.get('https://www.disneyplus.com/')
                j = j + 1
            with open('movie' + str(i) + '.json', 'w') as json_file:
                json.dump(sections[i], json_file)
            i = i + 1
        with open('movie.json', 'w') as json_file:
            json.dump(sections, json_file)
        self.browser.quit()
if __name__ == "__main__":
    ExtractMovies = ExtractMovies()
    sections = ExtractMovies.get_movies()
    print(len(sections))
    ExtractMovies.get_movie_urls(sections, 9, len(sections))
    print("Task completed")