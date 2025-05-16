from serpapi import GoogleSearch
import requests, lxml, json
import csv
params = {
    "q": "flowers",  # search query
    "tbm": "shop",  # shop results
    "location": "Dallas",  # location from where search comes from
    "hl": "en",  # language of the search
    "gl": "us",  # country of the search
    "api_key": "<<SERPAPI KEY>>"  # https://serpapi.com/manage-api-key
}

# https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

search = GoogleSearch(params)  # where data extraction happens on the SerpApi backend
results = search.get_dict()  # JSON -> Python dict
google_shopping_data = results["shopping_results"]

print(json.dumps(google_shopping_data, indent=2, ensure_ascii=False))


with open('maps-results.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write the headers
    csv_writer.writerow(["Title", "URL Link", "Price", "Delivery",  "Rating","Review"])

    # Write the data
    for result in google_shopping_data:
        # csv_writer.writerow([result["title"], result["link"]])
        csv_writer.writerow([result["title"], result["product_link"], result["extracted_price"],result["delivery"],result["store_rating"] if "store_rating" in result else "",result["store_reviews"] if "store_reviews" in result else ""])


def download_google_shopping_images():
    for index, result in enumerate(results["shopping_results"], start=1):
        image = requests.get(result['thumbnail'], headers=headers, timeout=30, stream=True)

        if image.status_code == 200:
            with open(f"images/image_{index}.jpeg", 'wb') as file:
                file.write(image.content)


def serpapi_get_google_shopping_data():
    google_shopping_data = results["shopping_results"]

    # download_google_shopping_images()

    print(json.dumps(google_shopping_data, indent=2, ensure_ascii=False))