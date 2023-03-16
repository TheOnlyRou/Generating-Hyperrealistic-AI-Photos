import json
import requests
import time

API_BASE_URL = f"https://api.tryleap.ai/api/v1/images/"


# TODO: Add logging & Error Handling
def create_model(title, headers):
    """
    Creates a new image model with the given title and subject keyword.

    Args:
        title (str): The title of the model.
        headers (dict): A dictionary containing the headers required to authenticate the API call.

    Returns:
        str: The ID of the newly created model.
    """
    url = "https://api.tryleap.ai/api/v1/images/models"

    payload = {
        "title": title,
        "subjectKeyword": "@me"
    }

    response = requests.post(url, json=payload, headers=headers)

    model_id = json.loads(response.text)["id"]
    return model_id


# TODO: Add logging & Error Handling
def upload_image_samples(model_id, images, headers):
    """
    Uploads a list of image URLs to the specified image model.

    Args:
        model_id (str): The ID of the image model to upload the images to.
        images (list): A list of image URLs to upload.
        headers (dict): A dictionary containing the headers required to authenticate the API call.
    """
    url = f"https://api.tryleap.ai/api/v1/images/models/{model_id}/samples/url"

    payload = {"images": images}
    response = requests.post(url, json=payload, headers=headers)
    print(f"UPLOAD RESPONSE:  {response}")


# TODO: Add logging & Error Handling
def queue_training_job(model_id, headers):
    """
    Queues a training job for the specified image model.

    Args:
        model_id (str): The ID of the image model to train.
        headers (dict): A dictionary containing the headers required to authenticate the API call.

    Returns:
        Tuple[str, str]: A tuple containing the version ID of the model and its current status.
    """
    url = f"https://api.tryleap.ai/api/v1/images/models/{model_id}/queue"
    response = requests.post(url, headers=headers)
    data = json.loads(response.text)

    version_id = data["id"]
    status = data["status"]

    return version_id, status


# TODO: Add logging & Error Handling
def get_model_version(model_id, version_id, headers):
    """
    Retrieves the status of a specific model version.

    Args:
        model_id (str): The ID of the image model.
        version_id (str): The ID of the model version to retrieve the status for.
        headers (dict): A dictionary containing the headers required to authenticate the API call.

    Returns:
        Tuple[str, str]: A tuple containing the version ID of the model and its current status.
    """
    url = f"https://api.tryleap.ai/api/v1/images/models/{model_id}/versions/{version_id}"
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    version_id = data["id"]
    status = data["status"]

    return version_id, status


# TODO: Add logging & Error Handling. Adjust for multiple number of images to be generated.
def generate_image(model_id, prompt, headers):
    """
    Generate a new image using the trained model.

    :param model_id: ID of the model to use
    :type model_id: str
    :param prompt: Prompt to generate the image from
    :type prompt: str
    :param headers: Headers to include in the API request
    :type headers: dict
    :return: Tuple of inference ID, status and image
    :rtype: Tuple[str, str, bytes]
    """
    url = f"https://api.tryleap.ai/api/v1/images/models/{model_id}/inferences"

    payload = {
        "prompt": prompt,
        "steps": 50,
        "width": 512,
        "height": 512,
        "numberOfImages": 1,
        "seed": 4523184
    }

    response = requests.post(url, json=payload, headers=headers)
    data = json.loads(response.text)

    inference_id = data["id"]
    status = data["status"]

    print(f"Inference ID: {inference_id}. Status: {status}")

    return inference_id, status
