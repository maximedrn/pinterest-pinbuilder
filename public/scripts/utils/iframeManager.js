// web/js/utils/iframeManager.js

/**
 * @author: Pinterest Pinbuilder.
 * Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
 * Any distribution, modification or commercial use is strictly prohibited.
 */


import "../common/format.js";
import { defined } from "../common/defined.js";
import { setHeaderButtonsState } from "./headerManager.js";
import { PAGE_TO_ICON, PROCESS_PAGE } from "./constants/values.js";
import {
    ELEMENT_NAVIGATION_BUTTON,
    ICON,
    ELEMENT_IFRAME,
    ELEMENT_IFRAME_SOURCE
} from "./constants/elements.js";


/**
 * Changes the visibility of iframes based on the provided iframe URL.
 * This function iterates through all iframes on the page and displays
 * the one that matches the given URL, while hiding all others. It also
 * updates the parent URL hash to reflect the selected iframe's URL.
 *
 * @param {string} iframeURL - The URL of the iframe to be displayed.
 */
export function changeVisibleIframe(iframeURL) {
    // Get all the current iframes and check for the one that
    // matches with the URL in parameters.
    const iframes = [...document.querySelectorAll(ELEMENT_IFRAME)];
    iframes.forEach(iframe => {
        // Display the selected iframe according to the URL.
        iframe.src.includes(iframeURL) ?
            iframe.style.display = "" :
            iframe.style.display = "none";
    });
    // Add the hash in the parent URL in case of reload.
    parent.location.hash = iframeURL;
}


/**
 * Loads the previous iframe based on the page hash and updates the
 * visibility of the iframe. Additionally, it changes the state of header
 * buttons to reflect the loaded iframe's selection.
 */
export function loadPreviousIframe() {
    // Retrieve the previous loaded iframe and make it visible.
    const pageHash = parent.location.hash.slice(1);
    const iframeURL = defined(pageHash) ? pageHash : PROCESS_PAGE;
    const iframePath = ELEMENT_IFRAME_SOURCE.format(iframeURL);
    changeVisibleIframe(iframeURL);

    // Change the header buttons state according to the loaded and
    // selected iframe, it depends on the clicked header button.
    const iframe =  document.querySelector(iframePath);
    const headerButtons = [...document.querySelectorAll(ELEMENT_NAVIGATION_BUTTON)];
    iframe.addEventListener("load", () => headerButtons.forEach(button => {
        // Retrieves the current icon and the icon associated with the
        const correctIcon = PAGE_TO_ICON[iframeURL];  // iframe URL.
        const buttonIcon = button.querySelector(ICON).innerHTML;
        // Now that the correct header is loaded, make sure the
        // icon that loads this iframe is also selected.
        if (buttonIcon === correctIcon)
            setHeaderButtonsState(button, headerButtons);
    }));
}
