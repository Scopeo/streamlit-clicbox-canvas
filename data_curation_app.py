import streamlit as st
from streamlit_drawable_canvas import st_canvas
import os
from utils import resize_image, scale_bounding_box, handle_wrong_datapoint, handle_missing_datapoint, handle_user_choice, create_img
import hosting_config
from streamlit_cognito_auth import CognitoAuthenticator
from dotenv import load_dotenv
# st.set_page_config(layout="wide")


# authentication of user
load_dotenv()

pool_id = os.environ.get('pool_id')
app_client_id = os.environ.get('app_client_id')
app_client_secret = os.environ.get('app_client_secret')

authenticator = CognitoAuthenticator(
    pool_id=pool_id,
    app_client_id=app_client_id,
    app_client_secret=app_client_secret,
)

is_logged_in = authenticator.login()
if not is_logged_in:
    st.stop()


def logout():
    authenticator.logout()


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
with st.sidebar:
    st.text(f"Welcome {authenticator.get_username()}")
    st.button("Logout", "logout_btn", on_click=logout)


def passing():
    pass


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

    images = hosting_config.file_manager.read_document(image_file_name)
    resized_images = []
    scaled_bounding_boxes = []
    heights = []
    widths = []

    for i, img in enumerate(images):
        img, width_scale, height_scale = resize_image(img, 800, 800)
        resized_images.append(img)
        widths.append(float(img.size[0]))
        heights.append(float(img.size[1]))

        page_scaled_bounding_boxes = scale_bounding_box(bounding_boxes, width_scale, height_scale, i + 1, heights)
        scaled_bounding_boxes.extend(page_scaled_bounding_boxes)

    new_img = create_img(resized_images, widths, heights)
    bounding_boxes["objects"] = scaled_bounding_boxes

    return new_img, image_file_name, bounding_boxes


def add_sidebar_empty_space(n):
    for _ in range(n):
        st.sidebar.markdown("<br>", unsafe_allow_html=True)


def create_session_state_dict(session_state) -> dict:
    session_state["label_folder_path"] = os.path.join(hosting_config.CONFIG["OCR_results_path"], session_state["selected_label"])
    list_files = [file for file in hosting_config.file_manager.list_files_in_folder(session_state["label_folder_path"]) if file.endswith(".json")]
    list_files.sort()
    session_state["OCR_output_files"] = list_files
    session_state["output_folder_path"] = os.path.join(hosting_config.CONFIG['output_path'], session_state["selected_label"])
    hosting_config.file_manager.create_folder(session_state["output_folder_path"])
    session_state["curation_output_files"] = [file for file in hosting_config.file_manager.list_files_in_folder(session_state["output_folder_path"]) if file.endswith(".json")]
    return session_state


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

if "bounding_boxes" not in st.session_state:
    st.session_state["bounding_boxes"] = dict()

user_name = st.session_state.get("username", authenticator.get_username())

if "initialized" not in st.session_state or not st.session_state["initialized"]:

    if st.session_state["selected_label"] == "":
        st.markdown(
            "<h1 style='text-align: center;'>Let's start</h1>",
            unsafe_allow_html=True
        )
        labels = hosting_config.file_manager.get_label_folder()
        label = st.selectbox("Select the Label:", labels)

        col3, col4 = st.columns([8, 1])
        if col4.button("Next", on_click=passing()):
            st.session_state["selected_label"] = label
            st.session_state = create_session_state_dict(st.session_state)
            st.session_state["initialized"] = True
            st.experimental_rerun()
    else:
        st.session_state = create_session_state_dict(st.session_state)
        st.session_state["initialized"] = True
        st.experimental_rerun()

elif len(st.session_state["OCR_output_files"]) == 0:
    st.markdown("<h1 style='text-align: center;'>You're done!</h1>", unsafe_allow_html=True)

