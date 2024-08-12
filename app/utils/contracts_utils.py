import json
import os
import os.path
from typing import List
import boto3
import os
import PyPDF2
import boto3
from dotenv import load_dotenv
from pdf2image import convert_from_path
from textractor.data.text_linearization_config import TextLinearizationConfig
from textractor.entities.document import Document
from app.services.S3_service import s3_client

load_dotenv()

aws_region = os.getenv('AWS_REGION', 'us-east-1')
session = boto3.Session(aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
                        region_name=aws_region)

textract_client = session.client(service_name='textract', region_name=aws_region)

print('Hello')

config = TextLinearizationConfig(
    selection_element_selected="[X]",
    selection_element_not_selected="[]",
    signature_token="[SIGNATURE]",
    hide_figure_layout=True,
    hide_header_layout=True,
    hide_page_num_layout=True,
    hide_footer_layout=True,
    title_prefix="# ",
    section_header_prefix="## "

)


def get_page_number(image_name):
    return int(image_name.split("-")[-1].split(".")[0])


def rename_pages(
        first_page: int, last_page: int, page_image_paths: List[str]
):
    batch = []

    for image in page_image_paths:
        page_number = get_page_number(image)
        if first_page <= page_number <= last_page:
            new_image_name = os.path.join(
                os.path.dirname(image), f"page-{page_number}.jpg"
            )
            os.rename(image, new_image_name)
            batch.append(new_image_name)

    return batch


def pdf_to_images(pdf_path, output_folder):
    """

    :rtype: object
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_pages = 0
    # Read the PDF file using PyPDF2
    with open(pdf_path, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        total_pages = len(pdf.pages)
    print(f'Total pages: {total_pages}')

    # Convert each page to an image

    page_image_paths = convert_from_path(
        pdf_path,
        output_folder=output_folder,
        paths_only=True,
        first_page=1,
        last_page=total_pages,
        output_file="page",
        fmt="jpeg",
        use_pdftocairo=True
    )

    # print(f'Page image paths: {page_image_paths}')

    renamed_page_image_paths = rename_pages(first_page=1, last_page=total_pages, page_image_paths=page_image_paths)

    # print(f'Renamed Page image paths: {renamed_page_image_paths}')

    return renamed_page_image_paths


def append_page_number(page_text: str = None, page_number: int = None):
    """

    :param page_text:
    :type page_number: object
    """
    document_str = '\n' + f'---start of  page {page_number} --- ''\n' + page_text + '\n' + f'----end of  page {page_number} ----''\n'
    return document_str


def get_page_number(image_path: str):
    from pathlib import Path
    return int(Path(image_path).parts[-1].split('.')[0].split('-')[-1])


def run_textract_save_responses(page_image_paths: List = [], json_output_directory: str = None,
                                text_output_directory: str = None):
    if not os.path.exists(json_output_directory):
        os.makedirs(json_output_directory)
        print('Created json output directory: {}'.format(json_output_directory))

    if not os.path.exists(text_output_directory):
        os.makedirs(text_output_directory)
        print('Created text output directory: {}'.format(text_output_directory))

    for page_image_path in page_image_paths:
        page_number = get_page_number(page_image_path)
        json_file_path = os.path.join(json_output_directory, f'page-{page_number}_textract.json')
        text_file_path = os.path.join(text_output_directory, f'page-{page_number}.txt')

        with open(page_image_path, 'rb') as img_file:
            # Read bytes
            img_bytes = img_file.read()
            print(f'Running AWS Textract for {page_image_path} ')
            response = textract_client.analyze_document(Document={'Bytes': img_bytes},
                                                        FeatureTypes=["TABLES", "FORMS", "SIGNATURES", "LAYOUT"])

        # Write the JSON response to the file
        with open(json_file_path, 'w') as file:
            print(f'Writing AWS Textract json response for {page_number} on {json_file_path} ')
            json.dump(response, file, indent=4)  # `indent=4` is optional, but it makes the JSON more readable


        with open(json_file_path) as f:
            response = json.load(f)
            document = Document.open(response)
            text = document.get_text(config=config)

            appended_text = append_page_number(page_text=text, page_number=page_number)

        with open(text_file_path, 'w') as f:
            print(f'Writing AWS Textract text response for {page_number} on {text_file_path} ')
            f.write(appended_text)


def upload_folder_to_s3(bucket_name, local_folder, s3_folder):
    """
    Uploads a local folder to an S3 bucket.

    :param bucket_name: Name of the S3 bucket
    :param local_folder: Path to the local folder to upload
    :param s3_folder: Path to the folder in S3 where the files will be uploaded
    """

    for root, dirs, files in os.walk(local_folder):
        for dir in dirs:
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_file_path, local_folder)
                s3_file_path = os.path.join(s3_folder, relative_path).replace("\\", "/")

            print(f'Uploading {local_file_path} to s3://{bucket_name}/{s3_file_path}')
            s3_client.upload_file(local_file_path, bucket_name, s3_file_path)
#

def upload_folder_to_s3_cmd(bucket_name, local_folder, s3_folder):
    import subprocess
    # local_folder = "/path/to/your/local/folder"
    s3_bucket = f"s3://{bucket_name}/output/"

    command = ["aws", "s3", "sync", local_folder, s3_bucket]
    os.environ['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY')
    os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_KEY')

    try:
        subprocess.run(command)
        print("Files copied to S3 successfully!")
    except subprocess.CalledProcessError as e:
        print("Error:", e)


# Usage example
bucket_name = 'your-bucket-name'
local_folder = 'path/to/your/local/folder'
s3_folder = 'your/s3/folder'

upload_folder_to_s3(bucket_name, local_folder, s3_folder)
