import "../../common/format.js";
import { stringToElement } from "../../common/stringToElement.js";
import { SHOW } from "../constants/attributes.js";
import { SNACKBAR_HTML_ELEMENT } from "../constants/dom.js";
import {
    CONTAINER_SNACKBAR,
    ELEMENT_SNACKBAR_ICON,
    ELEMENT_SNACKBAR_TEXT,
    ELEMENT_SNACKBAR_UUID
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
    if (!message || !message?.message) return;

    const uuid = crypto.randomUUID();
    const snackbarString = SNACKBAR_HTML_ELEMENT.format(uuid);
    const snackbarHtml = stringToElement(snackbarString);

    const snackbarContainer = document.querySelector(CONTAINER_SNACKBAR);
    snackbarContainer.insertBefore(snackbarHtml, snackbarContainer.firstChild);

    // Find the snackbar element on the web page.
    const snackbarQuerySelector = ELEMENT_SNACKBAR_UUID.format(uuid);
    const snackbarElement = document.querySelector(snackbarQuerySelector);
    // Find the snackbar span element within the snackbar.
    const snackbarSpan = snackbarElement.querySelector(ELEMENT_SNACKBAR_TEXT);
    // Find the snackbar icon element within the snackbar.
    const snackbarIcon = snackbarElement.querySelector(ELEMENT_SNACKBAR_ICON);

    const color = message?.color;

    if (color) snackbarElement.style.background = color;
    snackbarIcon.textContent = message?.icon || "warning";
    snackbarSpan.textContent = message.message.toString();

    // Add the "show" class to the snackbar element to make it visible.
    snackbarElement.classList.add(SHOW);
    // Hide the message after 3 seconds using a timeout.
    setTimeout(() => {
        snackbarElement.classList.remove(SHOW);
        snackbarElement.remove();
    }, 3000);
};

/**
 * Display a message in a snackbar on the web page.
 *
 * @param {string} requiredValueName - The name or description of the
 * required value.
 */
export function displayMessage(message) {
    displaySnackbar({ message: message });
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
