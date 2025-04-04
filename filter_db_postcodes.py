# do you have a list of postcodes but need to filtered so you only have the delivery areas and delete the PO boxes and other post office crap?
# well look no furthur!
# this script will connect to a database, get a list of all postcodes, then search the auspost page for postcodes, check the category and delete everything unless its a delivery area AKA a real postcode

import pymysql, requests
from bs4 import BeautifulSoup

# Database connection details (modify these as needed)
db_config = {
    "host": "localhost",
    "user": "aaaaa",
    "password": "aaaaa",
    "database": "aaaaa",
}

conn = pymysql.connect(**db_config)
cursor = conn.cursor()


cursor.execute("SELECT DISTINCT(postcode) FROM postcodes")
postcodes = [row[0] for row in cursor.fetchall()]


for db_postcode in postcodes:
    print(f"Searching for {db_postcode}")
    url = f"https://auspost.com.au/postcode/{db_postcode}"

    # Send a GET request to the URL
    headers = {"User-Agent": "Mozilla/5.0"}  # Avoid getting blocked
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the <tbody> element containing the data
        tbody = soup.find("tbody")
        
        if tbody:
            # Iterate through each row in the table
            for tr in tbody.find_all("tr"):
                # Extract the columns
                columns = tr.find_all("td")
                if len(columns) >= 3:
                    postcode_text = columns[0].text.strip()  # First column: Postcode
                    suburb_state_text = columns[1].text.strip()   # Second column: Suburb
                    category_text = columns[2].text.strip() # Third column: Category

                    suburb, state = suburb_state_text.rsplit(", ", 1) if ", " in suburb_state_text else (suburb_state_text, "Unknown")
                    
                    if category_text != "Delivery Area":
                        print(f"DELETING: Postcode: {postcode_text}, Suburb: {suburb}, State: {state} Category: {category_text}")
                        cursor.execute("DELETE FROM postcodes WHERE postcode=%s AND suburb=%s AND state=%s", (postcode_text, suburb, state))
                        conn.commit()
                    else:
                        print(f"KEEPING: Postcode: {postcode_text}, Suburb: {suburb}, State: {state} Category: {category_text}")

        else:
            print(f"No postcode data found for {db_postcode}")
            cursor.execute("DELETE FROM postcodes WHERE postcode=%s", (db_postcode,))
            conn.commit()
            print(f"DELEING: {db_postcode}")


    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")



cursor.close()
conn.close()

