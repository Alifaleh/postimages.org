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