import ipdb
import os
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import urllib2
import csv
import codecs

username="tmslav"
password="laajviii"
country='Canada'
outputdir="/home/tom/documents/elance/google_adwords/output"
url_file_map={}
class googleAdwords:
    def __init__(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2) # custom location
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', outputdir)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
        self.checked=False
        self.br=webdriver.Firefox(profile)
        self.br.get("http://www.google.com/adwords/")
        self.br.find_element_by_link_text("Sign in").click()
        self.br.find_element_by_xpath("//input[@id='Email']").send_keys(username)
        self.br.find_element_by_xpath("//input[@id='Passwd']").send_keys(password)
        self.hard_click(self.br.find_element_by_xpath,"//input[@id='signIn']")
        self.loading()

    def prepare_for_upload(self,file_name,country):
        self.filename=file_name
        self.hard_click(self.br.find_element_by_xpath,"//div[@class='aw-cues-item-c']['Tools and Analysis '=text()]")
        self.br.find_element_by_link_text("Keyword Planner").click()
        self.loading()
        if self.br.find_elements_by_xpath("//span[@id='gwt-debug-startover-startover-content']")!=[]:
            self.br.find_element_by_xpath("//span[@id='gwt-debug-startover-startover-content']").click()
        self.hard_click(self.br.find_element_by_xpath,"//div[@id='gwt-debug-splash-panel-stats-selection-input']")
        self.loading()
        self.br.find_elements_by_xpath("//input[@name='uploadFile'][@id='gwt-debug-upload-file']")[2].send_keys(os.path.abspath(file_name))
        self.br.find_elements_by_xpath("//div[@id='gwt-debug-location-pill-display-text-div']")[0].click()
        time.sleep(1)
        self.br.find_element_by_link_text("Remove all").click()
        time.sleep(1)
        self.br.find_element_by_xpath("//input[@id='gwt-debug-geo-search-box']").clear()
        self.br.find_element_by_xpath("//input[@id='gwt-debug-geo-search-box']").send_keys(country)
        time.sleep(1)
        self.br.find_element_by_link_text("Add").click()
        time.sleep(1)
        self.br.find_elements_by_xpath("//span['Get search volume'=text()]")[3].click()
        self.br.find_elements_by_xpath("//span['Get search volume'=text()]")[3].click()
        self.loading()
        time.sleep(2)
        self.br.find_element_by_xpath("//div[text()='Keyword ideas']").click()
        self.br.find_element_by_xpath("//div[text()='Keyword ideas']").click()
        self.loading()
        self.download()

    def hard_click(self,func,xpath,arr_numb=None):
        nl=False
        while not nl:
            try:
                if arr_numb!=None:
                    func(xpath)[arr_numb].click()
                else:
                    func(xpath).click()
                nl=True
            except:
                time.sleep(1)


    def download(self):
        time.sleep(5)
        self.hard_click( self.br.find_elements_by_xpath,"//*[text()='Download']",1)
        if not self.checked:
            self.hard_click(self.br.find_elements_by_xpath,"//span[@class='gwt-CheckBox'][contains('Segment',text())]/input[@type='checkbox']",2)
            self.checked=True

        self.hard_click(self.br.find_element_by_id,'gwt-debug-download-button-content')
        time.sleep(1)
        ready=False
        csv_url=""
        while not ready and csv_url=='':
            try:
                csv_url=self.br.find_element_by_link_text("Your download is now available. Click to retrieve it.").get_attribute("href")
                print csv_url
                self.br.find_element_by_link_text("Your download is now available. Click to retrieve it.").click()
                url_file_map[csv_url.split("/")[-1]]=self.filename
                ready=True
            except:
                time.sleep(1)
        self.loading()
        self.br.find_element_by_xpath("//span[@id='gwt-debug-close-button-success-content']").click()
        time.sleep(10)

    def next_csv(self,filename):
        self.filename=filename
        self.hard_click(self.br.find_element_by_xpath,"//span[@id='gwt-debug-modify-search-button-content']")
        time.sleep(1)
        self.br.find_elements_by_xpath("//input[@name='uploadFile'][@id='gwt-debug-upload-file']")[4].send_keys(os.path.abspath(filename))
        time.sleep(2)
        self.hard_click(self.br.find_elements_by_xpath,"//span[@id='gwt-debug-upload-ideas-button-content']",6)
        self.download()


    def loading(self):
        try:
            while "display: none" not in self.br.find_element_by_xpath("//div[@id='initialLoading']").get_attribute("style") and  self.get_state()!='complete':
                time.sleep(1)
            time.sleep(1)
        except:
            self.loading()
    def get_state(self):
        return self.br.execute_script("return document.readyState")
    def quit(self):
        self.br.quit()


if __name__=='__main__':
    files=[i for i in os.listdir(".") if ".csv" in i]
    sc=googleAdwords()
    sc.prepare_for_upload(files[0],country)
    for i in files[1:]:
        sc.next_csv(i)
    os.chdir("output")

    for i in url_file_map.keys():
        os.rename(i,url_file_map[i].replace(".csv","")+"output.csv")
    masterkw=[]
    for i in os.listdir("."):
        f=codecs.open(i,"rb","utf-16")
        csvread=csv.reader(f,delimiter='\t')
        csvread.next()
        for row in csvread:
            masterkw.append(row)
    sortedmaster=sorted(masterkw,key=lambda x:x[3])
    remove_0=[i for i in sortedmaster if i[3]!='0' and i[3]!='']
    csvwriter=csv.writer(open("masterkw.xls","wb"))
    for row in remove_0:
        csvwriter.writerow(row)
    ipdb.set_trace()
    sc.quit()












