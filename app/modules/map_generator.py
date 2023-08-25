import pgeocode
import csv
import os
import logging

def get_coordinates_by_postcode(country_code, postcode):
    geolocator = pgeocode.Nominatim(country_code)
    location = geolocator.query_postal_code(postcode)
    return location.latitude, location.longitude

def generate_map_html():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Paths for the locations.csv and template.html files
    csv_path = os.path.join(script_dir, '../data/locations.csv')
    template_path = os.path.join(script_dir, '../template.html')

    # Initialize the data list
    data = []

    # Read locations from CSV file
    if os.path.exists(csv_path):
        logging.debug(f"Reading locations from {csv_path}")
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            data.extend([(row['country'], row['postcode'], row['label']) for row in reader])
        logging.debug(f"Read {len(data)} locations from {csv_path}")

    locations = [
        (get_coordinates_by_postcode(country, postcode), label)
        for country, postcode, label in data
    ]

    # Generate markers
    markers = ""
    for (lat, lon), label in locations:
        markers += f"L.marker([{lat}, {lon}]).addTo(map).bindPopup('{label}').openPopup();\n"

    # Load and format the HTML template
    with open(template_path, 'r') as file:
        html_template = file.read()
        html_code = html_template.replace('###markers###', markers)

    # Return the generated HTML code
    return html_code