elif "label_folder_path" in st.session_state:
    current_file = st.session_state["OCR_output_files"][0]
    st.session_state["bounding_boxes"] = hosting_config.file_manager.read_file(os.path.join(st.session_state["label_folder_path"], current_file))
    if len(st.session_state["bounding_boxes"]["objects"]) > 0 and st.session_state["bounding_boxes"]["user_reviewed"] == 1 \
            and not st.session_state["previous_clicked"]:
        next_page()

    # show sidebar
    # add default width for sidebar
    st.markdown(
        """
       <style>
       [data-testid="stSidebar"][aria-expanded="true"]{
           min-width: 500px;
           max-width: 500px;
       }
       """,
        unsafe_allow_html=True,
    )

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

    resized_images, image_file_name, st.session_state["bounding_boxes"] = handle_image_and_bounding_box(current_file, st.session_state["bounding_boxes"])

    col1, col2 = st.sidebar.columns([1, 1])

    if col1.button("Refresh image", on_click=passing()):
        st.session_state["bounding_boxes"]["user_reviewed"] = 0
        for box in st.session_state["bounding_boxes"]["objects"]:
            box["fill"] = "rgb(0, 0, 0, 0)"
            box["stroke"] = "rgb(0, 0, 0, 0)"
            box["result"] = False
            box["group_id"] = box["index"]
            hosting_config.file_manager.save_current_state(current_file, st.session_state["bounding_boxes"], st.session_state["label_folder_path"], user_name)
        placeholder = st.empty()
        placeholder.empty()

    if col2.button("Restore skipped files"):
        for file in st.session_state["curation_output_files"][0:]:
            skipped_bounding_boxes = hosting_config.file_manager.read_file(os.path.join(st.session_state["output_folder_path"], file))
            if skipped_bounding_boxes["user_reviewed"] == 0:
                hosting_config.file_manager.move_files(
                    input_path=st.session_state["output_folder_path"],
                    output_path=st.session_state["label_folder_path"],
                    file_name=file
                )
                current_file = st.session_state["curation_output_files"].pop()
                st.session_state["OCR_output_files"].insert(0, current_file)

        st.session_state["initialized"] = False
        st.experimental_rerun()

    add_sidebar_empty_space(5)
    col3, col4 = st.sidebar.columns([2, 5])

    if col4.button("Wrong data point", on_click=passing()):
        hosting_config.file_manager.save_current_state(current_file, handle_wrong_datapoint(st.session_state["bounding_boxes"], user_name), st.session_state["label_folder_path"], user_name)
        next_page()

    if col4.button("Missing information", on_click=passing()):
        hosting_config.file_manager.save_current_state(current_file, handle_missing_datapoint(st.session_state["bounding_boxes"], user_name), st.session_state["label_folder_path"], user_name)
        next_page()

    add_sidebar_empty_space(5)
    col5, col6, col7 = st.sidebar.columns([3, 3, 1])
    if len(st.session_state.get("curation_output_files", [])) > 0:
        if col5.button("Previous", on_click=passing()):
            previous_page()

    if col7.button("Skip", on_click=passing()):
        st.session_state["bounding_boxes"]["user_reviewed"] = 0
        hosting_config.file_manager.save_current_state(current_file, st.session_state["bounding_boxes"], st.session_state["label_folder_path"], user_name)
        next_page()

    # show image part
    canvas_result = st_canvas(
        background_image=resized_images,
        display_toolbar=False,
        update_streamlit=True,
        height=resized_images.size[1],
        width=resized_images.size[0],
        drawing_mode="transform",
        key=f"{image_file_name}",
        initial_drawing={"objects": [box for box in st.session_state["bounding_boxes"]["objects"]]},
    )
    if canvas_result.json_data is not None:

        st.session_state["bounding_boxes"] = handle_user_choice(st.session_state["bounding_boxes"], canvas_result.json_data["objects"], user_name)

    if col6.button("Validate", on_click=passing()):
        hosting_config.file_manager.save_current_state(current_file, st.session_state["bounding_boxes"], st.session_state["label_folder_path"], user_name)
        next_page()
    st.write(image_file_name)