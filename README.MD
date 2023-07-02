# PostImages Python Client
The PostImages Python Client is a Python library that provides a convenient way to interact with the PostImages image hosting service. It allows you to log in, manage galleries, and upload images to your PostImages account.

## Installation
To use the PostImages Python Client, you need to have Python installed on your system. You can install the required dependencies by running the following command:

```bash
pip install requests beautifulsoup4
```
## Usage
Here's an example of how to use the PostImages Python Client:

```python
from src.postimages.postimages import PostImages

# Initialize PostImages client
email = "your_email@example.com"
password = "your_password"
client = PostImages(email, password)

# Login to your PostImages account
client.login()

'''
The login function returns a dictionary with the session key in the following format:

{'SESSIONKEY': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}

you can pass that session key to the constructor of the PostImages instead of using the login
method to prevent getting blocked by postimages.org due to many login attempts.
'''

# Get a list of galleries
galleries = client.get_galleries()
for gallery in galleries:
    print("Gallery:", gallery['name'])
    print("URL:", gallery['gallery_url'])

# Set the working gallery
gallery_name = "your_gallery_name"
client.set_working_gallery(gallery_name)

# Upload an image
image_path = "path_to_your_image.jpg"
image_urls = client.upload_image(image_path)
if image_urls:
    print("Image URLs:")
    for url_type, url in image_urls.items():
        print(url_type, ":", url)
else:
    print("Image upload failed.")
```

Please note that you need to replace "your_email@example.com" and "your_password" with your actual email and password for your PostImages account. Additionally, provide the correct gallery name and image path in the code.

Dependencies
The PostImages Python Client relies on the following dependencies:

requests: A library for making HTTP requests
beautifulsoup4: A library for parsing HTML and XML

## Contributing
Contributions to the PostImages Python Client are welcome! If you find any issues or have suggestions for improvements, please create an issue or submit a pull request on the GitHub repository.

 * Create Gallery: Implement a method to create a new gallery on PostImages.org.
 * Delete Gallery: Develop a method to delete an existing gallery from PostImages.org.
 * Delete Image: Add a method to delete a specific image from a gallery.
 * Get Gallery Images: Implement a method to retrieve all images within a gallery.
 * Download Image: Develop a method to download an image from PostImages.org.

## Author

The PostImages Python Client is developed by [Ali Faleh](https://github.com/alifaleh).

## License
This project is licensed under the Apache License 2.0.

![Visitor Badge](https://visitor-badge.laobi.icu/badge?page_id=alifaleh.postimages.org)