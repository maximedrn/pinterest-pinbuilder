// web/js/utils/constants/values.js

/**
 * @author: Pinterest Pinbuilder.
 * Copyright © 2023 Pinterest Pinbuilder. All rights reserved.
 * Any distribution, modification or commercial use is strictly prohibited.
 */


import {
    ELEMENT_ALTERNATIVE_TEXT_FIELD,
    ELEMENT_DATETIME_FIELD,
    ELEMENT_DESCRIPTION_FIELD,
    ELEMENT_LINK_FIELD,
    ELEMENT_PINBOARD_FIELD,
    ELEMENT_PIN_TYPE_TOGGLE,
    ELEMENT_TITLE_FIELD,
    ELEMENT_TOPIC_TAGS_FIELD
} from "./elements.js";



const FRONTEND_HOST = "http://localhost";
const FRONTEND_PORT = 8000;
export const FRONTEND_URL = `${FRONTEND_HOST}:${FRONTEND_PORT}`;
export const WORKER_FILE = `${FRONTEND_URL}/scripts/common/worker.js`;
export const FAVICON_PATH = "./assets/favicon-{}.png?v=2";

// File extensions.
const HTML = ".html"
const JSON = ".json"

// Page names.
const PROCESS = "process"
const CREATE = "create"
const SCRAPE = "scrape"

// Frontend HTML page names.
export const PROCESS_PAGE = PROCESS + HTML;
const CREATE_PAGE = CREATE + HTML;
const SCRAPE_PAGE = SCRAPE + HTML;

// Log files.
const UPLOAD = "upload"
const LOGIN = "login"
export const CREATE_FILE = CREATE + JSON;
export const UPLOAD_FILE = UPLOAD + JSON;
export const LOGIN_FILE = LOGIN + JSON;

// Header buttons' icon.
const PROCESS_PAGE_ICON = "article";
const CREATE_PAGE_ICON = "construction";
const SCRAPE_PAGE_ICON = "search";

export const ICON_TO_PAGE = {
    [CREATE_PAGE_ICON]: CREATE_PAGE,
    [PROCESS_PAGE_ICON]: PROCESS_PAGE,
    [SCRAPE_PAGE_ICON]: SCRAPE_PAGE
}

// Invert keys and values from `ICON_TO_PAGE`.
export const PAGE_TO_ICON = Object.fromEntries(
    Object.entries(ICON_TO_PAGE)
    .map(([key, value]) => [value, key]));

// Scheme mode values.
export const LIGHT = "light";
export const DARK = "dark";
export const SCHEME_MODES = [LIGHT, DARK];

// Field value checker.
export const EMPTY_VALUES = [
    "",
    null,
    NaN,
    undefined
];

// Pin data file keys and HTML elements.
export const TOPIC_TAGS = "topic_tags";
export const PAID_PIN = "paid_pin";
export const DATA_FILES_KEYS = {
    [PAID_PIN]: ELEMENT_PIN_TYPE_TOGGLE,
    pinboard: ELEMENT_PINBOARD_FIELD,
    title: ELEMENT_TITLE_FIELD,
    description: ELEMENT_DESCRIPTION_FIELD,
    alt_text: ELEMENT_ALTERNATIVE_TEXT_FIELD,
    link: ELEMENT_LINK_FIELD,
    [TOPIC_TAGS]: ELEMENT_TOPIC_TAGS_FIELD,
    datetime: ELEMENT_DATETIME_FIELD
};
export const UUID = "data-uuid";
export const DATA_FILE = "data-file";

export const FLATPICKR_FORMAT = "d/m/Y H:i";
export const MAXIMUM_SCHEDULE_DAYS = 14;
