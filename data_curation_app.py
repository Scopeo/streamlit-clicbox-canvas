import streamlit as st
from streamlit_drawable_canvas import st_canvas
import os
from utils import resize_image, scale_bounding_box, handle_wrong_datapoint, handle_missing_datapoint, handle_user_choice
import hosting_config


def next_page():
    if len(st.session_state["OCR_output_files"]) > 0:
        current_file = st.session_state["OCR_output_files"].pop(0)
        st.session_state["curation_output_files"].append(current_file)
        hosting_config.file_manager.move_files(
            input_path=st.session_state["label_folder_path"],
            output_path=st.session_state["output_folder_path"],
            file_name=current_file
        )
        st.session_state["previous_clicked"] = False
    st.experimental_rerun()


def previous_page():
    current_file = st.session_state["curation_output_files"].pop()
    st.session_state["OCR_output_files"].insert(0, current_file)
    hosting_config.file_manager.move_files(
        input_path=st.session_state["output_folder_path"],
        output_path=st.session_state["label_folder_path"],
        file_name=current_file
    )
    st.session_state["previous_clicked"] = True
    st.experimental_rerun()

@st.cache_data()
def handle_image_and_bounding_box(OCR_results_file, bounding_boxes):
    image_file_name = hosting_config.file_manager.get_image_file_name(OCR_results_file)

def handle_image_and_bounding_box(OCR_results_file, images_path, bounding_boxes):
    image_file_name = get_image_file_name(OCR_results_file.split("/")[-1], images_path, bucket, client)
    if image_file_name is None:
        next_page()
    images = hosting_config.file_manager.read_document(image_file_name)
    image = read_document(bucket, images_path+image_file_name, client)
    image, width_scale, height_scale = resize_image(image, 800, 800)

    bounding_boxes = scale_bounding_box(bounding_boxes, width_scale, height_scale)
    return image, image_file_name, bounding_boxes


def add_sidebar_empty_space(n):
    for _ in range(n):
        st.sidebar.markdown("<br>", unsafe_allow_html=True)


if "selected_label" not in st.session_state:
    st.session_state["selected_label"] = ""

if "initialized" not in st.session_state:
    st.session_state["initialized"] = False

if "previous_clicked" not in st.session_state:
    st.session_state["previous_clicked"] = False

if "output_folder_path" not in st.session_state:
    st.session_state["output_folder_path"] = hosting_config.CONFIG["output_path"]

if "curation_output_files" not in st.session_state:
    st.session_state["curation_output_files"] = list()

if "refresh_counter" not in st.session_state:
    st.session_state["refresh_counter"] = 0

if not st.session_state["initialized"]:
if "initialized" not in st.session_state or not st.session_state["initialized"]:
    st.markdown(
        "<h1 style='text-align: center;'>Let's start</h1>",
        unsafe_allow_html=True
    )

    labels = hosting_config.file_manager.get_label_folder()
    label = st.selectbox("Select the Label:", labels)
    if st.session_state["selected_label"] != label:
        st.session_state["selected_label"] = label
        st.session_state["label_folder_path"] = os.path.join(hosting_config.CONFIG["OCR_results_path"], label)
        list_files = [file for file in hosting_config.file_manager.list_files_in_folder(st.session_state["label_folder_path"]) if file.endswith(".json")]
        list_files.sort()
        st.session_state["OCR_output_files"] = list_files
        st.session_state["output_folder_path"] = os.path.join(hosting_config.CONFIG['output_path'], label)
        hosting_config.file_manager.create_folder(st.session_state["output_folder_path"])
        st.session_state["curation_output_files"] = [file for file in hosting_config.file_manager.list_files_in_folder(st.session_state["output_folder_path"]) if file.endswith(".json")]

    col3, col4 = st.columns([8, 1])
    if col4.button("Next"):
        st.session_state["initialized"] = True
        st.experimental_rerun()

