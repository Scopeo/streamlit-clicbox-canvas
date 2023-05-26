from file_management import AWSFileManagement, LocalFileManagement

HOSTING_MODE = "AWS"
if HOSTING_MODE == "AWS":
    CONFIG = {
        "OCR_results_path": "sample_predicted_data_to_curate/",
        "images_path": "2240_invoices_supplier/",
        "output_path": "new_results/",
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
        "OCR_results_path": "CV_data/json_resume_to_curate",
        "images_path": "CV_data/CV",
        "output_path": "CV_data/results"
    }
    file_manager = LocalFileManagement(
        CONFIG["OCR_results_path"],
        CONFIG["images_path"],
        CONFIG["output_path"]
    )
else:
    raise ValueError("Invalid file management type")
