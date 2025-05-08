# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

import pandas as pd

import logging

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

def main():
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()

    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to set the WebDriver path
    bot.driver_path = r"C:\chromedriver-win64\chromedriver.exe"
 
    # Variables
    excel_path = r"challenge.xlsx"
    logfile_name = r"logfile\dateLog.txt"
    df = pd.read_excel(excel_path)

    try:
        # Logfile settings
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
                
        # Beginning of project
        logging.info("Início - RPA Challenge")    
        bot.browse("https://rpachallenge.com/")
        logging.info("Abre o website")
        bot.wait(3000)
        
        # Obtaining buttons
        submit_btn = bot.find_element("//input[@class='btn uiColorButton']", By.XPATH)
        start_btn = bot.find_element("//button", By.XPATH)

        start_btn.click()
        logging.info("Clica no botão 'Start'")
   
        # Dictionary to store column and xpath
        fields = {
            0: "//rpa1-field[@ng-reflect-dictionary-value='First Name']//input",
            1: "//rpa1-field[@ng-reflect-dictionary-value='Last Name']//input",
            2: "//rpa1-field[@ng-reflect-dictionary-value='Company Name']//input",
            3: "//rpa1-field[@ng-reflect-dictionary-value='Role in Company']//input",
            4: "//rpa1-field[@ng-reflect-dictionary-value='Address']//input",
            5: "//rpa1-field[@ng-reflect-dictionary-value='Email']//input",
            6: "//rpa1-field[@ng-reflect-dictionary-value='Phone Number']//input"
        }
        logging.info("Define um dicionário que guarda coluna e xpath")
        
        logging.info("Início do Loop")
        # For each row in dataframe
        for i, row in df.iterrows():   
            try:
                # For each column and xpath in dictionary (fields)
                for column, xpath in fields.items():   
                    # Obtain the element
                    input_field = bot.find_element(xpath, By.XPATH)
                    # Write in the input
                    input_field.send_keys(row.iloc[column])
                    
                logging.info(f"Linha {i} preenchida")   
                submit_btn.click()  

            except Exception as e:
                print(f"Erro encontrado na linha {i}: {type(e).__name__}")
     
        logging.info("Fim do Loop")
        # Obtain success message
        success_message = bot.find_element("//div[@class='message2']", By.XPATH)
        logging.info(success_message.text)
                      
    except Exception as e:
        logging.info(f"Erro encontrado: {type(e).__name__}")


    # Wait 3 seconds before closing
    bot.wait(3000)

    # Close browser
    bot.stop_browser()
    logging.info("Fecha o navegador")
    logging.info("Sucesso - RPA Challenge") 
    add_breakline(logfile_name) 

def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
