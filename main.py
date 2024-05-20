import random
import threading
import time
import capsolver
import loguru
import requests

capsolver.api_key = "CAP-6F1B2D1DF11F10A0134685C8E935839A"

class BajaBlastGen:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        self.proxy = random.choice(open("proxy.txt", "r").readlines()).strip()
        self.session.proxies = {
            'http': f'http://{self.proxy}',
            'https': f'http://{self.proxy}'
        }

    def get_signup_page(self):
        r = self.session.get("https://www.bajablast.com/register")

    def solve_captcha(self):
        captcha_token = capsolver.solve({
            "type": "AntiTurnstileTaskProxyLess",
            "websiteURL": "https://www.bajablast.com/register",
            "websiteKey": "0x4AAAAAAAPsjgqJ9Eop4Iv1",
            "metadata": {
                "action": "register"
            }
        })
        loguru.logger.info(f"CAPTCHA solved: {captcha_token}")
        return captcha_token

    def create_account(self, email):
        data = {
            'first_name': 'Jerad',
            'last_name': 'Snake',
            'email': email,
            'confirm_email': email,
            'password': 'Pizza12.',
            'confirm_password': 'Pizza12.',
            'mailing_address1': '9035 Mossy Oak Ln',
            'mailing_address2': '21',
            'city': 'Clermont',
            'state': 'Florida',
            'zipcode': '34711',
            'phone': '6028739739',
            'birthday': '02/16/2000',
            'agree_rules': 'on',
            'cf-turnstile-response': self.solve_captcha(),
        }

        response = self.session.post('https://www.bajablast.com/register', data=data)
        if response.status_code == 200:
            loguru.logger.success(f"[{email}] Account created.")
            open("submissions.txt", "a").write(f"{email}:Pizza12.\n")
        else:
            loguru.logger.error(f"[{email}] Account creation failed: {response.text}")

def generate_account():
    while True:
        gen = BajaBlastGen()
        email = f"jeradsnake{random.randint(100, 999)}@gmail.com"
        gen.get_signup_page()
        time.sleep(random.uniform(3, 8))  # Random delay between requests
        gen.create_account(email)
        time.sleep(random.uniform(1, 3))  # Random delay between account creations

if __name__ == '__main__':
    num_threads = int(input("Number of threads to use: "))
    for _ in range(num_threads):
        threading.Thread(target=generate_account).start()