from file_management import AWSFileManagement, LocalFileManagement

HOSTING_MODE = "Local"
if HOSTING_MODE == "AWS":
    CONFIG = {
        "OCR_results_path": "1000_json_resume_curate/",
        "images_path": "1000_CV/",
        "output_path": "1000_resume_results/",
        "bucket": 'data-curation-application'
    }
    file_manager = AWSFileManagement(
        CONFIG["bucket"],
        CONFIG["OCR_results_path"],
        CONFIG["images_path"],
        CONFIG["output_path"]
    )
elif HOSTING_MODE == "Local":
    CONFIG = {
        "OCR_results_path": "CV_data/1000_CV_json_to_curate_check",
        "images_path": "CV_data/1000_CV",
        "output_path": "CV_data/1000_resume_results_check"
    }
    file_manager = LocalFileManagement(
        CONFIG["OCR_results_path"],
        CONFIG["images_path"],
        CONFIG["output_path"]
    )
else:
    raise ValueError("Invalid file management type")
