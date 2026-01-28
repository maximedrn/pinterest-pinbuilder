// web/js/common/stringToElement.js

/**
 * Convert a string representation of HTML into a DocumentFragment.
 *
 * @param {string} string - The HTML string to be converted.
 * @returns {DocumentFragment} - A DocumentFragment containing the DOM
 * elements parsed from the string.
 */
export function stringToElement(string) {
    // Create a new DocumentRange object and call createContextualFragment
    // on it, which parses the provided string as HTML and returns a
    // DocumentFragment.
    return document.createRange().createContextualFragment(string);
}
