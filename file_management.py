from PIL import Image
from abc import ABC, abstractmethod
import json
import os
import boto3
import io
from pdf2image import convert_from_bytes, convert_from_path
import shutil


class FileManagement(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_image_file_name(self, file_path):
        pass

    @abstractmethod
    def move_files(self, source_key, destination_key):
        pass

    @abstractmethod
    def get_label_folder(self):
        pass

    @abstractmethod
    def list_files_in_folder(self, folder_path):
        pass

    @abstractmethod
    def create_folder(self, folder_path):
        pass

    @abstractmethod
    def read_file(self, file_path):
        pass

    @abstractmethod
    def read_document(self, file_path):
        pass

    @abstractmethod
    def save_current_state(self, file_name, bounding_boxes, label_folder_path):
        pass


class AWSFileManagement(FileManagement):
    def __init__(self, aws_bucket_name, OCR_results_path, images_path, output_path):
        super().__init__()
        self.aws_bucket_name = aws_bucket_name
        self.s3 = boto3.client("s3")
        self.OCR_results_path = OCR_results_path
        self.images_path = images_path
        self.output_path = output_path

    def move_files(self, source_key, destination_key):
        print(f"Moving file from {source_key} to {destination_key}")
        self.s3.copy_object(Bucket=self.aws_bucket_name, CopySource={'Bucket': self.aws_bucket_name, 'Key': source_key}, Key=destination_key)
        self.s3.delete_object(Bucket=self.aws_bucket_name, Key=source_key)

    def get_image_file_name(self, json_file_name):
        s3 = boto3.resource('s3')
        bucket_resource = s3.Bucket(self.aws_bucket_name)
        for obj in bucket_resource.objects.filter(Prefix=self.images_path):
            image_file_name = os.path.basename(obj.key)
            if image_file_name.split(".")[0] == json_file_name[2:-5]:
                return image_file_name

    def get_label_folder(self):
        result = self.s3.list_objects(Bucket=self.aws_bucket_name, Prefix=self.OCR_results_path, Delimiter='/')
        list_folders = []
        for o in result.get('CommonPrefixes'):
            list_folders.append(os.path.basename(o.get('Prefix').strip('/')))
        return list_folders

    def list_files_in_folder(self, folder_prefix):
        s3 = boto3.resource('s3')
        bucket_resource = s3.Bucket(self.aws_bucket_name)

        files = []
        for obj in bucket_resource.objects.filter(Prefix=folder_prefix):
            if obj.key != folder_prefix:
                files.append(os.path.basename(obj.key))

        return files

    def create_folder(self, folder_path):
        if not folder_path.endswith('/'):
            folder_path += '/'

        self.s3.put_object(Bucket=self.aws_bucket_name, Key=folder_path)

    def read_file(self, file_key):
        obj = self.s3.get_object(Bucket=self.aws_bucket_name, Key=file_key)
        content = obj['Body'].read().decode('utf-8')
        json_content = json.loads(content)
        return json_content

    def read_document(self, file_key):
        obj = self.s3.get_object(Bucket=self.aws_bucket_name, Key=os.path.join(self.images_path, file_key))
        file_data = obj['Body'].read()
        file_extension = os.path.splitext(file_key)[-1].lower()

        if file_extension in ['.jpg', '.jpeg', '.png', '.heic', '.bmp', '.gif', '.tiff', '.tif', '.webp', '.heif']:
            image = Image.open(io.BytesIO(file_data))
        elif file_extension == '.pdf':
            image = convert_from_bytes(file_data)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

        return image

    def save_current_state(self, file_name, bounding_boxes, label_folder_path):
        obj = self.s3.get_object(Bucket=self.aws_bucket_name, Key=os.path.join(label_folder_path, file_name))
        saved_data = json.loads(obj['Body'].read().decode('utf-8'))

        saved_data["user_reviewed"] = bounding_boxes.get("user_reviewed", 0)
        saved_data["missing_information"] = bounding_boxes.get("missing_information", False)
        saved_data["wrong_datapoint"] = bounding_boxes.get("wrong_datapoint", False)

        for idx, _ in enumerate(saved_data["objects"]):
            saved_data["objects"][idx]["result"] = bounding_boxes["objects"][idx].get("result", True)
            saved_data["objects"][idx]["first"] = bounding_boxes["objects"][idx].get("first", True)
            saved_data["objects"][idx]["last"] = bounding_boxes["objects"][idx].get("last", True)

        self.s3.put_object(Bucket=self.aws_bucket_name, Key=os.path.join(label_folder_path, file_name), Body=json.dumps(saved_data, indent=2).encode('utf-8'))


class LocalFileManagement(FileManagement):
    def __init__(self, OCR_results_path, images_path, output_path):
        super().__init__()
        self.OCR_results_path = OCR_results_path
        self.images_path = images_path
        self.output_path = output_path

    def move_files(self, source_key, destination_key):
        shutil.move(source_key, destination_key)

    def get_image_file_name(self, json_file_name):
        for image_file_name in os.listdir(self.images_path):
            if os.path.splitext(image_file_name)[0] == json_file_name[:-5]:
                return image_file_name

    def get_label_folder(self):
        return os.listdir(self.OCR_results_path)

    def list_files_in_folder(self, folder_path):
        return os.listdir(folder_path)

    def create_folder(self, folder_path):
        return os.makedirs(folder_path, exist_ok=True)

    def read_file(self, file_path):
        with open(file_path, "r") as file:
            bounding_boxes = json.load(file)
        return bounding_boxes

    def read_document(self, file_name):
        file_extension = os.path.splitext(file_name)[-1].lower()
        if file_extension in ['.jpg', '.jpeg', '.png', '.heic', '.bmp', '.gif', '.tiff', '.tif', '.webp', '.heif']:
            image = Image.open(os.path.join(self.images_path, file_name))
        elif file_extension == '.pdf':
            image = convert_from_path(os.path.join(self.images_path, file_name))
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        return image

    def save_current_state(self, file_name, bounding_boxes, label_folder_path):

        with open(os.path.join(label_folder_path, file_name), "r") as json_file:
            saved_data = json.load(json_file)
            saved_data["user_reviewed"] = bounding_boxes.get("user_reviewed", 0)
            saved_data["missing_information"] = bounding_boxes.get("missing_information", False)
            saved_data["wrong_datapoint"] = bounding_boxes.get("wrong_datapoint", False)

        for idx, _ in enumerate(saved_data["objects"]):
            saved_data["objects"][idx]["result"] = bounding_boxes["objects"][idx].get("result", True)
            saved_data["objects"][idx]["first"] = bounding_boxes["objects"][idx].get("first", True)
            saved_data["objects"][idx]["last"] = bounding_boxes["objects"][idx].get("last", True)

        with open(os.path.join(label_folder_path, file_name), "w") as json_file:
            json.dump(saved_data, json_file, indent=2)

