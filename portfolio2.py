import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

EMAIL = "Your Email"
PASSWORD = "Your Password"
ID = "You Unique ID"
first_trade = True

desired_profit = float(input("Enter the profit you want: $"))

driver = uc.Chrome()
driver.implicitly_wait(15)
driver.get("https://qxbroker.com/en")
driver.maximize_window()



def press_up():
    """ This Function will Press the Up Button """
    btn_Up = driver.find_element(
        By.XPATH, '//div[@class="section-deal__success  percent"]')
    btn_Up.click()




def press_down():
    """ This Function will Press the Down Button """
    btn_Down = driver.find_element(
        By.XPATH, "//button[@class='button button--danger button--spaced put-btn section-deal__button ']")
    btn_Down.click()


def initial_trade_value(initial_amount):
    """ This Function will set the initial value for the First trade 
        when we are Randomly Pressing a Button"""

    investment_section = driver.find_element(
        By.XPATH, '//*[@id="root"]/div/div[1]/main/div[2]/div[1]/div/div[5]/div[2]/div/div/input')
    investment_section.click()
    investment_section.send_keys(Keys.CONTROL + 'a')
    investment_section.send_keys(Keys.BACK_SPACE)
    investment_section.send_keys(initial_amount)


# Changing Amount Function
def click_investment_section(new_amount):
    """ This Function will set the value for the next trades after the first trade
        is done by a Random Button Press"""

    investment_section = driver.find_element(
        By.XPATH, '//*[@id="root"]/div/div[1]/main/div[2]/div[1]/div/div[5]/div[2]/div/div/input')
    investment_section.click()
    investment_section.send_keys(Keys.CONTROL + 'a')
    investment_section.send_keys(Keys.BACK_SPACE)
    investment_section.send_keys(new_amount)


# Getting Time
def current_time():
    """ Returns Every Second of a Minute"""
    timer = driver.find_element(By.XPATH, '//div[@class="server-time online"]')
    sp = timer.text.split()
    real_time = sp[0]
    # Extract the seconds part (last 2 characters in the time string)
    seconds_part = real_time[-2:]
    # time.sleep(1)
    return seconds_part


# Starting of the Code


element = driver.find_element(By.XPATH, "//*[@id='top']/div/div[1]/a[2]")
element.click()


# time.sleep(2)
email_entry = driver.find_element(
    By.XPATH, "//*[@id='tab-1']/form/div[1]/input").send_keys(EMAIL)
password_entry = driver.find_element(
    By.XPATH, "//*[@id='tab-1']/form/div[2]/input").send_keys(PASSWORD)
signin_button = driver.find_element(
    By.XPATH, "//*[@id='tab-1']/form/button/div").click()

# input()           


print("Reached here")
time.sleep(5)
u_menu = driver.find_element(
    By.XPATH, "//div[@class='usermenu__info-wrapper']")
u_menu.click()

# User ID Checking
span_user_id = driver.find_element(
    By.XPATH, "//*[@id='root']/div/div[1]/header/div[8]/div[2]/div[2]/ul[1]/li[1]/div[2]/div/span")
# ------- Picking The text of span_tag containing User ID in a String "ID: 32878617"
user_id_string = span_user_id.text

# ------- Converting the String into a list by splitting it through the space
#         so that we have a list = ["ID:", "39289547"].Now we have the ID Number separate
#         so that we can match it Easily

user_id_list = user_id_string.split()
real_user_id = int(user_id_list[1])

try:
    if real_user_id == ID:
        dm_ac_menu = driver.find_element(
            By.XPATH, "//*[@id='root']/div/div[1]/header/div[8]/div[2]/div[2]/ul[1]/li[3]/a")
        dm_ac_menu.click()
        close_button = driver.find_element(
            By.XPATH, "//*[@id='root']/div/div[3]/div/div/div/div[2]/button").click()

        time.sleep(10)
        current_profit = 0

        initial_trading_amount = int(
            input("Set your initial trading amount here: $"))
        # Track the current trading amount
        current_trading_amount = initial_trading_amount
        initial_trade_value(initial_trading_amount)

        # Initialize previous demo account money
        demo_account_money = driver.find_element(
            By.XPATH, "//*[@id='root']/div/div[1]/header/div[8]/div[2]/div/div[3]/div[2]")
        dollars = demo_account_money.text
        previous_demo_account_money = float(dollars[1:].replace(',', ''))

        buttons = [press_up, press_down]
        current_btn = random.choice(buttons)

        # Starting the loop for doing the tradings until the User gets his Desired Profit
        while True:
            string_seconds = current_time()
            d = int(string_seconds)

            # Condition to place a trade at the start of each minute (when seconds are 0)
            if d == 0:
                # time.sleep(2)
                # Choose a random button to press in the first trade
                if first_trade:
                    current_btn = random.choice(buttons)
                    current_btn()
                    first_trade = False
                    time.sleep(2)
                else:
                    # time.sleep(1)
                    print(previous_demo_account_money)
                    # Calculate profit after the trade
                    demo_account_money = driver.find_element(
                        By.XPATH, "//*[@id='root']/div/div[1]/header/div[8]/div[2]/div/div[3]/div[2]")
                    dollars = demo_account_money.text
                    current_demo_account_money = float(
                        dollars[1:].replace(',', ''))
                    print(current_demo_account_money)
                    profit = current_demo_account_money - previous_demo_account_money
                    # Introducing r_profit variable for storing the changes made in every trade
                    r_profit = profit

                    # Update current profit for the next iteration
                    current_profit += int(profit)

                    print(f"Profit after trade: ${profit}")
                    print(f"Current Profit: ${current_profit}")

                    # Update previous demo account money for the next iteration
                    previous_demo_account_money = current_demo_account_money

                    time.sleep(5)

                    # Check if the desired profit is reached
                    if current_profit >= desired_profit:
                        print(f"Desired profit of ${
                              desired_profit} reached. Stopping the program.")
                        driver.quit()
                        break

                    # Reset the amount to the initial value after a profit
                    if r_profit >= 0:
                        time.sleep(0.5)
                        current_trading_amount = initial_trading_amount
                        # Click the button and update the investment amount
                        click_investment_section(current_trading_amount)
                        current_btn()

                    else:
                        time.sleep(1)
                        # Double the amount in the next iteration if there is a loss
                        current_trading_amount = str(
                            int(current_trading_amount) * 2)
                        # Switch the button in the next iteration
                        current_btn = press_down if current_btn == press_up else press_up

                        # Click the button and update the investment amount
                        click_investment_section(current_trading_amount)
                        current_btn()

                    r_profit = 0       # Here we are making r_profit zero or empty

except:
    print("Something went wrong.")
