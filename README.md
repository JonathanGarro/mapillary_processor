# Mapillary Image Processor

A python script that processes images in a folder to add GPS location data to their EXIF metadata by calling the Mapillary API. Note that this requires a Mapillary API token.

## Setup

1. Create a virtual environment:
	```bash
	python3 -m venv venv
	```

2. Activate the virtual environment:
	```bash
	source venv/bin/activate
	```

3. Install the required packages:
	```bash
	pip install -r requirements.txt
	```

4. Run the image processing script:
	```bash
	python3 mapillary_processor.py
	```

## Configuration

Before running the script, there are a couple variables you need to update in order for the script to run:

- Replace `<your-token-goes-here>` with your Mapillary API token, and;
- Set the `folder_with_images_to_process` variable to the path of the folder containing the images you want to process.

## Script Details

The script performs the following tasks:

1. **Get Image Geometry**:
	- The `get_image_geometry(image_id)` function retrieves the latitude and longitude of an image from the Mapillary API.

2. **Convert to Rational**:
	- The `convert_to_rational(number)` function converts a floating point number to a rational number.

3. **Convert to Degrees**:
	- The `convert_to_degrees(value)` function creates an IFD for EXIF data.

4. **Set GPS Location**:
	- The `set_gps_location(lat, lon)` function saves GPS location data to EXIF data.

5. **Save EXIF Data**:
	- The `save_exif_data(image_path, lat, lon)` function processes images to add GPS location data to their EXIF data.

6. **Process Images**:
	- The `process_images(folder_path)` function processes images in a folder to add GPS location data to their EXIF data.

## Example

To run the script, follow these steps:

1. Ensure you have set your Mapillary API token and the folder path in the script.

2. Run the script:
	```bash
	python3 mapillary_processor.py
	```

The script will process all `.jpg` and `.jpeg` images in the specified folder and add GPS location data to their EXIF metadata.

## Dependencies

The script requires the following Python packages:
- `requests`
- `Pillow`
- `piexif`