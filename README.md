# Generating Hyperrealistic AI Photos

This aim of this project is to generate unlimited hyperrealistic photos using AI, powered by [Leap AI](tryleap.ai). This project uses Python script uses the TryLeap API to train a machine learning model on a set of images, and generate a new image using the trained model.

This script uses the [Tryleap API](https://docs.tryleap.ai/) to generate images based on a set of sample images. The script creates a new model or searches for a model with the same name as the one provided, uploads the sample images, trains the model (if new model), and generates a new image using the trained model.



## How to use this project:

## How to Use

To use this script, you will need to have an API key from the Tryleap API. You can sign up for a free account [here](https://app.tryleap.ai/auth/signup).

1. Clone this repository or download the `main.py` file.
2. Install the required Python libraries by running `pip install -r requirements.txt` in your terminal.
3. Open `main.py` in your text editor of choice.
4. Replace the following variables with your own values:
   - `API_KEY`: Your Tryleap API key.
   - `IMAGES_PATH`: The path to the file containing URLs of the images to be used as samples.
   - `MODEL_TITLE`: The title of the model to be created.
   - `GENERATE_PROMPT`: The prompt to use when generating a new image.
5. Save the changes to `main.py`.
6. Run `python main.py` in your terminal to start the script.
7. The script will create a new model, upload the sample images, train the model, and generate a new image using the trained model. The image will be printed to the console.

## What to Edit

You will need to edit the following variables in `main.py` to use the script with your own data:

- `API_KEY`: Replace `API_KEY = f"*************************"` with your own Tryleap API key.
- `IMAGES_PATH`: Replace `IMAGES_PATH = f".\\images\\images.txt"` with the path to the file containing URLs of the images to be used as samples.
- `MODEL_TITLE`: Replace `MODEL_TITLE = f"********"` with the title of the model you want to create.
- `GENERATE_PROMPT`: Replace `GENERATE_PROMPT = f"A photo of @me working with a computer"` with the prompt you want to use when generating a new image.

Feel free to modify the code to suit your needs. If you have any questions or issues, please feel free to contact me

## TODO

1. Clean main.py and split it into utils & helper files

2. Make it so the code can upload files in a folder instead of providing URLs that get reuploaded anyway

3. Add try, catch statements for HTTP requests

4. Add error handling for image upload and check that all images are .jpg

5. Make it so it's possible to use other pretrained models like StableDiffusion 3.5

6. Make it so it's possible to print several images

7. Make it so it's possible to save the images at a local directory

8. Clean and organize logging statements
