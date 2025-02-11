
# Apec Auto Applier

This Python project automates the process of extracting job application links and applying to them using a personal apec account, a stored CV and personalized message.

## Project Structure
- **`JobLinks/links.json`**: Input JSON file (that you should edit) containing job search links to process. 
- **`JobLinks/Applications.csv`**: Output CSV file (that will be created) storing extracted application links.

⚠️ **CAUTION:** Links in `links.json` should all finish with `&page=` (check the existing example in the `links.json` file)
  - If the copied link doesn’t contain `&page=` at the end, append it.  
  - If the copied link has `&page=2` or any other number, just remove the number.  


## Prerequisites
- Python 3.8+
- Required Python packages: `selenium`, `python-dotenv`, `pandas`

## Setup Instructions

### 1. **Adjust Configuration Files**
- **`links.json`**: Update this file with APEC job search links (ensure all URLs are from the APEC platform):
  ```json
  {
    "links": [
      {"url": "https://www.apec.fr/candidat/offres-emploi.html#link_1", "number_of_offers": 50},
      {"url": "https://www.apec.fr/candidat/offres-emploi.html#link_2", "number_of_offers": 30}
    ]
  }


- **`.env` file**: Create this file to securely store your login credentials:
  ```env
  APEC_USERNAME=your_username
  APEC_PASSWORD=your_password
  ```

### 2. **Set Up Your CV and Message**
- **CV Path**: Update the `cv_path` variable in the script with the path to your CV.
- **Message**: Customize the `message` variable to include a personalized note for each application.

### 3. **Run the Script**
To start extracting and applying:
```bash
python main.py
```

## Workflow

### Extract and Save Applications
1. **Extract Links**: Retrieve job links from `links.json`.
2. **Store in CSV**: Save the extracted links to `Applications.csv`.

### Auto-Apply Process
1. **Retrieve Applications**: Load application links from the CSV.
2. **Automate Application**: Uses Selenium to submit your CV and message.

### Partial Execution
If the process is interrupted, manually set counters (`links_counter`, `submitted_counter`, etc.) to resume from where it left off.

## Troubleshooting
- Ensure all dependencies are installed.
- Verify correct paths for `links.json`, `Applications.csv`, and your CV file.
- Check `.env` file for proper configuration.

---

Happy Applying! 🚀
