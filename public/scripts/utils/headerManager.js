import { DISABLED } from "./constants/attributes.js";
import { ELEMENT_HEADER, ELEMENT_IFRAME, ELEMENT_NAVIGATION_BUTTON, ICON } from "./constants/elements.js";
import { ICON_TO_PAGE } from "./constants/values.js";
import { changeVisibleIframe } from "./iframeManager.js";


/**
 * Sets the state of header buttons to control their interaction.
 *
 * @param {Element} selectedButton - The button that is currently selected.
 * @param {Array<Element>} selectableButtons - An array of header buttons
 * that can be selected.
 */
export function setHeaderButtonsState(selectedButton, selectableButtons) {
    // Enable unselected buttons, and disable the currently selected one.
    selectableButtons.forEach(button => button.removeAttribute(DISABLED));
    selectedButton.setAttribute(DISABLED, "true");
}


/**
 * Adds click event listeners to header buttons and manages the visibility
 * of associated iframes based on the clicked button's icon. When a button is
 * clicked, this function retrieves the corresponding page URL from a mapping,
 * makes the associated iframe visible, and sets the button as selected while
 * deselecting all other header buttons.
 */
export function editHeader() {
    const headerButtons = [...document.querySelectorAll(ELEMENT_NAVIGATION_BUTTON)];
    headerButtons.forEach(button => button.addEventListener("click", () => {
        // Retrieve the page name based on the current button icon,
        // and make the associated iframe visible.
        const buttonIcon = button.querySelector(ICON).innerHTML;
        const selectedPageURL = ICON_TO_PAGE[buttonIcon];
        changeVisibleIframe(selectedPageURL);
        const selectableButtons = // Retrieve all other unselected buttons.
            headerButtons.filter(_button => _button != button);
        // The current button is now selected (unreachable).
        setHeaderButtonsState(button, selectableButtons);
    }));
}


/**
 * Adjusts the height of a fixed header to accommodate changes in the
 * interface size. This function calculates the current height of the
 * header element and updates the margin-top property of specified iframes
 * to ensure they don't overlap with the header. It also adds a
 * ResizeObserver to continuously monitor changes in the header's size
 * and automatically adjust the header height accordingly.
 */
export function responsiveHeaderHeight() {
    const headerElement = document.querySelector(ELEMENT_HEADER);

    const editHeaderHeight = () => {
        const headerHeight = headerElement.offsetHeight;
        const iframes = [...document.querySelectorAll(ELEMENT_IFRAME)];
        iframes.forEach(iframe => iframe.style.marginTop = `${headerHeight}px`);
    }
    // Adds an interface size change observer to adjust the fixed header.
    new ResizeObserver(_ => editHeaderHeight()).observe(headerElement);
    editHeaderHeight();
}
