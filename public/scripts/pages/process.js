// web/js/pages/process.js

/**
 * @author: Pinterest Pinbuilder.
 * Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
 * Any distribution, modification or commercial use is strictly prohibited.
 */


import {
    browseDataFile,
    dataFileSelection,
    displayFilesFromDataFolder,
    reloadDataFilesList
} from "../utils/dataFilesManager.js";
import { setSchemeMode } from "../utils/schemeManager.js";
import { isWorkerRunning } from "../utils/worker/workerManager.js";
import { noTranslate } from "../common/noTranslate.js";
import { UploadManager } from "../utils/uploadManager.js";
import { LoginManager } from "../utils/userManager.js";
import { displayConsoleOutputs } from "../utils/worker/consoleManager.js";
import { UPLOAD_FILE, SCHEME_MODES } from "../utils/constants/values.js";
import { START_TEXT, STOP_TEXT } from "../utils/constants/texts.js";
import { PROCESS_STARTED } from "../utils/constants/attributes.js";
import {
    ELEMENT_UPLOAD_BUTTON,
    ELEMENT_UPLOAD_BUTTON_TEXT
} from "../utils/constants/elements.js";


window.addEventListener("DOMContentLoaded", async () => {
    window.addEventListener("message", event => { // Scheme mode manager.
        if (SCHEME_MODES.includes(event.data)) setSchemeMode(event.data);
    }, false);

    // Process and worker manager.
    await eel.stop_login_process()();
    const worker = await isWorkerRunning(
        UPLOAD_FILE, (message) => displayConsoleOutputs(message));
    
    const uploadButton = document.querySelector(ELEMENT_UPLOAD_BUTTON);
    const uploadButtonText = document.querySelector(ELEMENT_UPLOAD_BUTTON_TEXT);
    uploadButtonText.textContent = worker ? STOP_TEXT : START_TEXT;
    if (worker) uploadButton.classList.add(PROCESS_STARTED);

    noTranslate(); // Icon translation.
    // Data files manager.
    await displayFilesFromDataFolder();
    reloadDataFilesList();
    dataFileSelection();
    browseDataFile();

    // Upload process manager.
    const uploadManager = new UploadManager;
    uploadManager.worker = worker;
    uploadManager.uploadProcess();

    // Login process manager.
    const loginManager = new LoginManager;
    loginManager.loginProcess();
    await loginManager.retrieveSavedUsers(); // Accounts.
});