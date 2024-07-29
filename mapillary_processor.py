# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# python3 mapillary_processor.py

import os
import requests
from PIL import Image
import piexif

token = '<your-token-goes-here>'
folder_with_images_to_process = 'path/to/files/goes/here'
url = 'https://graph.mapillary.com/'

def get_image_geometry(image_id):
	"""
	gets geometry (lat long) of an image from the mapillary API

	params:
	image_id (str): mapillary image ID

	returns:
	tuple: tuple containing lat and long, or None if the request fails
	"""	
	
	url = f"{url}/{image_id}"
	params = {
		'fields': 'geometry',
		'access_token': token
	}
	response = requests.get(url, params=params)
	if response.status_code == 200:
		data = response.json()
		coordinates = data['geometry']['coordinates']
		return coordinates[1], coordinates[0]  # latitude, longitude
	else:
		print(f"Couldn't find {image_id}: {response.status_code}")
		return None
	
def convert_to_rational(number):
	"""
	convert floating point number to a rational number

	params:
	number (float): floating point number

	returns:
	tuple: tuple representing the rational number
	"""
	
	f = round(number * 1000000)
	return (f, 1000000)

def convert_to_degrees(value):
	"""
	create an IFD for EXIF data

	params:
	lat (float): latitude
	lon (float): longitude

	returns:
	dict: dictionary representing the GPS IFD
	"""
	
	deg = int(value)
	min = int((value - deg) * 60)
	sec = (value - deg - min / 60) * 3600
	return (convert_to_rational(deg), convert_to_rational(min), convert_to_rational(sec))

def set_gps_location(lat, lon):
	"""
	save GPS location data to EXIF data

	params:
	image_path (str): path to the image file.
	lat (float): latitude
	lon (float): longitude

	returns:
	None
	"""
	
	gps_ifd = {
		piexif.GPSIFD.GPSLatitudeRef: 'N' if lat >= 0 else 'S',
		piexif.GPSIFD.GPSLatitude: convert_to_degrees(abs(lat)),
		piexif.GPSIFD.GPSLongitudeRef: 'E' if lon >= 0 else 'W',
		piexif.GPSIFD.GPSLongitude: convert_to_degrees(abs(lon)),
	}
	return gps_ifd

def save_exif_data(image_path, lat, lon):
	"""
	process images in a folder to add GPS location data to their EXIF data

	params:
	folder_path (str): path to the folder containing the images

	returns:
	None
	"""
	
	image = Image.open(image_path)
	exif_dict = None
	if "exif" in image.info:
		exif_dict = piexif.load(image.info["exif"])
	else:
		exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
		
	exif_dict["GPS"] = set_gps_location(lat, lon)
	exif_bytes = piexif.dump(exif_dict)
	image.save(image_path, "jpeg", exif=exif_bytes)
	
def process_images(folder_path):
	"""
	process images in a folder to add GPS location data to their EXIF data

	params:
	folder_path (str): path to the folder containing the images

	returns:
	None
	"""
	
	for filename in os.listdir(folder_path):
		if filename.lower().endswith(('.jpg', '.jpeg')): 
			image_id = os.path.splitext(filename)[0]
			coordinates = get_image_geometry(image_id)
			if coordinates:
				save_exif_data(os.path.join(folder_path, filename), *coordinates)
				
if __name__ == "__main__":
	folder_path = folder_with_images_to_process 
	process_images(folder_path)