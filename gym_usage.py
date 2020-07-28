try:

    # Import all necessary modules
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import json
    from bs4 import BeautifulSoup
    from datetime import datetime
    import time

    usage_df = pd.read_csv('usage.csv')


    def read_credentials(json_file):
        return json.load(open(json_file)) 


    def get_data(credentials):
        login = credentials['email']
        pin = credentials['pin']

        curr_date = datetime.today().strftime('%d/%m/%Y')
        curr_time = datetime.today().time().strftime('%H:%M')

        url = 'https://www.puregym.com/members/'

        driver = webdriver.Chrome('./chromedriver')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        
        driver.get(url)

        # Find the elements to add the email and pin and click to login
        email_el = driver.find_element_by_id('email')
        pin_el = driver.find_element_by_id('pin')

        email_el.send_keys(login)
        pin_el.send_keys(pin)

        # Log in
        login_btn = driver.find_element_by_id('login-submit')
        login_btn.click()

        time.sleep(5)

        # Get in and get the numbers
        usage_num = driver.find_element_by_xpath('//*[@id="main-content"]/div[3]/div/div/div[2]/div/div/div/div[1]/p/span')
        
        new_usage_df = pd.DataFrame(data={
                'Date': curr_date,
                'Time': curr_time,
                'Usage': usage_num.text,
                'Capacity': 119
            }, index=[0]
        )

        return new_usage_df


    def main():
        curr_usage_df = get_data(read_credentials('credentials.json'))

        # Create the main DF and save as csv
        main_usage_df = pd.concat([usage_df, curr_usage_df])
        main_usage_df.to_csv('usage.csv', index=False)


    if __name__ == "__main__":
        main()

except KeyboardInterrupt:
    pass