import requests
import pandas as pd
from bs4 import BeautifulSoup

# Function to scrape data for a given brand
def scrape_brand(brand):
    data = []
    current_page = 1
    proceed = True

    while proceed and current_page:
        print(f"Currently scraping page: {current_page} for brand: {brand}")
        url = f"https://www.oto.my/search/?keyword={brand}&pg=" + str(current_page)

        page = requests.get(url)
        soup = BeautifulSoup(page.text, "lxml")

        if soup.title and "-- No results were found --" in soup.title.text:
            proceed = False
        else:
            all_cars = soup.find_all("div", class_='results-container list-view')

            if not all_cars:
                print("No more cars found on page " + str(current_page))
                proceed = False
            else:
                for car in all_cars:
                    item = {"Brand": brand}  # Add the brand to the item dictionary

                    img = car.find("img")
                    if img and "srcset" in img.attrs:
                        item['Image'] = img.attrs["srcset"].split()[0]  # Take the first image link
                    else:
                        item['Image'] = 'N/A'  # Set default if not found

                    link = car.find("a")
                    if link and "href" in link.attrs:
                        item['Link'] = link.attrs["href"]
                    else:
                        item['Link'] = 'N/A'  # Set default if not found

                    price = car.find("div", class_="info-price")
                    if price:
                        item['Price'] = price.text[2:].strip()  # Strip whitespace
                    else:
                        item['Price'] = 'N/A'  # Set default if not found

                    condition = car.find("span", class_=["label listing-badge-style label-danger", "label listing-badge-style label-success", "label listing-badge-style label-warning"])
                    if condition:
                        item['Condition'] = condition.text.strip()
                    else:
                        item['Condition'] = 'Brand New Car'  # Set default if not found

                    # Extract additional details: mileage, transmission, body type, location
                    mileage_div = car.find("i", class_="icon-dashboard")
                    if mileage_div:
                        item['Mileage'] = mileage_div.find_next("span").text.strip()
                    else:
                        item['Mileage'] = 'Brand New Car'

                    engine_div = car.find("i", class_="icon-cogs")
                    if engine_div:
                        item['Engine'] = engine_div.find_next("span").text.strip()
                    else:
                        item['Engine'] = 'N/A'

                    transmission_div = car.find("i", class_="icon-wrench")
                    if transmission_div:
                        item['Transmission'] = transmission_div.find_next("span").text.strip()
                    else:
                        item['Transmission'] = 'N/A'

                    body_type_div = car.find("i", class_="icon-tags")
                    if body_type_div:
                        item['Body Type'] = body_type_div.find_next("span").text.strip()
                    else:
                        item['Body Type'] = 'N/A'

                    location_div = car.find("i", class_="icon-map-marker")
                    if location_div:
                        item['Location'] = location_div.find_next("span").text.strip()
                    else:
                        item['Location'] = 'N/A'

                    data.append(item)

        current_page += 1

    return data

# Main function to control scraping flow
def main():
    # List of car brands to scrape
    car_brands = ["Perodua", "Toyota", "Honda", "Proton", "Nissan", "BMW", "Mazda", "Mercedes-Benz", "Ford", "Audi", "Hyundai", "Kia", "Mitsubishi", "Volskwagen"]  

    # Scrape data for each brand and concatenate the results
    all_data = []
    for brand in car_brands:
        all_data.extend(scrape_brand(brand))

    # Create a DataFrame and save to Excel and CSV
    df = pd.DataFrame(all_data)
    df.to_excel("cars.xlsx", index=False)
    df.to_csv("cars.csv", index=False)

    print("Scraping complete. Data saved to cars.xlsx and cars.csv.")

if __name__ == "__main__":
    main()
