import { DISABLED, UNREACHABLE } from "../utils/constants/attributes.js";


/**
 * Enable or disable a DOM element and modify its class based on its 
 * reachability.
 *
 * @param {HTMLElement} nodeElement - The DOM element to be modified.
 * @param {boolean} isReachable - A flag indicating whether the element
 * should be reachable (true) or not (false).
 */
export function reachableElement(nodeElement, isReachable) {
    if (isReachable) {  // Remove the "disabled" attribute and
        // the "UNREACHABLE_CLASS" from the element's class list.
        nodeElement.removeAttribute(DISABLED);
        nodeElement.classList.remove(UNREACHABLE);
    } else {  // Add the "DISABLED" attribute and
        // the "UNREACHABLE" class to the element's class list.
        nodeElement.setAttribute(DISABLED, "");
        nodeElement.classList.add(UNREACHABLE);
        // If the element has no other classes, remove all classes.
        if (![...nodeElement.classList]) nodeElement.removeAttribute("class");
    }
}