elif len(st.session_state["OCR_output_files"]) == 0:
    st.markdown("<h1 style='text-align: center;'>You're done!</h1>", unsafe_allow_html=True)

elif "label_folder_path" in st.session_state:
    current_file = st.session_state["OCR_output_files"][0]
    bounding_boxes = hosting_config.file_manager.read_file(os.path.join(st.session_state["label_folder_path"], current_file))
    if len(bounding_boxes["objects"]) > 0 and bounding_boxes["user_reviewed"] == 1 \
            and not st.session_state["previous_clicked"]:
        next_page()

    st.set_page_config(layout="wide")
    # show sidebar
    # add default width for sidebar
    st.markdown('''
            <style>
                    [data-testid="stSidebar"]{
                        min-width: 30%;
                        max-width: 30%
                    }
            </style>
            ''', unsafe_allow_html=True)

    # remove whitespaces
    st.markdown("""
            <style>
                   .block-container {
                        padding-top: 1rem;
                    }

            </style>
            """, unsafe_allow_html=True)

    st.markdown("""
            <style>
                   .css-1544g2n {
                        padding-top: 2rem;
                    }

            </style>
            """, unsafe_allow_html=True)

    # add company logo
    image_url = "https://scopeo.ai/wp-content/uploads/2020/11/logo_1024_512.png"
    st.markdown('''
            <style>
                    .disabled-click {
                        pointer-events: none;
                    }
            </style>
            ''', unsafe_allow_html=True)
    st.sidebar.markdown(
        f'<img src="{image_url}" class="disabled-click" width="100">', unsafe_allow_html=True
    )

    st.sidebar.markdown(
        """<h1 style='text-align: center; '>Invoice Data Collection Application</h1>""",
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        f"<h4 style='text-align: center;'> Files done : {len(st.session_state.get('curation_output_files', []))}, "
        f"files left : {len(st.session_state.get('OCR_output_files', []))}</h4>",
        unsafe_allow_html=True
    )

    add_sidebar_empty_space(1)

    st.sidebar.markdown(f"<h5 style='text-align:'>Selected Label: {st.session_state['selected_label']}</h5>",
                        unsafe_allow_html=True)

    image, image_file_name, bounding_boxes = handle_image_and_bounding_box(current_file, images_path, bounding_boxes)

    col1, col2 = st.sidebar.columns([2, 5])
    if col1.button("Refresh image"):
        st.session_state["refresh_counter"] += 1

    add_sidebar_empty_space(5)
    col3, col4 = st.sidebar.columns([2, 5])

    if col4.button("Wrong data point"):
        hosting_config.file_manager.save_current_state(current_file, handle_wrong_datapoint(bounding_boxes), st.session_state["label_folder_path"])
        next_page()

    if col4.button("Missing information"):
        hosting_config.file_manager.save_current_state(current_file, handle_missing_datapoint(bounding_boxes), st.session_state["label_folder_path"])
        next_page()

    add_sidebar_empty_space(5)
    col5, col6 = st.sidebar.columns([5, 1])
    if len(st.session_state.get("curation_output_files", [])) > 0:
        if col5.button("Previous"):
            previous_page()
    if col6.button("Next"):
        next_page()

    #show image part
    canvas_result = st_canvas(
        background_image=image,
        display_toolbar=False,
        update_streamlit=True,
        height=image.size[1],
        width=image.size[0],
        drawing_mode="transform",
        key=f"{image_file_name}_{st.session_state['refresh_counter']}",
        initial_drawing=bounding_boxes,
    )
                hosting_config.file_manager.save_current_state(current_file, bounding_boxes, st.session_state["label_folder_path"])
    st.write(image_file_name)
    if canvas_result.json_data is not None:
        any_dark_green_box, bounding_boxes = handle_user_choice(bounding_boxes, canvas_result.json_data["objects"])
        if any_dark_green_box:
            save_current_state(current_file, bounding_boxes, bucket, client)
            next_page()
