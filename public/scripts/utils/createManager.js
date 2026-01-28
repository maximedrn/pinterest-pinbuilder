import { defined } from "../common/defined.js";
import "../common/format.js";
import { reachableElement } from "../common/reachableElement.js";
import { displayMessage } from "../utils/worker/snackbarManager.js";
import { CHECKED, FIELD_REQUIRED } from "./constants/attributes.js";
import {
    CONTAINER_ASSETS_ACTION_BUTTONS,
    CONTAINER_ASSETS_LIST,
    CONTAINER_BROWSED_ASSETS_FOLDER_TEXT,
    ELEMENT_APPLY_FOR_ALL_BUTTON,
    ELEMENT_ASSETS_FOLDER_CLEAR,
    ELEMENT_ASSETS_PREVIEW,
    ELEMENT_BROWSED_ASSETS_FOLDER_BUTTON,
    ELEMENT_BROWSED_ASSETS_FOLDER_TEXT,
    ELEMENT_CREATE_FIELDS,
    ELEMENT_LOADING_ASSETS,
    ELEMENT_LOADING_ASSETS_TEXT,
    ELEMENT_NEXT_ASSET_BUTTON,
    ELEMENT_NEXT_CHUNK_BUTTON,
    ELEMENT_ORGANIC_PIN,
    ELEMENT_PAID_PIN,
    ELEMENT_PIN_TYPE_TOGGLE,
    ELEMENT_PINBOARD_FIELD,
    ELEMENT_PREVIOUS_ASSET_BUTTON,
    ELEMENT_PREVIOUS_CHUNK_BUTTON,
    ELEMENT_REMOVE_BY_INDEX_BUTTON,
    ELEMENT_REMOVE_FOR_ALL_BUTTON,
    ELEMENT_SAVE_BUTTON,
    IMAGE
} from "./constants/elements.js";
import {
    ASSETS_LOADING_TEXT,
    BASE_64,
    NO_FOLDER_SELECTED_TEXT,
    NUMBER_OF_ASSETS
} from "./constants/texts.js";
import { CREATE_FILE, DATA_FILES_KEYS, PAID_PIN, TOPIC_TAGS } from "./constants/values.js";
import { TagManager } from "./tagsManager.js";
import { snackbarMessage } from "./worker/snackbarManager.js";
import { startLogWorker, stopLogWorker } from "./worker/workerManager.js";

/**
 * CreateManager class manages the creation of objects with pins.
 */
export class CreateManager extends TagManager {

    /**
     * Create a new CreateManager instance.
     * Initializes the selected pin to 0.
     */
    constructor() {
        super();
        // The selected pin represents the current pin in use.
        this._selected_pin = 0; // Initialize it to 0 by default.
        this.worker = null;
    }

    /**
     * Select an asset from the list and display its details.
     *
     * @param {number} index - The index of the asset to select.
     */
    #selectAsset(index) {
        const assetsContainer = document.querySelector(CONTAINER_ASSETS_LIST);
        const assets = [...assetsContainer.children];
        const selectedAsset = assets.at(index);
        selectedAsset.setAttribute(CHECKED, "");

        const scrollPosition = selectedAsset.offsetTop - (selectedAsset.offsetHeight * 2);
        assetsContainer.scrollTop = scrollPosition;

