import time
import json
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import Page
import ollama
from .config import CHROME_EXECUTABLE_PATH, USER_AGENT, VIEWPORT, SCROLL_WAIT, MAX_SCROLLS, LLM_MODEL
from .utils import safe_text


class GoogleMapsScraper:
    def __init__(self, page: Page):
        self.page = page

    def open_google_maps(self):
        self.page.goto("https://www.google.com/maps", timeout=60000)
        self.page.wait_for_selector("id=searchbox")

    def scroll_results_feed(self):
        print("\U0001F4DC Scrolling inside the listings feed panel...")
        last_count = 0
        stagnant_scrolls = 0
        for scroll_round in range(MAX_SCROLLS):
            count = self.page.locator("div.TFQHme").count()
            print(f"\U0001F501 Scroll {scroll_round+1}: {count} listings visible")
            self.page.evaluate("""
                () => {
                    const feed = document.querySelector('[role="feed"]');
                    if (feed) {
                        feed.scrollBy(0, feed.scrollHeight);
                    }
                }
            """)
            time.sleep(SCROLL_WAIT)
            new_count = self.page.locator("div.TFQHme").count()
            if new_count == last_count:
                stagnant_scrolls += 1
                if stagnant_scrolls >= 3:
                    print("\u2705 No new listings loaded after 3 scrolls. Done.")
                    break
            else:
                stagnant_scrolls = 0
            last_count = new_count
        return new_count

    def extract_ai_data(self, prompt: str, html_content: str):
        response = ollama.chat(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": html_content}
            ]
        )
        try:
            content = response['message']['content']
            if '```json' in content:
                json_content = content.split('```json')[1].split('```')[0]
            else:
                json_content = content
            return json.loads(json_content)
        except json.JSONDecodeError:
            print("\u274C Failed to parse JSON response")
            return None

    def parse_overview_data(self, df: pd.DataFrame):
        print("Parsing overview data from Google Maps results...")
        all_queries_data = []
        for index, row in df.iterrows():
            query = row['search_query']
            user_name = row['UserName']
            print(f"Searching: {index+1}:{query} ")
            self.open_google_maps()
            search_box = self.page.get_by_role("combobox")
            search_box.wait_for(state="visible", timeout=10000)
            search_box.click()
            search_box.fill(query)
            search_box.press("Enter")
            time.sleep(5)
            print("\U0001F4DC Scrolling to load all listings...")
            self.scroll_results_feed()
            html_content = self.page.content()
            soup = BeautifulSoup(html_content, "html.parser")
            cards = soup.select('div.Nv2PK.THOPZb.CpccDe')
            print(f"\U0001F4E6 Found {len(cards)} business cards")
            for card in cards:
                prompt = """
                From the provided HTML of a Google Maps search result card, extract the following:
                - name
                - address
                - rating
                - number of reviews
                - price range
                - type of restaurant or service
                - maps URL

                Return only JSON formatted object with these fields. Do not include any other text or comments.
                """
                html_card = str(card)
                data = self.extract_ai_data(prompt, html_card)
                all_queries_data.append(data)
            search_box.clear()
        return all_queries_data