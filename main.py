import argparse
import logging
import os
import time
from models import create_model, upload_image_samples, queue_training_job, \
    get_model_version, generate_image, get_models
from request import get_inference_job

# TODO: Make these CLI Arguments
API_KEY = f"0ccdfb4b-d9ac-4e3a-b4aa-6c679c666019"
IMAGES_PATH = f".\\images\\images.txt"
MODEL_TITLE = f"TestModel"
HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {API_KEY}"
}
GENERATE_PROMPT = f"A photo of @me working with a computer"

logger = logging.getLogger(__name__)


def main() -> None:
    """
    This function is the entry point for the application. It orchestrates the entire process.
    :param api_key: The API key required to make requests to the Tryleap API.
    :param images_path: The path to the file containing URLs of the images to be used as samples.
    :param model_title: The title of the model to be created.
    :return: None
    """
    # TODO: Split main() into more util & helper methods
    logging.basicConfig(level=logging.INFO)
    model_id = ""
    model_found = None

    # Load the list of images from the file
    # TODO: Upload all files found in a certain folder. Keep track of files uploaded to avoid duplicates
    # TODO: add error handling and check if images are .jpg
    logging.info('Opening Images')
    with open(IMAGES_PATH, 'r') as f:
        IMAGES = f.read().splitlines()
    logging.info(f"{len(IMAGES)} Images loaded")

    # Set the headers to include the API key

    # Create a new model
    trained_models = get_models(API_KEY)
    logging.info(f"Trained Models with same name: {trained_models}")
    if len(trained_models) > 0:
        for model in trained_models:
            if model["title"] == MODEL_TITLE:
                model_id = model["id"]
                model_found = True
                break
    if model_found:
        logging.info(f"Found Model with same title. Using that one instead.")
    else:
        logging.info('Creating model')
        model_id = create_model(MODEL_TITLE, HEADERS)

        # TODO: Make it so it's also possible to use this Stable Diffusion 3.5 model if you want to generate generic non-trained images
        # TODO: Or get another model from here https://docs.tryleap.ai/reference/pre-trained-models
        # model_id = f"ee88d150-4259-4b77-9d0f-090abe29f650"
        logging.info('Model loaded')

        # Upload the images to the model
        logging.info('Uploading sample images')
        upload_image_samples(model_id, IMAGES, HEADERS)
        logging.info('Uploaded sample images')

        # Train the model and wait for it to finish
        logging.info('Training the model using the images provided')
        version_id, status = queue_training_job(model_id, HEADERS)
        while status != "finished":
            time.sleep(10)
            version_id, status = get_model_version(model_id, version_id, HEADERS)
        logging.info('Model Trained')

    # Generate a new image using the trained model
    logging.info('Generating new images based on the trained model')
    inference_id, status = generate_image(
        model_id,
        prompt=GENERATE_PROMPT,
        headers=HEADERS
    )
    while status != "finished":
        time.sleep(10)
        inference_id, status, image = get_inference_job(model_id, inference_id, HEADERS)
    logging.info('Image generated. Printing Image')

    # TODO: Add functionality of printing several images as well as saving them locally.
    print(image)
    logging.info('Done.')


if __name__ == "__main__":
    main()
