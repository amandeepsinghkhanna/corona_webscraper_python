"""
    @script-author: Amandeep Singh Khanna
    @script-description: Python script to webscrape corona numbers from the Ministry of Health India website.
"""

# importing standard python modules:
import os  # for interfacing with the operating system.
import datetime # for datetime operations.
import logging  # for creating code execution log.

# importing PYPI modules:
import pandas as pd  # for interfacing with the pandas DataFrame objects.

# setting the working directory: 
os.chdir("D:\\Personal Files\\corona india web scraping python\\")

# setting the logging configuration:
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s -  %(levelname)s - %(message)s ",
    handlers=[
        logging.FileHandler("corona_scraper.log"),
        logging.StreamHandler(),
    ],
)

# user-defined function to extract the website information:
def extract_website_data(url):
    try:
        table_list = pd.read_html(url)
        corona_table = table_list[0]
        
        # keeping only required columns in the extracted table:
        corona_table = corona_table.iloc[:, 1:]
        
        # renaming columns in the extracted table:
        corona_table.columns = [
                'region',
                'confirmed',
                'recovered',
                'deaths'
        ]        
        
        # filtering only required rows in the extracted table:
        corona_table = corona_table[
            corona_table["region"].isin([ 'Andhra Pradesh', 'Andaman and Nicobar Islands',
            'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Delhi', 
            'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 
            'Karnataka', 'Kerala', 'Ladakh', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 
            'Mizoram', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Tamil Nadu', 
            'Telengana', 'Uttarakhand', 'Uttar Pradesh', 'West Bengal'
            ])
        ]
        
        corona_table['timestamp'] = datetime.datetime.now()
        
        return corona_table
        
    except Exception as e:
        logging.exception(f"Error in extraction of the table from website - {url}")

# user-defined function to store the extracted table:        
def store_extracted_data(corona_table, filename = 'corona_data.csv'):

    # Checking if the file exists:
    header_required = True
    
    if os.path.isfile('corona_data.csv'):

        header_required = False
        logging.debug("The file already exists.")
    try:
        corona_table.to_csv(filename, index=False, sep=',', header=header_required, mode='a')
    except Exception as e:
        logging.exception(f"Error occured in storing the extracted data")


# user-defined wrapper function:
def run_code(url):
    logging.info("Execution begins ")
    corona_table = extract_website_data(url)
    store_extracted_data(corona_table)
    logging.info("Execution sucessfully completed")
    
if __name__ == "__main__":
    url = 'https://www.mohfw.gov.in/'
    run_code(url)