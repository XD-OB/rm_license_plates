# License plate hidder

A Website/API built using **Flask** that detect and hide / replace the vehicule license plate from the image and hide it using **openCV**, if the user choose to replace the old plate the new one is traited to fill the old place.

![Screen Shot 1](/ressources/header.JPG)

- You can change the new used plate in: `./static/plate.png`
- Some images to test: `./images`
- Accept only `JPG` or `JPEG`
- The program is on the early stage, some problems can accure in the tests !

## Steps used in the image process:
The steps used to solve the problem are in the jupyter notebook:
- `./ressources/notebook.ipynb`

## Dependencies:
- openCV
- Flask
- Pillow
- imutils

You can install all the dependencies with the command:
- `pip install -r requirements.txt` 

## Usage:
### Launch the server:
- Run the cmd: `python app.py`
- Go to: `http://localhost:5000`

![Screen Shot 1](/ressources/launch.JPG)

### API:
The API have a visual interface so you can use the website or postman to send the request

original image -----[ API ]-----> new image (jpg)

In error case (No image sent | back format of the file) --------> JSON contain error detail 

- The files are stored in: `./static/results`

#### Hide the plate:
- `/api/hide`
#### Replace the plate:
- `/api/replace`

### Additional feature
Additional to the API urls there is a field to send the image and show both the result of **hide** and **replace** with the original image
- `/result`

![Screen Shot 1](/ressources/result.JPG)

## obelouch 1337

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
