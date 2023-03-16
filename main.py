import argparse
import logging
import os
import time
from models import create_model, upload_image_samples, queue_training_job, \
    get_model_version, generate_image
from request import get_inference_job

# TODO: Make these CLI Arguments
API_KEY = f"ee774d48-ec8b-480a-9bbb-08591696d7a8"
IMAGES_PATH = f".\\images\\images.txt"
MODEL_TITLE = f"TestModel"
HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {API_KEY}"
}
GENERATE_PROMPT = f"A photo of @me with a tall black hat and sunglasses"

logger = logging.getLogger(__name__)


def main() -> None:
    """
    This function is the entry point for the application. It orchestrates the entire process.
    :param api_key: The API key required to make requests to the Tryleap API.
    :param images_path: The path to the file containing URLs of the images to be used as samples.
    :param model_title: The title of the model to be created.
    :return: None
    """
    logging.basicConfig(level=logging.INFO)

    # Load the list of images from the file
    # TODO: add error handling and check if images are .jpg
    logging.info('Opening Images')
    with open(IMAGES_PATH, 'r') as f:
        IMAGES = f.read().splitlines()
    logging.info(f"{len(IMAGES)} Images loaded")

    # Set the headers to include the API key

    # Create a new model
    # TODO: Check if model is already present
    logging.info('Creating model')
    model_id = create_model(MODEL_TITLE, HEADERS)
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
