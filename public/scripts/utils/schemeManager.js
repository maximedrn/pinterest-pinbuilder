import {
    ELEMENT_IFRAME,
    ELEMENT_SCHEME_MODE_BUTTON,
    FAVICON_ELEMENT
} from "./constants/elements.js";
import { DARK, FAVICON_PATH, LIGHT } from "./constants/values.js";


/**
 * Determines the scheme mode (light or dark) based on a media query event.
 *
 * @param {MediaQueryListEvent} event - The media query event to check.
 * @returns {string} The scheme mode, either DARK or LIGHT.
 */
export function getSchemeMode(event) {
    return event.matches ? DARK : LIGHT;
}


/**
 * Sets the color scheme mode for the application and updates the HTML root
 * element's class to apply the chosen color scheme. Additionally, it updates
 * the favicon element to reflect the selected color scheme, if the favicon
 * element exists.
 *
 * @param {string} schemeMode - The desired color scheme mode.
 */
export function setSchemeMode(schemeMode) {
    // Set the HTML root element's class to apply the chosen color scheme.
    document.documentElement.className = schemeMode;
    // Find and update the favicon element to reflect the chosen scheme.
    const favicon = document.querySelector(FAVICON_ELEMENT);
    // Ensure the favicon element exists before attempting to update it.
    if (favicon) favicon.href = FAVICON_PATH.format(schemeMode);
};


/**
 * Manages the color scheme mode of the application based on the user's
 * preferred  color scheme. It initializes the color scheme based on the
 * user's preference, updates it when the user's preference changes, and
 * propagates the scheme mode to iframes within the application.
 */
export function schemeModeManager() {
    // Create a media query for detecting the user's preferred color scheme.
    const schemeModeEvent = window.matchMedia("(prefers-color-scheme: dark)");
    // Set the initial color scheme based on the user's preference.
    const schemeMode = getSchemeMode(schemeModeEvent);
    setSchemeMode(schemeMode);
    sendSchemeToIframes(schemeMode);

    // Add an event listener to track changes in the preferred color scheme.
    schemeModeEvent.addEventListener("change", event => {
        // When the color scheme preference changes, update the scheme mode.
        setSchemeMode(getSchemeMode(event));
    });
}


/**
 * Attaches an event handler to the click event of the mode-switching button
 * (light/dark). When the button is clicked, this function determines the
 * previous mode (light or dark), switches to the opposite mode, and sends a
 * message to all iframes on the page to inform them of the mode change.
 * Finally, it sets the new mode on the main document after a short delay.
 */
function sendSchemeToIframes(schemeMode) {
    const iframes = [...document.querySelectorAll(ELEMENT_IFRAME)];
    // Trigger scheme mode change for all iframes.
    iframes.forEach(iframe => {
        // Communicate theme changes to all the iframes.
        const message = () => iframe.contentWindow.postMessage(schemeMode);
        // When loading iframes and as soon as the function is called.
        iframe.addEventListener("load", () => message());
        message();
    });
}


/**
 * Adds an event listener to a scheme mode button, allowing users to manually
 * toggle between light and dark color schemes. When the button is clicked,
 * this function switches the color scheme between light and dark, updates the
 * interface, and propagates the scheme mode to iframes within the application.
 */
export function schemeModeButton() {
    document.querySelector(ELEMENT_SCHEME_MODE_BUTTON).addEventListener("click", () => {
        // Recover the previous scheme mode and take its opposite.
        const previousSchemeMode = document.documentElement.className;
        const schemeMode = previousSchemeMode === LIGHT ? DARK : LIGHT;
        setSchemeMode(schemeMode);  // Parent frame.
        sendSchemeToIframes(schemeMode);  // All iframes.
    });
}
