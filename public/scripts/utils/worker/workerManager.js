import { CONSOLE_OUTPUT_PARAGRAPH, CONSOLE_OUTPUT_TITLE } from "../constants/elements.js";
import { WORKER_FILE } from "../constants/values.js";


/**
 * Checks if a worker process is running based on the provided file name.
 * If "fileName" is provided, it calls the corresponding Eel function to check
 * if a process with that file name is running. If "fileName" is not provided,
 * it checks if any worker process is running.
 *
 * @param {string} fileName - The name of the worker process to check for (optional).
 * @param {Function} onMessage - Call a specific function on message.
 * @returns {Worker} The web worker instance for further interaction.
 */
export async function isWorkerRunning(fileName, onMessage) {
    // Check if "fileName" is provided, and based on that, call the
    // appropriate Eel function to check if a process is running.
    const isProcessRunning = fileName ?
        await eel.is_process_running(fileName)() :
        await eel.is_process_running()();

    // If "fileName" is provided and a process is running, start worker.
    if (fileName && onMessage && isProcessRunning)
        return startLogWorker(fileName, onMessage);
};


/**
 * Starts a web worker to process a log file and update the console output
 * on the web page.
 *
 * @param {string} logFileName - The name of the log file to be processed.
 * @param {Function} onMessage - Call a specific function on message.
 * @returns {Worker} The web worker instance for further interaction.
 */
export function startLogWorker(logFileName, onMessage) {
    // Create a new web worker instance using the specified worker file.
    const worker = new Worker(WORKER_FILE, { type: "module" });
    // Post a message to the worker with the log file name to
    worker.postMessage(logFileName); // initiate processing.

    // Find and display the console output title element on the web page.
    const consoleTitle = document.querySelector(CONSOLE_OUTPUT_TITLE);
    if (consoleTitle) consoleTitle.style.display = "none";
    // Find the console output paragraph element and remove its content.
    const consoleContainer = document.querySelector(CONSOLE_OUTPUT_PARAGRAPH);
    if (consoleContainer) consoleContainer.innerHTML = "";

    // Listen for messages from the worker when it"s done processing.
    worker.addEventListener("message", data => onMessage(data.data));
    return worker;  // Return the web worker instance for further interaction.
}


/**
 * Stops a web worker and resets the console output elements.
 * This function terminates the specified web worker (if provided) and resets
 * the visibility and content of console output elements on the web page.
 *
 * @param {Worker} worker - The web worker instance to terminate.
 */
export function stopLogWorker(worker) {
    // Find and display the console output title element on the web page.
    const consoleTitle = document.querySelector(CONSOLE_OUTPUT_TITLE);
    if (consoleTitle) consoleTitle.style.display = "";
    // Find the console output paragraph element and remove its content.
    const consoleContainer = document.querySelector(CONSOLE_OUTPUT_PARAGRAPH);
    if (consoleContainer) consoleContainer.innerHTML = "";
    if (worker) worker.terminate();
}
