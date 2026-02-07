/**
 * Validates a NUSMods share URL
 * @param {string} url - The URL to validate
 * @returns {object} - { valid: boolean, error?: string }
 */
export const validateNusmodsUrl = (url) => {
    if (!url || url.trim() === '') {
        return { valid: false, error: 'Please paste your NUSMods link' };
    }

    const trimmedUrl = url.trim();

    // Check if it's a valid URL format
    try {
        new URL(trimmedUrl);
    } catch {
        return { valid: false, error: "That doesn't look like a valid URL" };
    }

    // Check if it's a NUSMods URL
    if (!trimmedUrl.startsWith('https://nusmods.com/')) {
        return { valid: false, error: 'Please use a link from nusmods.com' };
    }

    // Check if it's a timetable share URL
    const timetablePattern = /^https:\/\/nusmods\.com\/timetable\/sem-[12]\/share\?.+$/;
    if (!timetablePattern.test(trimmedUrl)) {
        return {
            valid: false,
            error: "That doesn't look like a timetable share link. Make sure you copy from the 'Share/Sync' button!"
        };
    }

    return { valid: true };
};

/**
 * Extracts module codes from a NUSMods URL
 * @param {string} url - The NUSMods URL
 * @returns {string[]} - Array of module codes
 */
export const extractModules = (url) => {
    try {
        const urlObj = new URL(url);
        const params = new URLSearchParams(urlObj.search);
        return Array.from(params.keys());
    } catch {
        return [];
    }
};

/**
 * Extracts semester from a NUSMods URL
 * @param {string} url - The NUSMods URL  
 * @returns {string} - Semester string (e.g., "sem-1", "sem-2")
 */
export const extractSemester = (url) => {
    const match = url.match(/\/timetable\/(sem-[12])\//);
    return match ? match[1] : 'unknown';
};
