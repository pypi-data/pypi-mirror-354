
# from dotenv import load_dotenv
import os
import json
import requests
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# load_dotenv()
# access_key = os.getenv("UNSPLASH_ACCESS_KEY")
query = "car"
from .decorators import execution_time
from PIL import Image


def get_next_filename(name, path=None):
    # Separate the base name and the extension
    new_name, extension = os.path.splitext(name)
    if not path:
        path = os.getcwd()  # Use current working directory if no path is provided
    
    # Initialize the full file path
    n = 1
    p = os.path.join(path, f"{new_name}{extension}")
    
    # Check for file existence and append a number if it already exists
    while os.path.exists(p):
        p = os.path.join(path, f"{new_name}({n}){extension}")
        n += 1
    
    return os.path.basename(p)

def download_image(query, access_key=None):
    # Ensure access_key is provided before proceeding
    if not access_key:
        logger.error("Access key is missing.")
        raise RuntimeError("You have to add the access key.")
    
    # Construct the Unsplash API URL
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={access_key}"
    
    # Fetch the random image data from Unsplash API
    try:
        logger.info("Fetching image data from Unsplash")
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        logger.error(f"Error fetching image data: {e}")
        return

    # Save the API response to a JSON file
    with open(f'{query}_response.json', "w") as f:
        json.dump(response.json(), f, indent=4)
    
    data = response.json()
    img_url = data['urls'].get("raw")
    description = data.get('description', query)
    
    if not img_url:
        logger.error("Image not url found")
        return

    # Create the directory for storing the images
    path = os.path.join("media", query)
    os.makedirs(path, exist_ok=True)  # Recursively create directories if they don't exist
    
    # Generate a unique filename
    title = get_next_filename(description if description else query + ".jpg", path)
    
    # Stream the image content (for handling large files efficiently)
    try:
        logger.info(f"Downloading image for query: {query}.")
        image_response = requests.get(img_url, stream=True)
        image_response.raise_for_status()  # Check for any image download issues
    except requests.RequestException as e:
        logger.error(f"Error downloading image: {e}")
        print(f"Error downloading image: {e}")
        return

    # Save the image to disk
    image_path = os.path.join(path, f"{title}.jpg")
    with open(image_path, "wb") as f:
        for chunk in image_response.iter_content(1024):  # Stream data in chunks
            f.write(chunk)
    
    logger.info(f"Image downloaded successfully to {image_path}!")


# I want to create image type converter. list image file types that can be converted in python

image_types = {
    "JPEG": [".jpg", ".jpeg"],
    "PNG": [".png"],
    "GIF": [".gif"],
    "BMP": [".bmp"],
    "TIFF": [".tiff", ".tif"],
    "WEBP": [".webp"]
}
def get_image_types():
    """
    Returns a dictionary of image types and their corresponding file extensions.

    Returns:
        dict: A dictionary where keys are image types and values are lists of file extensions.
    """
    return image_types

def get_image_extensions():
    """
    Returns a list of all image file extensions.
    
    Returns:
        list: A list of image file extensions.
    """
    return [ext for types in image_types.values() for ext in types]

def get_image_type(file_path):
    """
    Determines the image type based on the file extension.

    Args:
        file_path (str): The path to the image file.

    Returns:
        str: The image type (e.g., "JPEG", "PNG") or None if the type is unknown.
    """
    _, ext = os.path.splitext(file_path.lower())
    for image_type, extensions in image_types.items():
        if ext in extensions:
            return image_type
    return None

def convert_image(input_path, output_path, output_format):
    """
    Converts an image to a different format.

    Args:
        input_path (str): The path to the input image file.
        output_path (str): The path to the output image file.
        output_format (str): The desired output image format (e.g., "JPEG", "PNG").

    Returns:
        bool: True if the conversion was successful, False otherwise.
    """
    try:
        with Image.open(input_path) as img:
            img.convert("RGB").save(output_path, format=output_format)
        return True
    except Exception as e:
        logger.error(f"Error converting image: {e}")
        return False
    
def convert_image_type(input_path, output_format):
    """
    Converts an image to a different format and saves it with a new filename.

    Args:
        input_path (str): The path to the input image file.
        output_format (str): The desired output image format (e.g., "JPEG", "PNG").

    Returns:
        str: The path to the converted image file.
    """
    # Get the base name and extension of the input file
    base_name, _ = os.path.splitext(os.path.basename(input_path))
    
    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(input_path)
    
    # Generate a new filename with the desired format
    output_filename = f"{base_name}.{output_format.lower()}"
    output_path = os.path.join(output_dir, output_filename)
    
    # Convert the image
    if convert_image(input_path, output_path, output_format):
        return output_path
    else:
        return None
    
def convert_images_in_directory(directory, output_format):
    """
    Converts all images in a directory to a specified format.

    Args:
        directory (str): The path to the directory containing images.
        output_format (str): The desired output image format (e.g., "JPEG", "PNG").

    Returns:
        list: A list of paths to the converted image files.
    """
    converted_files = []
    
    # Get all files in the directory
    for filename in os.listdir(directory):
        if any(filename.lower().endswith(ext) for ext in get_image_extensions()):
            input_path = os.path.join(directory, filename)
            converted_file = convert_image_type(input_path, output_format)
            if converted_file:
                converted_files.append(converted_file)
    
    return converted_files

def convert_images_in_subdirectories(directory, output_format):
    """
    Converts all images in subdirectories to a specified format.

    Args:
        directory (str): The path to the directory containing images.
        output_format (str): The desired output image format (e.g., "JPEG", "PNG").

    Returns:
        list: A list of paths to the converted image files.
    """
    converted_files = []

    # Walk through all subdirectories
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if any(filename.lower().endswith(ext) for ext in get_image_extensions()):
                input_path = os.path.join(root, filename)
                converted_file = convert_image_type(input_path, output_format)
                if converted_file:
                    converted_files.append(converted_file)

    return converted_files
