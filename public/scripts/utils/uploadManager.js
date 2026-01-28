import { displayMessage } from "../utils/worker/snackbarManager.js";
import { PROCESS_STARTED, SELECTED } from "./constants/attributes.js";
import {
    ELEMENT_BROWSED_FILE,
    ELEMENT_DELETE_TEMP_FILE,
    ELEMENT_MAXIMUM_ATTEMPTS,
    ELEMENT_SELECTED_ACCOUNT,
    ELEMENT_SELECTED_FILE,
    ELEMENT_STARTING_VALUE,
    ELEMENT_UPLOAD_BUTTON,
    ELEMENT_UPLOAD_BUTTON_TEXT
} from "./constants/elements.js";
import { SNACKBAR_CANNOT_BE_EMPTY, START_TEXT, STOP_TEXT } from "./constants/texts.js";
import { DATA_FILE, UPLOAD_FILE, UUID } from "./constants/values.js";
import { displayConsoleOutputs } from "./worker/consoleManager.js";
import { startLogWorker, stopLogWorker } from "./worker/workerManager.js";


/**
 * Represents an Upload Manager for handling file uploads and processing.
 */
export class UploadManager {

    /**
     * Constructor for the UploadManager class.
     * Initialize a new instance of the UploadManager class.
     */
    constructor() {
        this.worker = null;
    }

    /**
     * Check if the process encountered an error and display a message if needed.
     *
     * @param {boolean} isRunning - Indicates if the process is running.
     * @param {string} error - The error message to display.
     * @returns {boolean} - Indicates if the process is running.
     */
    #checkProcessError(isRunning, error) {
        if (!isRunning) { // The process is not running.
            displayMessage(error); // Show the error.
            // Reset the upload button states and its text content.
            const uploadButton = document.querySelector(ELEMENT_UPLOAD_BUTTON);
            uploadButton.classList.remove(SELECTED);
        }
        return isRunning;
    }

    /**
     * Retrieve and validate required process fields from the UI.
     *
     * @returns {[boolean, Object]} - A tuple indicating if the fields are 
     * valid and an object containing the required fields.
     */
    #retrieveProcessFields() {
        // Retrieve the selected or browsed file (browsed > selected).
        let selectedFile = document.querySelector(ELEMENT_BROWSED_FILE)?.getAttribute(DATA_FILE);
        if (!selectedFile) selectedFile = document.querySelector(ELEMENT_SELECTED_FILE)?.getAttribute(DATA_FILE);
        const accountName = document.querySelector(ELEMENT_SELECTED_ACCOUNT)?.getAttribute(UUID);
        const startingValue = document.querySelector(ELEMENT_STARTING_VALUE)?.value;
        const maximumAttempts = document.querySelector(ELEMENT_MAXIMUM_ATTEMPTS)?.value;
        const deleteTempFile = document.querySelector(ELEMENT_DELETE_TEMP_FILE)?.checked;

        // Required fields constant.
        const requiredFields = {
            "Process file": selectedFile,
            "Account": accountName,
            "Starting value": startingValue,
            "Number of attempts": maximumAttempts
        }

        // Check each required field value and return a boolean according
        // if one of them is missing or not, and the field values.
        for (const [fieldName, value] of Object.entries(requiredFields)) {
            if (value) continue; // The value exists.
            // The value does not exist, display an error and return false.
            displayMessage(fieldName + SNACKBAR_CANNOT_BE_EMPTY);
            return [false, []];
        }

        const content = {
            file_path: selectedFile,
            uuid: accountName,
            starting_value: parseInt(startingValue) - 1 || 0,
            maximum_attempts: parseInt(maximumAttempts) || 1,
            delete_temp_file: !deleteTempFile
        }

        return [true, content];
    }

    /**
     * Handle the upload process, including starting and stopping.
     */
    uploadProcess() {
        const uploadButton = document.querySelector(ELEMENT_UPLOAD_BUTTON);
        const uploadButtonText = document.querySelector(ELEMENT_UPLOAD_BUTTON_TEXT);
        uploadButton.addEventListener("click", async () => {

            // In case a process is already started, stop it by calling 
            // Python and set the upload button state to default.
            if (uploadButton.classList.contains(PROCESS_STARTED)) {
                await eel.stop_upload_process()();
                uploadButtonText.textContent = START_TEXT;
                uploadButton.classList.remove(PROCESS_STARTED);
                uploadButton.classList.remove(SELECTED);
                stopLogWorker(this.worker);
                return;
            }

            // Retrieve and check the fields.
            const [isOk, content] = this.#retrieveProcessFields();
            if (!isOk) return; // One of the fields value is incorrect.

            // Set the state of the upload button and start the worker.
            uploadButton.classList.add(SELECTED);
            this.worker = startLogWorker(
                UPLOAD_FILE, (message) => displayConsoleOutputs(message));

            // Start the upload process (and maybe a login process if required).
            const [isRunning, error] = await eel.start_upload_process(content)();
            if (!this.#checkProcessError(isRunning, error)) return;
            uploadButton.classList.add(PROCESS_STARTED);

            // Change the state of the upload button -> become a stop button.
            uploadButton.classList.remove(SELECTED);
            uploadButtonText.textContent = STOP_TEXT;
        });
    }
}
