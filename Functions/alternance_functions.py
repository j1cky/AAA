from selenium import webdriver


from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

def easy_apply(url, firstname, familyname, email, phone, cv_path):

    try:
        # Open the job application link
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        # Click on the "Easy Apply" button
        wait = WebDriverWait(driver, 10)
        easy_apply_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='postuler-button']"))
        )
        easy_apply_button.click()

        # Wait for the form to appear
        time.sleep(2)  # Allow time for the pop-up to render
        
        # Fill in the form fields
        driver.find_element(By.ID, "lastName").send_keys(familyname)
        print("Family Name filled")
        driver.find_element(By.ID, "firstName").send_keys(firstname)
        print("First Name filled")
        driver.find_element(By.ID, "email").send_keys(email)
        print("Email filled")
        driver.find_element(By.ID, "phone").send_keys(phone)
        print("Phone filled")


        # Upload CV file
        cv_upload = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
        cv_upload.send_keys(cv_path)

        # Submit the form
        
        submit_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='candidature-not-sent']"))
        )
        submit_button.click()
        time.sleep(4) 

        print("Application submitted successfully!")

    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error during the application process: {e}")



def check_easy_apply(url):
    try:
        # Open the job application link
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        # Wait for the page to load completely
        wait = WebDriverWait(driver, 10)

        # Check if the application button "J'envoie ma candidature" is present
        try:
            apply_button = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[contains(text(), \"J'envoie ma candidature\")]")
                )
            )
            if apply_button:
                print("Easy Apply button found.")
                
                return True
        except TimeoutException:
            print("No Easy Apply button found. Checking if already applied...")
        return None
    
        # # Check if the message "Bravo, vous avez déjà postulé" is present
        # try:
        #     already_applied_message = wait.until(
        #         EC.presence_of_element_located(
        #             (By.XPATH, "//span[contains(text(), 'Bravo, vous avez déjà postulé')]")
        #         )
        #     )
        #     if already_applied_message:
        #         print("Already applied message found.")
        #         return False
        # except TimeoutException:
        #     print("No already applied message found.")

        # # If neither the button nor the message is found, return None (unknown state)
        # return None    

    except Exception as e:
        print(f"Error during checking apply possibility: {e}")
        return None
    



def get_job_links(url):

    try:
        # Open the job application link
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        # Wait for the page to load completely
        wait = WebDriverWait(driver, 10)
        
        # Wait until the 'jobList' div is present
        job_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[queryparamshandling='merge']"))) # Works for Apec

        # Get all job offer elements
        job_offer_elements = driver.find_elements(By.CSS_SELECTOR, "a[queryparamshandling='merge']")

        # Works for La bonne alternance
        # job_list = wait.until(EC.presence_of_element_located((By.ID, "jobList")))  
        # job_offer_elements = job_list.find_elements(By.CLASS_NAME, "chakra-link")

        # Extract the href attributes
        job_links = [ element.get_attribute('href') for element in job_offer_elements]       
        
        return job_links
    
    except Exception as e:
        print(f"Error during filtering links: {e}")
        return None
