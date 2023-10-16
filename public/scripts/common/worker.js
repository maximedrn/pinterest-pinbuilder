// web/js/common/worker.js

/**
@author: Pinterest Pinbuilder.

Telegram: https://t.me/maximedrn

Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
Any distribution, modification or commercial use is strictly prohibited.
*/


import { FRONTEND_URL } from "../utils/constants/values.js";


let content = "";


/**
 * Initializes a web worker that periodically fetches log data from a 
 * specified URL and sends updates to the main thread when new data
 * is available.
 *
 * @param {string} fileName - The name of the log file to fetch.
 */
const worker = (fileName) => {
    const url = `${FRONTEND_URL}/logs/${fileName}`;

    /**
     * Periodically checks for updates in the log file content and sends
     * updates to the main thread when new data is available.
     */
    const checkAndUpdateContent = () => {
        const request = new XMLHttpRequest();
        request.open("GET", url, true);
        request.send();

        request.onreadystatechange = () => {
            if (request.readyState === 4 && request.status === 200) {
                const result = request.responseText;
                if (content === result) return;

                content = result;
                if (content) self.postMessage(content);
            }
        };
    };

    // Set up a periodic timer to check and update content every second.
    setInterval(checkAndUpdateContent, 1000);
};


/**
 * Event listener for messages from the main thread. Starts the worker with
 * the specified log file name when a message is received.
 *
 * @param {Event} event - The message event from the main thread.
 */
self.addEventListener("message", (event) => {
    worker(event.data);
});

