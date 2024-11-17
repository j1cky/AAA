import tqdm
from Functions.sorting_functions import *
import csv

"""
py code same as all_apply.ipynb to be used with terminal 
"""

current_working_directory = Path.cwd()
directory = "JobLinks"
input_file = "All_job_links.csv"
output_path = current_working_directory / directory / input_file


links_list = []

with open(str(output_path), mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader, None)  # Skip the header row if present
    
    # Append each link to the list
    for row in reader:
        if row:  # Check if row is not empty
            links_list.append(row[0])  # Access the first column (link)

print("Retrieved links from CSV:")
links_list[:5]


print('\nList of links has been extracted\n')





cv_path = '/home/ocr8n/Documents/CV_Aziz_ISC.pdf'
message = ''



links_counter = 0
submitted_counter = 0
applied_counter = 0
external_links_counter = 0
not_available_counter = 0
external_links_list = []


login_file_path = "~/Documents/GitHub/login.txt"
usr, password = read_login_credentials(login_file_path)


for link in tqdm.tqdm(links_list):
    links_counter += 1
    print('________________________________________________\n')
    print(f'Link number : {links_counter}\n')
    print('\n First step, Can I apply easily?\n')
    driver,note = check_easy_apply(link)

    match note:
            case 1:
                print('Yes !! Easy apply found\n')
                print('connecting ....\n')
                driver = apec_connect(driver, usr, password)
                print('connected !! \n')

                if not already_applied(driver):
                    fill_and_submit(driver, cv_path, message)
                    time.sleep(2)
                    driver.quit()
                    print("Submitted, everything fine")
                    submitted_counter += 1

                else:
                    driver.quit()
                    print('Great !! I already applied to this job.')                    
                    applied_counter += 1

            case 2:
                print('Unfortunately, External website link  :(')                
                driver.quit()
                external_links_counter += 1
                external_links_list.append(link)

            case 3:
                print('probably the announcement is no longer available')
                driver.quit()
                not_available_counter += 1
    
        

# Summary of the results
print('\n\nSummary of Application Process:')
print('--------------------------------')
print(f'Total links processed: {links_counter}')
print(f'Successfully submitted applications: {submitted_counter}')
print(f'Already applied: {applied_counter}')
print(f'External website links: {external_links_counter}')
print(f'Announcements no longer available: {not_available_counter}')

