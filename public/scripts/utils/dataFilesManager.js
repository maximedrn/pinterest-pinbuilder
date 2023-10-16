// web/js/utils/dataFilesManager.js

/**
 * @author: Pinterest Pinbuilder.
 * Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
 * Any distribution, modification or commercial use is strictly prohibited.
 */


import "../common/format.js";
import { stringToElement } from "../common/stringToElement.js";
import { checkboxEvent } from "./checkboxManager.js";
import { DATA_FILE_HTML_ELEMENT } from "./constants/dom.js";
import { CHECKED } from "./constants/attributes.js";
import {
    CONTAINER_DATA_FILES,
    ELEMENT_DATA_FILE,
    ELEMENT_BROWSED_DATA_FILE_CLEAR,
    ELEMENT_BROWSED_DATA_FILE_BUTTON,
    CONTAINER_BROWSED_DATA_FILE_TEXT,
    ELEMENT_BROWSED_DATA_FILE_TEXT,
    ELEMENT_DATA_FILE_RELOAD,
    CONTAINER_SELECTED_FILE
} from "../utils/constants/elements.js";
import { DATA_FILE } from "./constants/values.js";


/**
 * Display files from a data folder on the web page.
 * This function retrieves a list of data files from the data folder using
 * Eel, generates HTML elements for each file, and appends them to a specified
 * container. If no files are found, it does nothing.
 *
 * @async
 * @function displayFilesFromDataFolder
 */
export async function displayFilesFromDataFolder() {
    // Call the "retrieve_files_from_data_folder" function using Eel.
    const dataFilesArray = await eel.retrieve_files_from_data_folder()();
    // Check if the "dataFilesArray" is empty (has a length of 0).
    if (!dataFilesArray.length) return;

    // Find the HTML element that will contain the data files.
    let dataFilesContainer = document.querySelector(CONTAINER_DATA_FILES);
    dataFilesArray.forEach(dataFile => {
        // Parse the data file template with the data file path.
        let dataFileElement = DATA_FILE_HTML_ELEMENT.format(dataFile, dataFile);
        // Convert from a string to an element and append it to the DOM.
        dataFilesContainer.appendChild(stringToElement(dataFileElement));
    });
}


/**
 * Unselect a browsed data file and hide its display container on the web
 * page. This function clears the selected data file path from a container
 * element and hides the container, effectively unselecting the data file.
 *
 * @function unselectBrowsedDataFile
 */
export function unselectBrowsedDataFile() {
    const unselectFile = () => {
        // Find the path element of browsed data file container element.
        const browsedDataFileContainerPath = document
            .querySelector(CONTAINER_BROWSED_DATA_FILE_TEXT);
        const browsedDataFileContainerSpan = 
            [...document.querySelectorAll(ELEMENT_BROWSED_DATA_FILE_TEXT)];
        // Set the inner HTML of path element to empty.
        browsedDataFileContainerSpan.forEach(span => {
            span.innerHTML = "";
            span.removeAttribute(DATA_FILE);
        });
        // Hide the browsed data file container.
        browsedDataFileContainerPath.style.display = "none";
    }

    // Find the browsed data file container element.
    const browseDataFileClearButton = document
        .querySelector(ELEMENT_BROWSED_DATA_FILE_CLEAR);
    browseDataFileClearButton.addEventListener("click", () => unselectFile());
    unselectFile();
}


/**
 * Browse for a data file using Eel and display the selected file path on the
 * web page. This function opens a file dialog using Eel, retrieves the
 * selected file path, and displays it in a specified container element on
 * the web page. If no file is selected, it does nothing.
 *
 * @function browseDataFile
 */
export function browseDataFile() {
    // Find the browsed data file container element.
    const browsedDataFileContainer = document
        .querySelector(ELEMENT_BROWSED_DATA_FILE_BUTTON);
    browsedDataFileContainer.addEventListener("click", async () => {
        // Call the "browse_file" function using Eel.
        const browsedDataFilePath = await eel.browse_file()();
        // Check if no file path is returned (empty or falsy value).
        if (!browsedDataFilePath) return;

        // Find the path element of browsed data file container element.
        const browsedDataFileContainerSpan = document
            .querySelector(ELEMENT_BROWSED_DATA_FILE_TEXT);
        // Set the inner HTML of path element to the selected file path.
        browsedDataFileContainerSpan.innerHTML = browsedDataFilePath;
        browsedDataFileContainerSpan.setAttribute(DATA_FILE, browsedDataFilePath);
        // Display the browsed data file container (make it visible).
        document.querySelector(CONTAINER_BROWSED_DATA_FILE_TEXT)
            .style.removeProperty("display");

        const previousSelectedFile = document.querySelector(CONTAINER_SELECTED_FILE);
        if (previousSelectedFile) previousSelectedFile.classList.remove(CHECKED);
    });
}


export function dataFileSelection() {
    checkboxEvent(ELEMENT_DATA_FILE, unselectBrowsedDataFile);
}


export function reloadDataFilesList() {
    const reloadButton = document.querySelector(ELEMENT_DATA_FILE_RELOAD);
    reloadButton.addEventListener("click", async () => {
        const filesListElement = document.querySelector(CONTAINER_DATA_FILES);
        const filesToRemove = [...filesListElement.children].slice(2);
        filesToRemove.forEach(file => filesListElement.removeChild(file));

        await displayFilesFromDataFolder();
        dataFileSelection();
    });
}