import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# Replace with your actual Gemini API key
API_KEY = "A........."

# Initialize Gemini AI client
genai.configure(api_key=API_KEY)

def scrape_website(url):
    """
    Scrapes text content from the given URL.
    """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract all text from paragraphs
            paragraphs = soup.find_all('p')
            text_content = " ".join([p.get_text() for p in paragraphs])

            return text_content if text_content else "No text found on the page."
        else:
            return f"Failed to retrieve content. Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching the webpage: {e}"

def analyze_with_gemini(text):
    """
    Sends scraped text to Gemini AI and returns a summary.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Summarize this content: {text}")
        return response.text if response.text else "No AI response received."
    except Exception as e:
        return f"Error with AI response: {e}"

def main():
    url = input("Enter the website URL to scrape: ").strip()
    scraped_content = scrape_website(url)

    if "Error" not in scraped_content:
        print("\n🔍 Scraped Content (First 500 characters):\n", scraped_content[:500], "...")
        summary = analyze_with_gemini(scraped_content)
        print("\n🤖 AI Summary:\n", summary)
    else:
        print(scraped_content)

if __name__ == "__main__":
    main()
