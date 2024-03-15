from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import undetected_chromedriver as uc
import time

# create a new instance of Chrome
driver = uc.Chrome()
driver.get("https://ma.indeed.com/?from=gnav-jobsearch--indeedmobile")
driver.set_window_size(1200, 800)

try:
    job_title_field = driver.find_element(By.XPATH, "//*[@id='text-input-what']")
    search_button = driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton")
    job_title_field.send_keys('ingénieur informatique')
    search_button.click()
    time.sleep(2)
except:
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"#credential_picker_container > iframe:nth-child(1)")))
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#close"))).click()
    driver.switch_to.default_content()
    job_title_field = driver.find_element(By.XPATH, "//*[@id='text-input-what']")
    search_button = driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton")
    job_title_field.send_keys('ingénieur informatique')
    search_button.click()

#find the job titles, job locations and company name
df = pd.DataFrame({"Poste date":[],"Title":[],"Location":[],"Company":[],"Job type":[], "Job description":[]})
for i in range(32):
    driver.get("https://ma.indeed.com/jobs?q=ingénieur+informatique&l=Maroc&start="+str(i)+"0")
    driver.implicitly_wait(4)
    for job_post in driver.find_elements(By.CLASS_NAME, "job_seen_beacon"):
        soup = BeautifulSoup(job_post.get_attribute('innerHTML'),'html.parser')
        try:
            poste_date = soup.find("span", class_ = "css-qvloho eu4oa1w0").text
        except:
            poste_date = None
        try:
            job_title = soup.find("h2", class_ = 'jobTitle css-14z7akl eu4oa1w0').text.replace("\n","").strip()
            time.sleep(2)
        except:
            job_title = None
        try:
            company = soup.find('span', class_ = 'css-92r8pb eu4oa1w0').text.replace("\n","").strip()
            time.sleep(1)
        except:
            company = None
        try:
            location = soup.find('div', class_ = 'css-1p0sjhy eu4oa1w0').text.replace("\n","").strip()
            time.sleep(2)
        except:
            location = None
        try:
            job_type = soup.find('div', class_ = "css-1cvo3fd eu4oa1w0").text.replace("\n","").strip()
            time.sleep(1)
        except:
            job_type = None
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", job_post)
            job_post.click()
            time.sleep(3)
            driver.implicitly_wait(4)
        except:
            close_button = driver.find_element(By.XPATH,'/html/body/div[3]/div[1]/div[1]/button')
            close_button.click()
            driver.execute_script("arguments[0].scrollIntoView(true);", job_post)
            job_post.click()
            time.sleep(2)

        try:
            driver.implicitly_wait(4)
            job_desc = driver.find_element(By.ID, "jobDescriptionText").text
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
        except:
            job_desc = None
            time.sleep(2)
        new_row = pd.Series({"Poste date":poste_date,"Title":job_title,"Location":location,"Company":company,"Job type":job_type, "Job description":job_desc})
        df.loc[len(df)] = new_row
print("Got these many results:",df.shape)
df.to_csv("IT.csv",index=False)