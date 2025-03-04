from playwright.sync_api import sync_playwright
import json
import os
from find_router_ip import find_router_ip

def load_config(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def time_to_seconds(t):
    h, m, s = map(int, t.split(':'))
    return h * 3600 + m * 60 + s

def scrape_clients(router_ip):
    with sync_playwright() as p:
        # Configuration for launching the browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the router login URL
        router_login_url = f"http://{router_ip}{ROUTER_LOGIN_PAGE}"
        page.goto(router_login_url)

        # If Sign In not visible, print display text and close
        if not page.is_visible('[value="Sign In"]'):
            nologin_text = page.query_selector('.nologin').inner_text()
            print(f'Unable to log in: {nologin_text}')
            browser.close()
            return

        # If Captcha active, print and exit
        if page.is_visible('#captcha_input_div'):
            print('Unable to log in: Captcha is required')
            browser.close()
            return

        # Enter login info
        page.type('#login_username', ROUTER_USER)
        page.type('[name="login_passwd"]', ROUTER_PASS)

        # Click sign in button
        page.click('[value="Sign In"]')
        page.wait_for_load_state("networkidle")  # Wait for navigation
        
        # If error status visible, print error text and close
        if page.is_visible('.error_hint'):
            error_text = page.query_selector('.error_hint').inner_text()
            print(f'Login failed: {error_text}')
            browser.close()
            return

        # Click client list view button
        page.click('[onclick="pop_clientlist_listview(true)"]')
        page.wait_for_timeout(1000)

        # Evaluate JavaScript in the context of the page to get client names
        clients = page.evaluate('''() => {
            const client_rows = document.querySelectorAll('.viewclientlist_clientName_edit');
            return Array.from(client_rows, row => row.innerHTML);
        }''')

        rows = page.query_selector_all(".list_table tr")

        all_data = []
        for row in rows:
            tds = row.query_selector_all("td")
            try:
                client_title = tds[1].query_selector('div').get_attribute('title')
            except Exception as e:
                client_title = "N/A"

            row_data = [td.inner_text() for td in tds]

             # Extract the title property of the "clientIcon_no_hover" div
            # client_type = [tds[2].query_selector('.clientIcon_no_hover').get_attribute('title')]
            # print(client_type)

            row_data.append(client_title)

            all_data.append(row_data)


        user_list = []
        wireless_users = []
        wired_users = []
        for data_row in all_data:
            if len(data_row) > 7:
                user_name = data_row[2]
                access_time = data_row[8]
                client_type = data_row[9]
                user_info = {"user_name": user_name, "access_time": access_time, "client_type": client_type}
                try:
                    # Check if access_time is valid
                    time_to_seconds(access_time)
                    wireless_users.append(user_info)
                except ValueError:
                    wired_users.append({"user_name": user_name, "access_time": "-", "client_type": client_type})

        # List of users sorted by time
        sorted_wireless_users = sorted(wireless_users, key=lambda x: time_to_seconds(x["access_time"]))  
        sorted_users = sorted_wireless_users + wired_users

        # Print client list
        print('Client list:')
        for user in sorted_users:
            print(f'{user["user_name"][:20]:<20} {user["access_time"]:9} {user["client_type"]}')

        # Cleanup
        browser.close()

# Load config and credentials
working_dir = os.getcwd()
config = load_config(f'{working_dir}/credentials/router.json')
ROUTER_USER = config['ROUTER_USER']
ROUTER_PASS = config['ROUTER_PASS']
ROUTER_LOGIN_URL = config['LOGIN_URL']
ROUTER_LOGIN_PAGE = config['LOGIN_PAGE']

# Find router IP address
router_ip = find_router_ip()
if router_ip:
    print(f"Router IP address found: {router_ip}")
    # Run the scraper function with router IP found
    scrape_clients(router_ip)
else:
    print("Router IP address could not be determined")
