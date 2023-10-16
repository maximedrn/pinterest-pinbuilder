// web/js/utils/licenseKeyManager.js

/**
 * @author: Pinterest Pinbuilder.
 * Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
 * Any distribution, modification or commercial use is strictly prohibited.
 */


import { checkForUpdate } from "./updateManager.js";
import { displayMessage } from "../utils/worker/snackbarManager.js";
import { ENABLED } from "./constants/attributes.js";
import {
    ELEMENT_LICENSE_KEY_CLOSE,
    ELEMENT_LICENSE_KEY_BUTTON,
    ELEMENT_LICENSE_KEY_DISABLE_TEXT,
    ELEMENT_LICENSE_KEY_ENABLE_TEXT,
    ELEMENT_LICENSE_KEY_INPUT,
    CONTAINER_LICENSE_KEY,
    CONTAINER_LICENSE_KEY_TEXT
} from "./constants/elements.js";


/**
 * Checks the validity of a license key and manages the interface accordingly.
 * This function handles user interactions with the license key popup, including
 * opening and closing the popup, validating the license key, and updating the
 * interface to indicate the license key's status.
 */
export async function checkLicenseKey() {
    const licenseKeyPopup = document.querySelector(CONTAINER_LICENSE_KEY);

    // Adds a listener to close the popup when the cross button is clicked.
    document.querySelector(ELEMENT_LICENSE_KEY_CLOSE).addEventListener(
        "click", () => licenseKeyPopup.style.display = "none");

    // Retrieve the two texts corresponding to the tool's activation status.
    const licenseKeyEnableText = document.querySelector(ELEMENT_LICENSE_KEY_ENABLE_TEXT);
    const licenseKeyDisableText = document.querySelector(ELEMENT_LICENSE_KEY_DISABLE_TEXT);
    // When the texts container is clicked, the license key management popup appears.
    const licenseKeyTextsContainer = document.querySelector(CONTAINER_LICENSE_KEY_TEXT);
    licenseKeyTextsContainer.addEventListener("click", () =>
        licenseKeyPopup.style.display = "");

    /**
     * Updates the interface display to indicate that the license key is valid.
     * This function modifies the visibility and style of various elements in the 
     * interface to communicate that the license key is correct and enabled.
     */
    const licenseKeyIsValid = () => {
        licenseKeyTextsContainer.classList.add(ENABLED);
        licenseKeyDisableText.style.display = "none";
        licenseKeyEnableText.style.display = "";
        licenseKeyPopup.style.display = "none";
    }

    // Add a listener for when the license key confirmation button is clicked.
    const licenseKeyField = document.querySelector(ELEMENT_LICENSE_KEY_INPUT);
    const confirmButton = document.querySelector(ELEMENT_LICENSE_KEY_BUTTON);
    confirmButton.addEventListener("click", async () => {
        // Communicate the license key with the Python interface.
        const [isValid, errorMessage] = await eel.send_license_key(
            licenseKeyField.value)();

        // Display (error) message if returned by Python interface.
        if (errorMessage) displayMessage(errorMessage);
        if (!isValid) {  // It returned an invalid license key.
            licenseKeyTextsContainer.classList.remove(ENABLED);
            licenseKeyDisableText.style.display = "";
            licenseKeyEnableText.style.display = "none";
            return; // Quit the listener, no need to continue.
        }

        licenseKeyIsValid();
        await checkForUpdate(); // Request for tool update check.
    });

    // When the tool is launched, check that the license key (if any) 
    // is valid or not. If it is valid, the interface is changed and
    // the key is added to the field.
    const validLicenseKey = await eel.check_license_key()();
    if (validLicenseKey) {
        const licenseKey = await eel.retrieve_license_key()();
        licenseKeyField.setAttribute("value", licenseKey);
        licenseKeyIsValid();
        await checkForUpdate(); // Request for tool update check.
    }
}
