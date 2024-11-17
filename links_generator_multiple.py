from Functions.sorting_functions import *
import json
from pathlib import Path
import math
import  csv

current_working_directory = Path.cwd()


directory = "JobLinks"
input_file = "links.json"

multiple_links_path = current_working_directory / directory / input_file

filepath = os.path.expanduser(multiple_links_path)


with open('links.json', 'r') as file:
    data = json.load(file)

big_links_count = 0
list_all_app_links = []

for entry in data['links']:
    url = entry['url']
    number_of_offers = entry['number_of_offers']
    page_max = math.ceil(number_of_offers/20)
    big_links_count += 1
    print(f'Extracting links from link number : {big_links_count}')
    app_links_per_page = [get_job_links(url+str(page_n)) for page_n in range(page_max)]   
    flat_list_links = [item for sublist in app_links_per_page for item in sublist] 
    list_all_app_links.append(flat_list_links)



final_big_list = [item for sublist in list_all_app_links for item in sublist]

print(f'Le nombre de liens obtenus est : {len(final_big_list)}')

current_working_directory = Path.cwd()
directory = "JobLinks"
output_file = "All_job_links.csv"

# Use Path to join the components
output_path = current_working_directory / directory / output_file

output_path.parent.mkdir(parents=True, exist_ok=True)

with open(str(output_path) , mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    writer.writerow(["Data Scientist Job Links"])
    
    # Write each link as a new row
    for link in final_big_list:
        writer.writerow([link])

print(f"Links have been written to {output_file}")