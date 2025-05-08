# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

import os

import logging

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

    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to set the WebDriver path
    bot.driver_path = r"C:\chromedriver-win64\chromedriver.exe"
     
    # Credentials
    username = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    
    # Websites Links
    decoder_weblink = "https://pathfinder.automationanywhere.com/challenges/AutomationAnywhereLabs-Translate.html?_fsi=MZ1nc3Vl"
    translator_link = "https://translate.glosbe.com/bg-en"
    
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
        logging.info("Início - Atividade Message Decoder")
        bot.browse(decoder_weblink)
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

        # Beginning of project - Message Decoder
        # Obtaining bulgarian text to translate  
        bulgarian_text = bot.find_element("(//h2)[1]", By.XPATH).text
        bulgarian_text = bulgarian_text.split(":", 1)[1]
        logging.info("Captura e recorta o texto em búlgaro")
        
        # Using a website to translate
        bot.create_tab(translator_link)
        logging.info("Abre o tradutor em outra aba")
        text_area = bot.find_element("//textarea", By.XPATH)
        text_area.send_keys(bulgarian_text)
        logging.info("Escreve o texto no tradutor")
        
        bot.wait(5000)
        
        # Obtaining the translation result
        translation = bot.find_element("//div[@class='w-full sm:w-1/2 px-0'][2]", By.XPATH)
        translation_text = translation.text
        logging.info("Captura o texto traduzido para inglês")

        # Switching tab
        opened_tabs = bot.get_tabs()
        new_tab = opened_tabs[0]
        bot.activate_tab(new_tab)

        bot.wait(3000)

        # Submitting the translation 
        input_field = bot.find_element("//input[@id='message_input']", By.XPATH)
        input_field.send_keys(translation_text)
        logging.info("Escreve a tradução no input")

        submit_btn = bot.find_element("//a[@class='btn btn-primary mt-auto']", By.XPATH)
        submit_btn.click()
        logging.info("Clica no botão 'Submit'")

        bot.wait(2000)
        
        # Capturing accuracy and closing the page
        accuracy = bot.find_element("//h3[@id='accuracy']", By.XPATH)
        logging.info(f"Precisão: {accuracy.text}")
        logging.info("Fecha a janela")
        logging.info("Sucesso - Atividade Message Decoder")
        add_breakline(logfile_name)

    except Exception as e:
        logging.info(f"Erro encontrado: {type(e).__name__}")


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
