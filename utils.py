def resize_image(image, max_width, max_height):
    aspect_ratio = float(image.size[1]) / float(image.size[0])
    new_width = max_width
    new_height = int(new_width * aspect_ratio)

    if new_height > max_height:
        new_height = max_height
        new_width = int(new_height / aspect_ratio)

    width_scale = float(new_width) / float(image.size[0])
    height_scale = float(new_height) / float(image.size[1])

    image.thumbnail((new_width, new_height))
    return image, width_scale, height_scale


def scale_bounding_box(bounding_boxes, width_scale, height_scale):
    for index, obj in enumerate(bounding_boxes["objects"]):
        bounding_boxes["objects"][index]["left"] *= width_scale
        bounding_boxes["objects"][index]["top"] *= height_scale
        bounding_boxes["objects"][index]["width"] *= width_scale
        bounding_boxes["objects"][index]["height"] *= height_scale
    return bounding_boxes


def save_current_state(file_name, bounding_boxes, bucket, client):
    obj = client.get_object(Bucket=bucket, Key=file_name)
    saved_data = json.loads(obj['Body'].read().decode('utf-8'))

    saved_data["user_reviewed"] = bounding_boxes.get("user_reviewed", 0)
    saved_data["missing_information"] = bounding_boxes.get("missing_information", False)
    saved_data["wrong_datapoint"] = bounding_boxes.get("wrong_datapoint", False)

    for idx, _ in enumerate(saved_data["objects"]):
        saved_data["objects"][idx]["result"] = bounding_boxes["objects"][idx].get("result", True)
        saved_data["objects"][idx]["first"] = bounding_boxes["objects"][idx].get("first", True)
        saved_data["objects"][idx]["last"] = bounding_boxes["objects"][idx].get("last", True)

    client.put_object(Bucket=bucket, Key=file_name, Body=json.dumps(saved_data, indent=2).encode('utf-8'))


def handle_wrong_datapoint(data):
    data["wrong_datapoint"] = True
    data["user_reviewed"] = 1
    data["missing_information"] = False
    for obj in data["objects"]:
        obj["result"] = False
    return data


def handle_missing_datapoint(data):
    data["missing_information"] = True
    data["user_reviewed"] = 1
    data["wrong_datapoint"] = False
    for obj in data["objects"]:
        obj["result"] = False
    return data


def handle_user_choice(data, canvas_bounding_boxes):
    any_dark_green_box = False
    for i, canvas_bounding_box in enumerate(canvas_bounding_boxes):
        ocr_bounding_box = data["objects"][i]
        if canvas_bounding_box["fill"] == "rgb(208, 240, 192, 0.2)":
            ocr_bounding_box["result"] = True
        elif canvas_bounding_box["fill"] == "rgb(208, 239, 192, 0.2)":
            ocr_bounding_box["result"] = True
            any_dark_green_box = True
        else:
            ocr_bounding_box["result"] = False

        if canvas_bounding_box["stroke"] == 'rgb(50,199,50)':
            ocr_bounding_box["first"] = True
            ocr_bounding_box["last"] = False
        elif canvas_bounding_box["stroke"] == "rgb(50,201,50)":
            ocr_bounding_box["last"] = True
            ocr_bounding_box["first"] = False
        elif canvas_bounding_box["stroke"] == "rgb(50,205,50)":
            ocr_bounding_box["first"] = True
            ocr_bounding_box["last"] = True
        else:
            ocr_bounding_box["first"] = False
            ocr_bounding_box["last"] = False

        ocr_bounding_box.update(canvas_bounding_box)
    if any_dark_green_box:
        data["user_reviewed"] = 1
        data["missing_information"] = False
        data["wrong_datapoint"] = False
    return any_dark_green_box, data
