// web/js/utils/checkboxManager.js

/**
 * @author: Pinterest Pinbuilder.
 * Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
 * Any distribution, modification or commercial use is strictly prohibited.
 */


import { CHECKED } from "./constants/attributes.js";


/**
 * Attach a click event listener to checkboxes and manage their state.
 *
 * @param {string} domElements - CSS selector for the checkbox elements.
 * @param {Function} callable - Optional callback function to execute on
 * checkbox click.
 */
export function checkboxEvent(domElements, callable) {
    // Select all elements matching the provided CSS selector.
    const elements = [...document.querySelectorAll(domElements)];
    // Add a click event listener to each element.
    elements.forEach(element => element.addEventListener("click", () => {
        // Toggle the "CHECKED" class based on its presence.
        [...element.classList].includes(CHECKED) ? element
            .classList.remove(CHECKED) : element.classList.add(CHECKED);
        // If a callback function is provided, execute it.
        if (callable) callable();
        // Uncheck other checkboxes within the same group.
        elements.filter(selectableFile => selectableFile !== element).forEach(
            selectableFile => selectableFile.classList.remove(CHECKED));
    }));
}
