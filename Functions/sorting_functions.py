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

from pathlib import Path

import os


options = Options()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# default_user_data_dir = Path.home() / ".config/google-chrome"  

# options.add_argument(f"--user-data-dir={str(default_user_data_dir)}")
# options.add_argument("--profile-directory=Default") 


def offer_applier(test_url):

    driver = check_easy_apply(test_url)


    if driver:
        formulaire = promotion_or_formulaire(driver)

        if not formulaire:
            if connected(driver) :
                postuler(driver)
                fill_and_submit(driver, cv_path, message)
            else :
                print('Lien du formulaire')
                connexion = apec_connect(driver,usr, password)
                if connexion :
                    print('Connected')
                    fill_and_submit(driver, cv_path, message)
                
        else:
            fill_and_submit(driver, cv_path, message)



    driver.quit()

def select_importer_cv(driver):
    try:
        wait = WebDriverWait(driver, 10)
        
        # SClick the "Apply with CV" radio button
        apply_with_cv_radio = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'form-check') and .//label[contains(text(), 'Je préfère joindre uniquement un CV')]]//input"))
        )
        apply_with_cv_radio.click()

        # Step 2: Wait for the "Import a CV" option to be visible (this assumes it appears after the first option is selected)
        dropdown_options = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'dropdown') or contains(@class, 'form-check')]//label"))
        )

        # Loop through options to find "Importer un CV"
        for option in dropdown_options:
            text = option.text.strip()
            if "Importer un CV" in text:
                option.click()
                break
        
    except Exception as e:
        print(f"Error selecting 'Apply with CV' and 'Import a CV': {e}")


def fill_and_submit(driver, cv_path, message):

    try:
        wait = WebDriverWait(driver, 10)

        if message :
            pass

        print('Selecting importer cv :')
        select_importer_cv(driver)

        # Upload CV file
        cv_upload = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
        cv_upload.send_keys(cv_path)


        # Uncheck Save CV if checked
        try:            
            # Localiser la case à cocher
            save_cv_checkbox = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='isCvSave']"))
            )

            # Vérifier si la case est cochée
            is_checked = save_cv_checkbox.is_selected()

            if is_checked:
                # Décochez la case si elle est cochée
                save_cv_checkbox.click()
                print("Checkbox 'Enregistrer le CV' était cochée, elle a été décochée.")
            else:
                print("Checkbox 'Enregistrer le CV' n'est pas cochée.")    
        except Exception as e:
            print(f"Erreur lors de la vérification de la case 'Enregistrer le CV': {e}")

        # Submit
        try:
            wait = WebDriverWait(driver, 10)
            
            # Localiser le bouton de soumission
            submit_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'btn btn-primary') and @title='Envoyer ma candidature']"))
            )
            
            # Pause optionnelle pour la stabilité
            time.sleep(1) 

            # Clic sur le bouton de soumission
            submit_button.click()
            print("Application submitted successfully!")
            return True

        except Exception as e:
            print(f"Error during submitting process: {e}")
            return False

        

    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error during the application process: {e}")


def read_login_credentials(filepath):
    """
    Reads email and password from a specified text file.
        filepath (str): Path to the login file.

    Returns:
        tuple: (email, password)
    """
    filepath = os.path.expanduser(filepath)

    # Read the file and extract email and password
    try:
        with open(filepath, 'r') as file:
            lines = file.read().splitlines()
            email = lines[0].strip()  # First line is the email
            password = lines[1].strip()  # Second line is the password
            return email, password
    except FileNotFoundError:
        print("Error: File not found.")
        return None, None
    
    except IndexError:
        print("Error: File format is incorrect. String! First line email, second line password.")
        return None, None
    

def postuler(driver):
    try:
        wait = WebDriverWait(driver, 10)
        # Click on the "Postuler" button
        connect_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//button[@type='submit' and contains(@class, 'popin-btn')])[2]"))
        )
    except Exception as e:
        print(f"Error checking first apply button: {e}")
        return False


def connected(driver):
    """
    Checks if the user is already connected by looking at the navigation bar.
    - Returns True if the user is logged in.
    - Returns False if the user is not logged in.
    """
    try:
        wait = WebDriverWait(driver, 5)

        # Check for the logged-in link (with class 'logged')
        logged_in_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'nav-link-espace')]"))
        )

        # Determine if the user is logged in or not
        if "logged" in logged_in_element.get_attribute("class"):
            username = logged_in_element.find_element(By.TAG_NAME, "span").text
            print(f"User is connected: {username}")
            return True
        else:
            print("User is NOT connected (Mon espace).")
            return False

    except Exception as e:
        print(f"Error checking connection status: {e}")
        return False


def promotion_or_formulaire(driver):
    current_url = driver.current_url
    # Check if the user is on the promotion URL (not connected)
    if "promotion" in current_url:
        return False
    
    # Check if the user is on the formulaire URL (connected)
    if "formulaire" in current_url:
        print("User is connected.")
        return True


def apec_connect(driver, usr, password):
    try:
        wait = WebDriverWait(driver, 10)
        
        # Wait and fill email
        email_input = wait.until(
            EC.visibility_of_element_located((By.XPATH, "(//input[@id='emailid'])[2]"))
        )
        email_input.clear()
        email_input.send_keys(usr)
        print("Email filled")

        # Wait and fill password
        password_input = wait.until(
            EC.visibility_of_element_located((By.XPATH, "(//input[@id='password'])[2]"))
        )
        password_input.clear()
        password_input.send_keys(password)
        print("Password filled.")

        # Click on the "Se connecter" button
        connect_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//button[@type='submit' and contains(@class, 'popin-btn')])[2]"))
        )
        connect_button.click()
        print("Clicked the connect button.")

        # time.sleep(2) 
        return driver

    except TimeoutException:
        print("Erreur : Formulaire de connexion non trouvé.")
        return driver

    except Exception as e:
        print(f"Erreur lors de la connexion : {e}")
        return False


def check_easy_apply(url):

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 6)
        driver.get(url)

        #  Cookie Handling
        try:
            cookie_wait = WebDriverWait(driver, 2)
            close_banner = cookie_wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            close_banner.click()
            print("Closed cookie consent banner.")
        except TimeoutException:
            print("No cookie consent banner found, continuing immediately.")

        # Locate the "Postuler" button
        try:            
            apply_button = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[contains(@class, 'btn-primary') and contains(text(), 'Postuler')]")
                )
            )
            button_text = apply_button.text.strip()

            # Easy Apply
            if button_text == "Postuler":
                print("Easy Apply button found.")
                apply_button.click()                
                time.sleep(2)  
                return driver 
            

            # Website
            elif "Postuler sur le site" in button_text:
                print("Complicated Apply button found (redirects to external site).")
                return False  
            
            # No longer Available
            else:
                print("Unknown apply button text.")
                return False
        except TimeoutException:
            print("No apply button found.")
            driver.quit()
            return False   
    except Exception as e:
        print(f"Error during checking apply possibility: {e}")
        driver.quit()
        return False


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


