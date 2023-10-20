// web/js/utils/informationManager.js

/**
 * @author: Pinterest Pinbuilder.
 * Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
 * Any distribution, modification or commercial use is strictly prohibited.
 */



import {
    CONTAINER_INFORMATION,
    CONTAINER_VERSION,
    ELEMENT_INFORMATION_BUTTON,
    ELEMENT_INFORMATION_CLOSE,
    ELEMENT_VERSION_TEXT
} from "./constants/elements.js";


/**
 * Displays information in a web page using DOM manipulation.
 *
 * This function retrieves and displays information when triggered by a button
 * click event. It hides or shows an information container, and fetches and
 * displays a tool version. Additionally, it listens for close button clicks
 * to hide the information container.
 */
export async function displayInformation() {
    const informationContainer = document.querySelector(CONTAINER_INFORMATION);
    const informationButton = document.querySelector(ELEMENT_INFORMATION_BUTTON);
    const informationCloseButton = document.querySelector(ELEMENT_INFORMATION_CLOSE);

    informationButton.addEventListener("click", () =>
        informationContainer.style.display = "");
    informationCloseButton.addEventListener("click", () =>
        informationContainer.style.display = "none");

    const versionContainer = document.querySelector(CONTAINER_VERSION);
    const version = await eel.get_tool_version()();
    if (!version) versionContainer.style.display = "none";

    const versionText = document.querySelector(ELEMENT_VERSION_TEXT);
    versionText.textContent = version;
}
