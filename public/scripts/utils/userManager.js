// web/js/utils/userManager.js

/**
 * @author: Pinterest Pinbuilder.
 * Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
 * Any distribution, modification or commercial use is strictly prohibited.
 */


import "../common/format.js";
import { timeStampToDatetime } from "../common/datetime.js";
import { stringToElement } from "../common/stringToElement.js"
import { startLogWorker, stopLogWorker } from "./worker/workerManager.js";
import { displayConsoleOutputs } from "./worker/consoleManager.js";
import { displayMessage } from "../utils/worker/snackbarManager.js";
import { checkboxEvent } from "./checkboxManager.js";
import { ACCOUNT_HTML_ELEMENT } from "./constants/dom.js";
import { SELECTED } from "./constants/attributes.js";
import { LOGIN_FILE } from "./constants/values.js";
import {
    CONTAINER_ACCOUNTS,
    ELEMENT_ACCOUNT,
    ELEMENT_ADD_ACCOUNT_BUTTON,
    ELEMENT_LOGIN_BUTTON,
    ELEMENT_UPLOAD_BUTTON
} from "./constants/elements.js";


export class LoginManager {

    /**
     * Constructor for the LoginManager class.
     * Initialize a new instance of the LoginManager class.
     */
    constructor() {
        this.worker = null;
    }

    /**
     * Retrieves and displays a list of saved users on a web page.
     * 
     * This function fetches user data using the `retrieve_users_data`
     * function from the Eel backend. It then iterates through the user
     * data, formats it, and appends it to the HTML document.
     */
    async retrieveSavedUsers() {
        const usersList = await eel.retrieve_users_data()();
        const accountContainer = document.querySelector(CONTAINER_ACCOUNTS);
        
        // Remove all the account elements except the first one.
        const accountElements = [...accountContainer.children];
        accountElements.slice(1).forEach(accountElement => accountElement.remove());
        
        usersList.forEach(([username, uuid, image_url, timestamp]) => {
            const datetime = timeStampToDatetime(timestamp);
            const userElementString = ACCOUNT_HTML_ELEMENT.format(
                image_url, username, uuid, username, datetime);
    
            const userElement = stringToElement(userElementString);
            accountContainer.appendChild(userElement);
        });
        checkboxEvent(ELEMENT_ACCOUNT);
    }

    /**
     * Manage the login process, including starting and stopping login activities.
     */
    loginProcess() {
        // Get references to DOM elements.
        const addAccountButton = document.querySelector(ELEMENT_ADD_ACCOUNT_BUTTON);
        const loginButton = document.querySelector(ELEMENT_LOGIN_BUTTON);
        const uploadButton = document.querySelector(ELEMENT_UPLOAD_BUTTON);

        // Add a click event listener to the "Add Account" button.
        addAccountButton.addEventListener("click", async () => {
            // Highlight the "Login" button.
            loginButton.classList.add(SELECTED);
            loginButton.style.display = "";

            // Start the login process and check if it was successful.
            const [isStarted, error] = await eel.start_login_process()();
            if (!isStarted) {
                displayMessage(error);
                loginButton.style.display = "none";
                loginButton.classList.remove(SELECTED);
                return;
            }

            // Highlight the "Upload" button and set up worker for logging.
            uploadButton.classList.add(SELECTED);
            loginButton.classList.remove(SELECTED);
            this.worker = startLogWorker(
                LOGIN_FILE, (message) => displayConsoleOutputs(message));
        });

        // Add a click event listener to the "Login" button.
        loginButton.addEventListener("click", async () => {
            // Stop the login process, clean up, and retrieve saved user data.
            await eel.stop_login_process()();
            loginButton.style.display = "none";
            loginButton.classList.remove(SELECTED);
            uploadButton.classList.remove(SELECTED);
            stopLogWorker(this.worker);
            await this.retrieveSavedUsers();
        });
    }
}
