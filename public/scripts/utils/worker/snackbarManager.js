// web/js/utils/worker/snackbarManager.js

/**
 * @author: Pinterest Pinbuilder.
 * Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
 * Any distribution, modification or commercial use is strictly prohibited.
 */


import { SHOW } from "../constants/attributes.js";
import {
    ELEMENT_SNACKBAR,
    ELEMENT_SNACKBAR_ICON,
    ELEMENT_SNACKBAR_TEXT
} from "../constants/elements.js";


/**
 * Display a message in a snackbar on the web page.
 *
 * This function finds the snackbar element on the web page and updates its
 * appearance based on the provided message object. The message object can
 * contain a color for the snackbar background, an icon, and the text message
 * to display. The snackbar is shown for 5 seconds and then automatically
 * hidden.
 *
 * @param {Object} message - The message object to display in the snackbar.
 * @param {string} message.color - The background color for the snackbar.
 * @param {string} message.icon - The icon to display in the snackbar.
 * @param {string} message.message - The text message to display in the snackbar.
 */
function displaySnackbar(message) {
    // Find the snackbar element on the web page.
    const snackbarElement = document.querySelector(ELEMENT_SNACKBAR);
    // Find the snackbar span element within the snackbar.
    const snackbarSpan = document.querySelector(ELEMENT_SNACKBAR_TEXT);
    // Find the snackbar icon element within the snackbar.
    const snackbarIcon = document.querySelector(ELEMENT_SNACKBAR_ICON);

    const color = message?.color;
    const icon = message?.icon;

    if (color) snackbarElement.style.background = color;
    if (icon) snackbarIcon.textContent = icon;
    snackbarSpan.textContent = message.message.toString();

    // Add the "show" class to the snackbar element to make it visible.
    snackbarElement.classList.add(SHOW);
    // Hide the message after 5 seconds using a timeout.
    setTimeout(() => snackbarElement.classList.remove(SHOW), 5000);
};

/**
 * Display a message in a snackbar on the web page.
 *
 * @param {string} requiredValueName - The name or description of the
 * required value.
 */
export function displayMessage(message) {
    displaySnackbar({message: message});
}

/**
 * Display a message in a snackbar on the web page.
 *
 * @param {string} message - The JSON-encoded message to display in
 * the snackbar.
 */
export function snackbarMessage(message) {
    message = JSON.parse(message).at(0);
    displaySnackbar(message);
}
