import pandas as pd # Collect transfer values of players with over 900 Premier League minutes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

input_file = 'SourceCode/problem-1/results.csv'
output_file = 'SourceCode/problem-4/results.csv'

url = 'https://www.footballtransfers.com/en'

df = pd.read_csv(input_file)
players = df[df['Min'] > 900][['Player', 'Pos', 'Team', 'Age', 'Min']]

# Setup Chrome
options = Options()
options.add_argument("--headless")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--disable-notifications')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Setup Driver
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(url)
driver.implicitly_wait(10)

# Setup Actions and Wait
actions = ActionChains(driver)
wait = WebDriverWait(driver, 15)

# Close notification popup
try:
    close_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@title='Close']"))
    )
    close_button.click()
    print('Close a successful notification popup')
except:
    print('No notification popup to close')

# Hover tab "Players"
players_tab = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[@title='Players']"))
)
actions.move_to_element(players_tab).perform()
time.sleep(1.5)

# Click "All Premier League Players"
all_premier_league_players = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[@title='All Premier League Players']"))
)
all_premier_league_players.click()
print('Successfully visit the All Premier League Players website!')
driver.implicitly_wait(10)

all_players = []
page = 0

# Data Scraping
while True:
        next_button = driver.find_element(By.CLASS_NAME, 'pagination_next_button')

        page += 1
        print(f'Retrieving data from page {page}' , end=' | ')

        rows = driver.find_elements(By.CSS_SELECTOR, "#player-table-body tr")
        for row in rows:
            skill = row.find_element(By.CSS_SELECTOR, 'div.table-skill__skill').text
            pot = row.find_element(By.CSS_SELECTOR, 'div.table-skill__pot').text    

            all_players.append({
                'Skill / Pot' : f'{skill} / {pot}',
                'Player': row.find_element(By.CSS_SELECTOR, "div.text a").text.strip(),
                'ETV': row.find_element(By.CSS_SELECTOR, 'td.text-center span.player-tag').text.strip()
            })
        print('Complete data retrieval!')
        
        if next_button.get_attribute('disabled'): break
        next_button.click()
        time.sleep(1.5)

res = pd.DataFrame(all_players)
players = pd.merge(players, res, on='Player', how='inner')
players.to_csv(output_file, index=False)
print('Successful save to csv!')