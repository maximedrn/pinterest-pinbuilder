import "../common/format.js";
import { reachableElement } from "../common/reachableElement.js";
import { stringToElement } from "../common/stringToElement.js";
import { TAG_LIST_HTML_ELEMENT, TOPIC_TAG_HTML_ELEMENT } from "./constants/dom.js";
import {
    CONTAINER_TOPIC_TAGS,
    CONTAINER_TOPIC_TAGS_LIST,
    ELEMENT_SELECTED_TOPIC_TAGS,
    ELEMENT_TOPIC_TAGS,
    ELEMENT_TOPIC_TAGS_FIELD,
    ICON
} from "./constants/elements.js";


/**
 * TagManager class for managing topic tags in a web application.
 */
export class TagManager {

    /**
     * Check if a topic tag with a specific ID is selected.
     *
     * @param {string} tagId - The ID of the topic tag to check.
     * @returns {Element | null} - The selected topic tag or null if not selected.
     */
    #isTagSelected(tagId) {
        const selectedTagId = ELEMENT_SELECTED_TOPIC_TAGS.format(tagId);
        const selectedTag = document.querySelector(selectedTagId);
        return selectedTag;
    }

    /**
     * Add a selected topic tag to the list of selected tags.
     *
     * @param {Object} tag - The topic tag object to add.
     */
    #addTag(tag) {
        const tagsContainer = document.querySelector(CONTAINER_TOPIC_TAGS);
        const selectedTagString = TOPIC_TAG_HTML_ELEMENT.format(
            tag.id, tag.value, tag.tagValue, tag.tagValue);
        const selectedTagHtml = stringToElement(selectedTagString);
        tagsContainer.appendChild(selectedTagHtml);

        const selectedTagId = ELEMENT_SELECTED_TOPIC_TAGS.format(tag.id);
        const selectedTag = document.querySelector(selectedTagId);

        const selectedTagRemoveButton = selectedTag.querySelector(ICON);
        selectedTagRemoveButton.addEventListener("click", () => selectedTag.remove());
    }

    /**
     * Get a list of currently selected topic tags.
     *
     * @returns {Array} - An array of topic tags with id, value, and tagValue
     * properties.
     */
    _getTopicTags() {
        const tagsListContainer = document.querySelector(CONTAINER_TOPIC_TAGS);
        const topicTagElements = [...tagsListContainer.children];
        let topicTags = [];

        for (let tagElement of topicTagElements) topicTags.push({
            id: tagElement.getAttribute("data-id"),
            value: tagElement.getAttribute("data-value"),
            tagValue: tagElement.getAttribute("data-tag-value")
        });
        return topicTags;
    }

    /**
     * Set the list of selected topic tags.
     *
     * @param {Array} topicTags - An array of topic tags to set as selected.
     */
    _setTopicTags(topicTags) {
        if (!topicTags) return;
        this._emptySelectedTopicTags();
        const tagsField = document.querySelector(ELEMENT_TOPIC_TAGS_FIELD);
        tagsField.value = ""; // Empty the search input to remove string object.
        topicTags.forEach(tag => this.#addTag(tag));
    }

    /**
     * Empty the list of topic tags.
     */
    _emptyTopicTagsList() {
        const tagsListContainer = document.querySelector(CONTAINER_TOPIC_TAGS_LIST);
        tagsListContainer.innerHTML = "";
    }

    /**
     * Empty the list of selected topic tags.
     */
    _emptySelectedTopicTags() {
        const tagsListContainer = document.querySelector(CONTAINER_TOPIC_TAGS);
        tagsListContainer.innerHTML = "";
    }

    /**
     * Retrieve and manage tags based on user input.
     */
    async _retrieveTags() {
        const tagsField = document.querySelector(ELEMENT_TOPIC_TAGS_FIELD);
        const tagsListContainer = document.querySelector(CONTAINER_TOPIC_TAGS_LIST);

        tagsField.addEventListener("input", async (event) => {
            // Empty the dropdown when typing and before adding elements.
            this._emptyTopicTagsList();

            if (!event.target.value) return;
            const tags = await eel.search_for_tags(event.target.value)();
            this._emptyTopicTagsList();

            for (let tag of tags) {
                // Create the tag element to add to the dropdown.
                const tagElementString = TAG_LIST_HTML_ELEMENT.format(
                    tag.id, tag.value, tag.tagValue, tag.tagValue, tag.value);
                const tagElementHtml = stringToElement(tagElementString);
                tagsListContainer.appendChild(tagElementHtml);

                const tagElementId = ELEMENT_TOPIC_TAGS.format(tag.id);
                const tagElement = document.querySelector(tagElementId);

                // Disable the element if it is already selected.
                if (this.#isTagSelected(tag.id)) reachableElement(tagElement, false);

                // Verify that the element has not been removed from the list.
                // If so, enable it back, else let it disabled.
                tagsField.addEventListener("click", () => {
                    if (!this.#isTagSelected(tag.id))
                        reachableElement(tagElement, true);
                });

                // Add the selected tag to the list.
                tagElement.addEventListener("click", () => {
                    // Remove the content of the dropdown and the input.
                    this._emptyTopicTagsList();
                    tagsField.value = "";
                    this.#addTag(tag);
                });
            }
        });
    }
}