        this._selected_pin = index;
        this.#editEditionState(true);
        this.#getPinData();
    }

    /**
     * Loads the previous chunk of assets and updates the asset preview and data
     * fields. This method is triggered when the "Previous" button is clicked.
     */
    async #loadPreviousChunk(index) {
        // Load the previous chunk and check if the limit is reached.
        const isLimitNotReached = await eel.load_previous_chunk()();
        // If the limit is reached, exit the function.
        if (!isLimitNotReached && !isNaN(index)) return this.#selectAsset(index);
        if (!isLimitNotReached) return;
        // Load and display the assets preview from the previous chunk.
        const length = await this.#loadAssetsPreviewBinary();
        // Clear the data fields related to the previous chunk.
        this.#emptyPinDataFields();
        if (length - 1 >= 0) this.#selectAsset(length - 1);
    }

    /**
     * Attach a click event listener to the "Previous" button to load the
     * previous chunk of data.
     *
     * This method adds a click event listener to the "Previous" button
     * element, which, when clicked, triggers the loading of the previous
     * chunk of data. It also temporarily disables the button during the
     * loading process and re-enables it when the operation is complete.
     */
    #loadPreviousChunkEvent() {
        // Get a reference to the "Previous" button element.
        const previousChunkButton = document.querySelector(ELEMENT_PREVIOUS_CHUNK_BUTTON);
        // Add a click event listener to the "Previous" button.
        previousChunkButton.addEventListener("click", async () => {
            reachableElement(previousChunkButton, false);
            await this.#loadPreviousChunk();
            reachableElement(previousChunkButton, true);
        });
    }

    /**
     * Loads the next chunk of assets and updates the asset preview and data
     * fields. This method is triggered when the "Next" button is clicked.
     */
    async #loadNextChunk(index) {
        // Load the next chunk and check if the limit is reached.
        const isLimitNotReached = await eel.load_next_chunk()();
        // If the limit is reached, exit the function.
        if (!isLimitNotReached && !isNaN(index)) return this.#selectAsset(index);
        if (!isLimitNotReached) return;
        // Load and display the assets preview from the next chunk.
        await this.#loadAssetsPreviewBinary();
        // Clear the data fields related to the previous chunk.
        this.#emptyPinDataFields();
        this.#selectAsset(0);
    }

    /**
     * Attach a click event listener to the "Next" button to load the next
     * chunk of data.
     *
     * This method adds a click event listener to the "Next" button element,
     * which, when clicked, triggers the loading of the next chunk of data.
     * It also temporarily disables the button during the loading process
     * and re-enables it when the operation is complete.
     */
    #loadNextChunkEvent() {
        // Get a reference to the "Next" button element.
        const nextChunkButton = document.querySelector(ELEMENT_NEXT_CHUNK_BUTTON);
        // Add a click event listener to the "Next" button.
        nextChunkButton.addEventListener("click", async () => {
            reachableElement(nextChunkButton, false);
            await this.#loadNextChunk();
            reachableElement(nextChunkButton, true);
        });
    }

    /**
     * Attach a click event listener to the "Previous Asset" button to load
     * the previous asset.
     *
     * This method adds a click event listener to the "Previous Asset" button
     * element, which, when clicked, allows users to navigate to the previous
     * asset within the list. If there is no previous asset in the list, it
     * loads the previous data chunk to retrieve more assets.
     */
    #loadPreviousAsset() {
        const previousAssetButton = document.querySelector(ELEMENT_PREVIOUS_ASSET_BUTTON);
        previousAssetButton.addEventListener("click", async () => {
            const assets = [...document.querySelector(CONTAINER_ASSETS_LIST).children];
            const index = assets.findIndex(element => element.hasAttribute(CHECKED));

            const element = assets.find(element => element.hasAttribute(CHECKED));
            element.removeAttribute(CHECKED);

            if (index - 1 >= 0) return this.#selectAsset(index - 1);

            reachableElement(previousAssetButton, false);
            await this.#loadPreviousChunk(index);
            reachableElement(previousAssetButton, true);
        });
    }

    /**
     * Attach a click event listener to the "Next Asset" button to load the 
     * next asset.
     *
     * This method adds a click event listener to the "Next Asset" button
     * element, which, when clicked, allows users to navigate to the next
     * asset within the list. If there is no next asset in the list, it
     * loads the next data chunk to retrieve more assets.
     */
    #loadNextAsset() {
        const nextAssetButton = document.querySelector(ELEMENT_NEXT_ASSET_BUTTON);
        nextAssetButton.addEventListener("click", async () => {
            const assets = [...document.querySelector(CONTAINER_ASSETS_LIST).children];

            const index = assets.findIndex(element => element.hasAttribute(CHECKED));
            const element = assets.find(element => element.hasAttribute(CHECKED));
            element.removeAttribute(CHECKED);

            if (index + 1 < assets.length) return this.#selectAsset(index + 1);

            reachableElement(nextAssetButton, false);
            await this.#loadNextChunk(index);
            reachableElement(nextAssetButton, true);
        });
    }

    /**
     * Initiates the saving of pin data when the save button is clicked.
     */
    #savePinData() {
        // Get a reference to the "Save" button element.
        const saveButton = document.querySelector(ELEMENT_SAVE_BUTTON);
        // Add a click event listener to the "Save" button.
        // And call the Eel function to save the file asynchronously.
        saveButton.addEventListener("click", async () => await eel.save_file()());
    }

    /**
     * Sets up utility buttons (Apply for All, Delete for All, Delete) for each
     * pin data field. This method adds event listeners to the utility buttons
     * associated with each pin data field to handle actions such as applying
     * changes for all pins or deleting data.
     */
    #fieldUtilsButtons() {
        // Retrieve all pin data fields and their corresponding elements.
        const pinData = this.#retrievePinDataFields();

        // Iterate over the pin data fields and their elements.
        Object.entries(pinData).forEach(([fieldName, fieldElement]) => {
            // Determine the parent element based on the field type.
            let parentElement = fieldElement.parentNode.parentNode;
            if (fieldName === PAID_PIN) parentElement = parentElement.parentNode;

            const emptyFields = (fieldName, fieldElement) => {
                if (fieldName === PAID_PIN) {
                    pinData.paid_pin.checked = false;
                    this.#setPinType(false);
                } else if (fieldName === TOPIC_TAGS) this._emptySelectedTopicTags();
                else fieldElement.value = "";
            }

            // Add a click event listener to the "Apply for All" button.
            const applyForAll = parentElement.querySelector(ELEMENT_APPLY_FOR_ALL_BUTTON);
            // Call the Eel function to apply the change for all pins.
            applyForAll.addEventListener("click", async () => {
                let fieldValue;
                if (fieldName === TOPIC_TAGS) fieldValue = this._getTopicTags();
                else if (fieldName === PAID_PIN) fieldValue = pinData.paid_pin.checked;
                else fieldValue = fieldElement.value;
                await eel.apply_for_all(fieldName, fieldValue);
            });

            // Add a click event listener to the "Delete for All" button.
            const deleteForAll = parentElement.querySelector(ELEMENT_REMOVE_FOR_ALL_BUTTON);
            // Call the Eel function to delete data for all pins. 
            deleteForAll.addEventListener("click", async () => {
                emptyFields(fieldName, fieldElement);
                await eel.delete_for_all(fieldName);
            });

            // Add a click event listener to the "Delete" button.
            const deleteByIndex = parentElement.querySelector(ELEMENT_REMOVE_BY_INDEX_BUTTON);
            // Clear the field's value and apply the updated data by index.
            deleteByIndex.addEventListener("click", async () => {
                emptyFields(fieldName, fieldElement);
                this.#applyDataByIndex();
            });
        });
    }

    /**
     * Set the pin type based on the specified "checked" parameter.
     *
     * This method sets the pin type (paid or organic) for a group of elements
     * based on the provided "checked" parameter. When "checked" is true, it
     * sets the elements to represent paid pins. When "checked" is false, it
     * sets the elements to represent organic pins.
     *
     * @param {boolean} checked - A boolean flag indicating the pin type to set
     * (true for paid, false for organic).
     */
    #setPinType(checked) {
        const paidPinElements = [...document.querySelectorAll(ELEMENT_PAID_PIN)];
        const organicPinElements = [...document.querySelectorAll(ELEMENT_ORGANIC_PIN)];
        paidPinElements.forEach(element => reachableElement(element, checked));
        organicPinElements.forEach(element => reachableElement(element, !checked));

        // The Pinboard is required only if it is a paid Pin.
        const pinboardInput = document.querySelector(ELEMENT_PINBOARD_FIELD);
        const pinboardTitle = pinboardInput.parentNode.parentNode.querySelector("h3");
        checked // checked = True => paid Pin is selected.
            ? pinboardTitle.classList.add(FIELD_REQUIRED)
            : pinboardTitle.classList.remove(FIELD_REQUIRED);
    }

    /**
     * Handles the pin type selection by adding event listeners to pin type
     * elements. This method allows users to select a pin type, disabling the
     * selected one and enabling other selectable pin types, ensuring only one
     * pin type is active at a time.
     */
    #pinTypeListener() {
        const pinTypeToggle = document.querySelector(ELEMENT_PIN_TYPE_TOGGLE);
        pinTypeToggle.addEventListener("change", () => this.#setPinType(pinTypeToggle.checked));
    }

    /**
     * Apply pin data changes when a pin data field is changed. This method 
     * listens for changes in pin data fields and sends updated data to Eel
     * for the selected pin index.
     */
    #applyDataByIndex() {
        const pinDataFields = this.#retrievePinDataFields();
        Object.values(pinDataFields).forEach(dataField =>
            dataField.addEventListener("change", async () => {
                // Send the updated data to Eel for the selected pin index.
                let pinData = Object.fromEntries(Object.entries(pinDataFields)
                    .map(([key, selector]) => [key, selector.value]));
                pinData.paid_pin = pinDataFields.paid_pin.checked;
                pinData.topic_tags = this._getTopicTags();
                await eel.apply_data_by_index(this._selected_pin, pinData);
            }));
    }

    /**
     * Retrieve pin data fields and their corresponding DOM elements.
     * This method retrieves and returns an object containing pin data field
     * keys and their associated DOM elements based on selector keys from
     * DATA_FILES_KEYS.
     *
     * @returns {Object} An object mapping pin data field keys to DOM elements.
     */
    #retrievePinDataFields() {
        return Object.fromEntries(Object.entries(DATA_FILES_KEYS).map(
            ([key, selector]) => [key, document.querySelector(selector)]));
    }

    /**
     * Clear the values of all pin data fields and reset the selected pin
     * to 0. This method empties the values of all pin data fields and sets
     * the selected pin index to 0.
     */
    #emptyPinDataFields() {
        const pinDataFields = this.#retrievePinDataFields();
        Object.values(pinDataFields).forEach(
            pinDataField => pinDataField.value = "");
        this._emptySelectedTopicTags();
        this._selected_pin = 0;
    }

    /**
     * Fetches pin data for the selected pin and updates the data fields.
     * This method retrieves pin data for the currently selected pin from Eel,
     * updates the data fields on the interface, and logs the received data.
     */
    async #getPinData() {
        // Retrieve pin data for the selected pin from Eel.
        const pinData = await eel.get_pin_data(this._selected_pin)();
        // Update the data fields with the retrieved pin data.
        const pinDataFields = this.#retrievePinDataFields();
        Object.entries(pinDataFields).map(([key, field]) =>
            field.value = defined(pinData[key]) ? pinData[key] : "");
        pinDataFields.paid_pin.checked = !!pinData.paid_pin;
        this.#setPinType(pinDataFields.paid_pin.checked);
        this._setTopicTags(pinData.topic_tags);
    }

    #editEditionState(enabled) {
        // Enable and configure data fields container.
        const createElements = [
            document.querySelector(ELEMENT_CREATE_FIELDS),
            document.querySelector(ELEMENT_SAVE_BUTTON),
            ...document.querySelector(CONTAINER_ASSETS_ACTION_BUTTONS).children];
        createElements.forEach(element => reachableElement(element, enabled));

        if (enabled) return;
        this.#emptyPinDataFields();
        this._emptySelectedTopicTags();
        this._selected_pin = 0;
    }

    /**
     * Loads assets' binary data and displays them in the asset container.
     * This method fetches binary data for assets from Eel, displays them as
     * images in the asset container, and configures interaction behavior like 
     * election and layout.
     *
     * @returns {boolean} True if assets were loaded successfully, false otherwise.
     */
    async #loadAssetsPreviewBinary() {
        // Fetch binary data for assets from Eel.
        const assetsBinary = await eel.get_assets_preview_binary()();
        // Check if assets binary data is empty.
        if (!assetsBinary.length) return false;

        // Get a reference to the assets container in the DOM.
        const assetsContainer = document.querySelector(CONTAINER_ASSETS_LIST);
        assetsContainer.innerHTML = ""; // Clear previous content.

        // Initialize the Masonry layout for the assets container.
        const masonry = new Masonry(assetsContainer, {
            itemSelector: ELEMENT_ASSETS_PREVIEW,
            horizontalOrder: true,
            fitWidth: true
        });

        // Iterate over each asset binary data and create image elements.
        const validAssetsBinary = assetsBinary.filter(assetBinary => !!assetBinary);
        validAssetsBinary.forEach(assetBinary => {
            const imageElement = document.createElement(IMAGE);
            imageElement.className = ELEMENT_ASSETS_PREVIEW.slice(1);
            imageElement.src = BASE_64.format(assetBinary);

            // Append the image to the assets container and adjust the layout.
            assetsContainer.appendChild(imageElement);
            masonry.appended(imageElement);
            imagesLoaded(imageElement, () => masonry.layout());

            // Add a click event listener to display data for the clicked image.
            imageElement.addEventListener("click", async () => {
                const images = [...assetsContainer.children];
                images.filter(image => image !== imageElement)
                    .forEach(image => image.removeAttribute(CHECKED));

                // Toggle the "checked" attribute for the selected image.
                if (imageElement.hasAttribute(CHECKED)) {
                    imageElement.removeAttribute(CHECKED);
                    this.#editEditionState(false);
                    return;
                }

                imageElement.setAttribute(CHECKED, "");
                // Update the selected pin index and display the the data.
                this._selected_pin = images.indexOf(imageElement);
                this.#editEditionState(true);
                await this.#getPinData();
            });
        });
        return assetsBinary.length; // Assets were loaded successfully.
    }

    /**
     * Handles the selection of an assets folder and initializes the asset 
     * creation manager. This method sets up event listeners for selecting an
     * assets folder, starting the creation manager, and configuring the user
     * interface based on the selected folder and assets.
     */
    assetsFolderSelection() {
        // Get a reference to the assets folder input element.
        const assetsFolderInput = document.querySelector(ELEMENT_BROWSED_ASSETS_FOLDER_BUTTON);

        // Add a click event listener to the assets folder input.
        assetsFolderInput.addEventListener("click", async () => {
            // Prompt the user to select an assets folder and retrieve the selected
            // folder path and the number of assets in the folder.
            const [selectedFolder, numberOfAssets] = await eel.browse_folder()();
            // Check if the selected folder or number of assets is missing.
            if (!selectedFolder || !numberOfAssets) return;

            const [isValid, errorMessage] = await eel.start_creation_manager(
                selectedFolder)(); // Start the creation manager and check its validity.
            if (!isValid) { // If the creation manager is not valid,
                displayMessage(errorMessage); // display an error message and exit.
                return;
            }

            // Display the loading text while the assets are loading.
            const assetsLoadingContainer = document.querySelector(ELEMENT_LOADING_ASSETS);
            const assetsLoadingText = document.querySelector(ELEMENT_LOADING_ASSETS_TEXT);
            assetsLoadingText.innerHTML = ASSETS_LOADING_TEXT;

            // Load and display the assets preview in binary format.
            if (!await this.#loadAssetsPreviewBinary()) {
                assetsLoadingText.innerHTML = NO_FOLDER_SELECTED_TEXT;
                return;
            }
            assetsLoadingContainer.style.display = "none";

            // Update and display the number of assets and the selected folder.
            const assetsSpanText = [...document.querySelectorAll(ELEMENT_BROWSED_ASSETS_FOLDER_TEXT)];
            assetsSpanText[0].innerHTML = NUMBER_OF_ASSETS.format(numberOfAssets);
            assetsSpanText.at(-1).innerHTML = selectedFolder;
            const assetsPath = document.querySelector(CONTAINER_BROWSED_ASSETS_FOLDER_TEXT);
            assetsPath.style.display = "";

            // Enable and configure UI elements in the assets container.
            const assetsSaveButton = document.querySelector(ELEMENT_SAVE_BUTTON);
            const previousButton = document.querySelector(ELEMENT_PREVIOUS_CHUNK_BUTTON);
            const nextButton = document.querySelector(ELEMENT_NEXT_CHUNK_BUTTON);
            const assetsContainer = [assetsSaveButton, previousButton, nextButton];
            assetsContainer.forEach(element => reachableElement(element, true));
            this.#selectAsset(0);

            // Display and configure the assets clear button.
            const assetsClearButton = document.querySelector(ELEMENT_ASSETS_FOLDER_CLEAR);
            assetsClearButton.style.display = "";
            assetsClearButton.addEventListener("click", () => {
                // Clear and hide the displayed information and assets.
                assetsSpanText.forEach(span => span.innerHTML = "");
                assetsSpanText.forEach(span => span.style.display = "none");
                assetsClearButton.style.display = "none";

                assetsLoadingContainer.style.display = "block";
                assetsLoadingText.innerHTML = NO_FOLDER_SELECTED_TEXT;

                const assetsContainer = document.querySelector(CONTAINER_ASSETS_LIST);
                assetsContainer.innerHTML = "";
                assetsContainer.style.height = "";

                // Disable UI elements in the assets container.
                this.#editEditionState(false);
                stopLogWorker(this.worker);
            });

            // Initialize event handlers for various actions.
            this.#loadPreviousChunkEvent();
            this.#loadNextChunkEvent();
            this.#loadPreviousAsset();
            this.#loadNextAsset();
            this.#savePinData();
            this.#fieldUtilsButtons();
            this.#pinTypeListener();
            this.#applyDataByIndex();
            this._retrieveTags();

            this.worker = startLogWorker(
                CREATE_FILE, (message) => snackbarMessage(message));
        });
    }
}
