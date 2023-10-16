// web/js/utils/updateManager.js

/**
 * @author: Pinterest Pinbuilder.
 * Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
 * Any distribution, modification or commercial use is strictly prohibited.
 */


import { displayMessage } from "../utils/worker/snackbarManager.js";
import {
    ELEMENT_UPDATE_CHANGELOG,
    ELEMENT_UPDATE_CHANGELOG_LIST,
    ELEMENT_UPDATE_BUTTON,
    ELEMENT_UPDATE_CLOSE,
    CONTAINER_UPDATE
} from "./constants/elements.js";


/**
 * Adds an event listener to the update download button, allowing users
 * to initiate the download of a software update. When the button is clicked,
 * this function sends a request to download the update through Eel (a Python
 * interface) and closes the window if the update starts successfully.
 */
function downloadUpdateButton() {
    // Add a click event listener to the update download button.
    const updateButton = document.querySelector(ELEMENT_UPDATE_BUTTON);
    updateButton.addEventListener("click", async () => {
        // Send a request to ask to download the update.
        const errorMessage = await eel.download_update()();
        // If there is no error message from the Python interface,
        if (!errorMessage) { // it means the update can be done.
            eel.download_update(true); // Start the update.
            window.close(); // Close the interface.
        }
        displayMessage(errorMessage);
    });
}


/**
 * Adds an event listener to the close button in the update popup window.
 * When the button is clicked, this function hides the update popup by
 * setting its display property to "none."
 */
function downloadCloseButton() {
    // Get references to the update popup and the close button elements.
    const updatePopUp = document.querySelector(CONTAINER_UPDATE);
    const updateCloseButton = document.querySelector(ELEMENT_UPDATE_CLOSE);
    // Add a click event listener to the close button to
    // hide the update popup by changing its display property.
    updateCloseButton.addEventListener("click", () =>
        updatePopUp.style.display = "none");
}


/**
 * Checks for a software update and updates the interface to display the
 * changelog and buttons for downloading the update or closing the update
 * notification popup.
 */
export async function checkForUpdate() {
    // Check if there is a new update available through Eel.
    const isNewUpdate = await eel.check_for_update()();
    if (!isNewUpdate) return; // No update available, exit.

    // Retrieve the tool's changelog from Eel.
    const changelog = await eel.retrieve_tool_changelog()();

    // Get references to the changelog container and the changelog list container.
    const changelogContainer = document.querySelector(ELEMENT_UPDATE_CHANGELOG);
    const changelogListContainer = document.querySelector(ELEMENT_UPDATE_CHANGELOG_LIST);

    // If there are no changelog entries, hide the changelog container.
    if (!changelog.length) changelogContainer.style.display = "none";

    // Populate the changelog list container with the retrieved
    changelog.forEach(element => { // changelog entries.
        const elementContainer = document.createElement("li");
        elementContainer.appendChild(document.createTextNode(element));
        changelogListContainer.appendChild(elementContainer);
    });

    // Display the update popup.
    const updatePopUp = document.querySelector(CONTAINER_UPDATE);
    updatePopUp.style.display = "";

    // Add event listeners for the download update and close buttons.
    downloadUpdateButton();
    downloadCloseButton();
}
