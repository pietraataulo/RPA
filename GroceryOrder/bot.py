# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

import os

import logging

import pandas as pd

import traceback
import requests

list_path = "shopping-list.csv"

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()
    
    file_url = "https://aai-devportal-media.s3.us-west-2.amazonaws.com/challenges/shopping-list.csv" 

    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to set the WebDriver path
    bot.driver_path = r"C:\chromedriver-win64\chromedriver.exe"
       
    # Credentials
    username = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    
    # Websites Link
    shopping_weblink = "https://pathfinder.automationanywhere.com/challenges/AutomationAnywhereLabs-ShoppingList.html?_fsi=MZ1nc3Vl"
    
    try:
        # Logfile config
        logfile_name = r"logfile\dateLog.txt"
        logging.basicConfig(
            filename=logfile_name,
            level=logging.INFO,
            format="(%(asctime)s) %(message)s",
            datefmt="%d/%m/%Y %H:%M:%S",
            encoding= "utf-8"
        )
   
        # Add a breakline in logfile
        def add_breakline(logfile_name):
            with open(logfile_name, "a", encoding = "utf-8") as log_file:
                log_file.write("\n")

        # Open Challenge website
        logging.info("Início - Atividade Online Grocery Ordering")
        bot.browse(shopping_weblink)
        logging.info("Abre o website")


        # Automation Anywhere Community Login
        bot.wait(10000)
        
        cookies_btn = bot.find_element("//button[@id='onetrust-accept-btn-handler']", By.XPATH)
        cookies_btn.click()   # Click OK on Cookies button

        community_btn = bot.find_element("//button[@id='button_modal-login-btn__iPh6x'][1]", By.XPATH)
        community_btn.click()  # Select Community login option

        email_input = bot.find_element("//input[@placeholder='*Email']", By.XPATH)
        email_input.send_keys(str(username))  # Enter email

        next_btn = bot.find_element("(//button)[1]", By.XPATH)
        next_btn.click()  # Click on Next button

        password_input = bot.find_element("//input[@placeholder='Password']", By.XPATH)
        password_input.send_keys(str(password))  # Enter password

        login_btn = bot.find_element("(//button)[2]", By.XPATH)
        login_btn.click()   # Click on Login button
        bot.wait(3000)
 
        # Beginning of project - Online Grocery Ordering
        # Downloading CSV file
        response = requests.get(file_url)
        
        # Remove file if it already exists
        if os.path.exists(list_path) and os.path.isfile(list_path):
            os.remove(list_path)
            logging.info(f"Arquivo {list_path} removido")

        destination_folder = r"GroceryOrder\shopping-list.csv"

        # Check if the request was successful 
        if response.status_code == 200:
            # Write the content of the response to a file
            with open(destination_folder, 'wb') as file:
                file.write(response.content)
            logging.info(f"Arquivo baixado com sucesso: {destination_folder}")
        else:
            print(f"Não foi possível baixar o arquivo: {response.status_code}")

        df = pd.read_csv(list_path)
        logging.info("Lê o arquivo CSV")

        # Capturing input field, add button, agree to terms button and submit
        input_field = bot.find_element("//input[@id='myInput']", By.XPATH)
        add_btn = bot.find_element("//button[@id='add_button']", By.XPATH)
        yes_terms = bot.find_element("//input[@value='option1']", By.XPATH)
        submit_btn = bot.find_element("//button[@id='submit_button']", By.XPATH)

        # For each row in dataframe
        for index, row in df.iterrows():
            input_field.send_keys(row.iloc[1])  #  Write items from column 2 in the input field
            add_btn.click()  #  Click on "Add"
            logging.info(f"{row.iloc[1]} adicionado!")

        yes_terms.click()
        logging.info("Clica no botão Aceitar Termos")
        submit_btn.click()
        logging.info("Clica em 'Submit'")

        bot.wait(4000)
          
        # Capturing accuracy and closing the page
        accuracy = bot.find_element("//h3[@id='accuracy']", By.XPATH)
        logging.info(f"Precisão: {accuracy.text}")
        logging.info("Fecha a janela")
        logging.info("Sucesso - Online Grocery Ordering")
       
    except Exception as e:
        logging.info(f"Erro encontrado: {type(e).__name__}")
        traceback.print_exc()

    add_breakline(logfile_name)
    # Wait 3 seconds before closing
    bot.wait(3000)

    # Finish and clean up the Web Browser
    # You MUST invoke the stop_browser to avoid
    # leaving instances of the webdriver open
    bot.stop_browser()

def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()