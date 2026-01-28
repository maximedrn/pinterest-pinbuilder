import "../../common/format.js";
import { stringToElement } from "../../common/stringToElement.js";
import {
    CONSOLE_HTML_ELEMENT,
    CONSOLE_HTML_ELEMENT_BACKGROUND
} from "../constants/dom.js";
import { CONSOLE_OUTPUT_PARAGRAPH } from "../constants/elements.js";


/**
 * Display console outputs on a web page.
 *
 * This function takes an array of messages, parses them as JSON, and renders
 * them as HTML elements within a specified container on the web page. Each
 * message can have a title and an optional background color. The function
 * clears the existing content in the container before rendering the new
 * messages.
 *
 * @param {string} messages - A JSON string representing an array of messages
 * to be displayed.
 */
export function displayConsoleOutputs(messages) {
    messages = JSON.parse(messages).reverse();
    const consoleContainer = document.querySelector(CONSOLE_OUTPUT_PARAGRAPH);
    consoleContainer.innerHTML = "";

    messages.forEach(message => {
        const title = message?.title || "";
        const color = message?.color;
        const second_message = message?.second_message || "";
        const consoleLiteral = color ? CONSOLE_HTML_ELEMENT_BACKGROUND.format(
            color, title, message.message, second_message) :
            CONSOLE_HTML_ELEMENT.format(title, message.message, second_message);

        const consoleHtml = stringToElement(consoleLiteral);
        consoleContainer.appendChild(consoleHtml);
    });
}
