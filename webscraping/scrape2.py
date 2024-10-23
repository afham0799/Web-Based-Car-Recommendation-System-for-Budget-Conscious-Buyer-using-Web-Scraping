import requests
from bs4 import BeautifulSoup

# Define the URL of the website you want to scrape
website_url = "https://carro.co/my/en?utm_source=google&utm_medium=sem&utm_campaign=2024_PM_GG_MY_WEB_BUY_SEM_LEADS_Generic-BuyUsedCars_AlwaysOn&utm_content=Retail_Search_ENG_SecondHand_Carro_699618049854&utm_term=second%20hand%20cars&gad_source=1&gclid=EAIaIQobChMIq5O607GlhgMVVAyDAx3idgmxEAAYASAAEgLJWvD_BwE&query=proton"

# Send a GET request to the website
response = requests.get(website_url)

# Check if the request was successful
if response.status_code == 200:
    print("Website can be accessed.")
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Example: Print the title of the webpage
    print("Title of the webpage:", soup.title.string)
    
    # Add more BeautifulSoup operations here as needed
    
    # Find all car items on the webpage
    car_items = soup.find_all("div", class_="car-item")
    
    # Iterate over each car item
    for car in car_items:
        # Extracting the price
        price = car.find("div", class_="browsing-card-price")
        if price:
            price_text = price.get_text(strip=True)
            print("Price:", price_text)
        else:
            print("Price not found.")
    
else:
    print(f"Failed to access the website. Status code: {response.status_code}")
