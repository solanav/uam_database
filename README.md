# uam_database
UAM (madrid) moodle data scrapper. This tool allows you to download images from all the users that have uploaded one to moodle.

# Explanation of the tools
- native_interface.py: uses tk to create a native interface for the database and search users by name or surname.
- web_interface.py: uses a simple http server to create a bootstrap front using the same user data. This is served on http://localhost:8080
- users.json: json file with the name and surname of all the scrapped users and the link to their image.
- update_images.py: single-threaded downloader of the images of the users. Requires the file users.json. This script will save the images inside a folder called images.

