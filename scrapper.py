import bs4
import requests
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
import csv

class Scrapper:
    def __init__(self,
                name,
                browser=webdriver.Chrome(),
                folder_name='data\\true',
                search_URL=None,
                div_class="eA0Zlc WghbWd FnEtTd mkpRId m3LIae RLdvSe qyKxnc ivg-i PZPZlf GMCzAd",
                div_xpath="""//*[@id="rso"]/div/div/div[1]/div/div/div[%s]""",
                image_xpath="""//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]"""):
        
        self.name = name
        self.browser = browser
        self.folder_name = folder_name
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name)
        self.topic = name.strip().replace(' ', '+')
        if search_URL:
            self.search_URL = search_URL
        else: self.search_URL = f"https://www.google.com/search?q={self.topic}&source=lnms&tbm=isch"
        self.len_containers=0
        self.urls_list=[]
        self.image_file_name=f'{self.name.strip().replace(" ", "_")}'
        self.div_class=div_class
        self.div_xpath=div_xpath
        self.image_xpath=image_xpath
        

    def search_image(self):
        self.browser.get(self.search_URL)

    def scroll_down(self):
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        while True:
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def save_page(self):
        if(self.len_containers==0):
            i=0
            while i<5 or self.len_containers==0:
                try:
                    page_html = self.browser.page_source
                    pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
                    containers = pageSoup.findAll('div', {'class':self.div_class})
                    self.len_containers = len(containers)  
                except:
                    print("Error with saving page")
                    i+=1
                    continue
                i+=1
        if self.len_containers==0:
            print("There no any divs with this class")
        return self.len_containers

    def scroll_up(self):
        self.browser.execute_script("window.scrollTo(0, 0);")

    def find_image_urls(self, save_file_name='image_urls', limit=1000, save=True):
        for i in range(self.len_containers):
            if len(self.urls_list)==limit: break
            xPath = self.div_xpath%(i)
            imageXPATH=self.image_xpath
            time.sleep(0.1)
            
            try:
                self.browser.find_element(By.XPATH, xPath).click()
                time.sleep(3)
                try:
                    imagelement = self.browser.find_element(By.XPATH, imageXPATH)
                    imageurl=imagelement.get_attribute("src")
                    if imageurl not in self.urls_list:
                        self.urls_list.append(imageurl)
                        print(f'{i+1}/{self.len_containers}')
                    else:
                        print("Already in list")
                        continue
                except:
                    print("Error with image")
                    continue
            except:
                print("Error with div")
                continue
        if save: self.save_urls(savename=save_file_name)
        return self.urls_list, len(self.urls_list)
    
    def save_urls(self, savename='image_urls', folder_to_save='.'):
        self.urls_list = list(set(self.urls_list))
        if os.path.exists(f'{folder_to_save}\\{savename}.csv'):
            os.remove(f'{folder_to_save}\\{savename}.csv')
        csv_file = f'{folder_to_save}\\{savename}.csv'
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            for url in self.urls_list:
                writer.writerow([url])
        print(f"Saved {len(self.urls_list)} urls to {folder_to_save}\\{savename}.csv")

    def import_urls(self, filename='image_urls', folder_to_import='.'):
        try:
            with open(f'{folder_to_import}\\{filename}.csv', 'r') as file:
                reader = csv.reader(file)
                self.urls_list = [row[0].strip("'[]") for row in reader]
                self.urls_list = list(set(self.urls_list))
            print(f"Imported {len(self.urls_list)} urls from {folder_to_import}\\{filename}.csv")
        except:
            print(f"Error with importing {folder_to_import}\\{filename}.csv")
       
    def download_image(self, url, num=1):
        reponse = requests.get(url, verify=False)
        if reponse.status_code==200:
            with open(os.path.join(self.folder_name, f"{self.image_file_name}"+str(num)+".jpg"), 'wb') as file:
                file.write(reponse.content)
        
    def download_cycle(self):
        counter=0
        for i in range(len(self.urls_list)):
            try:
                self.browser.get(self.urls_list[i])
                self.download_image(self.urls_list[i], i)
                time.sleep(0.25)
                print(f"Downloaded {i+1}/{len(self.urls_list)} images")
                counter+=1
            except:
                print(f"Error with downloading {self.urls_list[i]}")
        return counter

    def full_cycle(self, save_file_name='image_urls', limit=1000, save=True):
        self.search_image()
        self.scroll_down()
        self.save_page()
        self.scroll_up()
        print(f'Founded {self.find_image_urls(save_file_name=save_file_name, limit=limit, save=save)[1]} images for "{self.name}"')
        print(f'Downloaded {self.download_cycle()} images for "{self.name}"')
        self.browser.quit()
        
    
    
scraper=Scrapper('hello', folder_name='data\\false')
#scraper.import_urls('image_urls')
scraper.full_cycle('false_image_urls', 25)

    