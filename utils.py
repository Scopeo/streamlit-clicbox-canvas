import datetime
from PIL import Image, ImageDraw


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


def create_img(resized_images, widths, heights):

    max_width = int(max(widths))
    total_height = int(sum(heights))

    new_img = Image.new('RGB', (max_width, total_height))
    draw = ImageDraw.Draw(new_img)

    y_offset = 0
    for im in resized_images:
        new_img.paste(im, (0, y_offset))
        y_offset += im.size[1]
        shape = [(0, y_offset), (im.size[0], y_offset)]
        draw.line(shape, fill="black", width=5)

    return new_img


def scale_bounding_box(bounding_boxes, width_scale, height_scale, current_page, heights):
    scaled_boxes = []

    for index, obj in enumerate(bounding_boxes["objects"]):
        if obj["page"] == current_page:
            obj["left"] *= width_scale
            obj["top"] *= height_scale
            obj["width"] *= width_scale
            obj["height"] *= height_scale
            obj["top"] += sum(heights[0:-1])
            scaled_boxes.append(obj)

    return scaled_boxes


def handle_wrong_datapoint(data, user_name):
    data["wrong_datapoint"] = True
    data["user_reviewed"] = 1
    data["missing_information"] = False
    data["reviewer"] = user_name
    data["review_datetime"] = datetime.datetime.now().isoformat()
    for obj in data["objects"]:
        obj["fill"] = "rgb(0, 0, 0, 0)"
        obj["stroke"] = "rgb(0, 0, 0, 0)"
        obj["result"] = False
    return data


def handle_missing_datapoint(data, user_name):
    data["missing_information"] = True
    data["user_reviewed"] = 1
    data["wrong_datapoint"] = False
    data["reviewer"] = user_name
    data["review_datetime"] = datetime.datetime.now().isoformat()
    for obj in data["objects"]:
        obj["fill"] = "rgb(0, 0, 0, 0)"
        obj["stroke"] = "rgb(0, 0, 0, 0)"
        obj["result"] = False
    return data


def handle_user_choice(data, canvas_bounding_boxes, user_name):
    page_bounding_boxes = [obj for obj in data["objects"]]
    for i, canvas_bounding_box in enumerate(canvas_bounding_boxes):
        ocr_bounding_box = page_bounding_boxes[i]
        if canvas_bounding_box["fill"] != "rgb(0, 0, 0, 0)":
            ocr_bounding_box["result"] = True
            ocr_bounding_box["fill"] = canvas_bounding_box["fill"]
            ocr_bounding_box["stroke"] = canvas_bounding_box["stroke"]
            ocr_bounding_box["group_id"] = canvas_bounding_box["fill"]
        else:
            ocr_bounding_box["result"] = False

        ocr_bounding_box.update(canvas_bounding_box)

    data["user_reviewed"] = 1
    data["missing_information"] = False
    data["wrong_datapoint"] = False
    data["reviewer"] = user_name
    data["review_datetime"] = datetime.datetime.now().isoformat()

    return data
