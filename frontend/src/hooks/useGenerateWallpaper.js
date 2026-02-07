import { useState, useCallback } from 'react';

// API configuration - update this with your backend URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Custom hook for generating wallpapers via the backend API
 */
export const useGenerateWallpaper = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);
    const [metadata, setMetadata] = useState(null);

    /**
     * Generate a wallpaper
     * @param {string} nusmodsUrl - The NUSMods share URL
     * @param {Object} options - Customization options
     * @param {string} options.aspectRatio - Device/aspect ratio ID
     * @param {string} options.designStyle - Design style ID
     * @param {string} options.theme - 'light' or 'dark'
     */
    const generate = useCallback(async (nusmodsUrl, options = {}) => {
        setLoading(true);
        setError(null);
        setImageUrl(null);
        setMetadata(null);

        const { aspectRatio = 'iphone-14-pro', designStyle = 'minimalist', theme = 'dark' } = options;

        try {
            const response = await fetch(`${API_BASE_URL}/api/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    nusmods_url: nusmodsUrl,
                    aspect_ratio: aspectRatio,
                    design_style: designStyle,
                    theme: theme,
                }),
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Failed to generate wallpaper');
            }

            setImageUrl(data.image_url);
            setMetadata({
                ...data.metadata,
                aspectRatio,
                designStyle,
                theme,
            });
            return { success: true, imageUrl: data.image_url };
        } catch (err) {
            const errorMessage = err.message === 'Failed to fetch'
                ? 'Unable to connect to the server. Please check your internet connection.'
                : err.message;
            setError(errorMessage);
            return { success: false, error: errorMessage };
        } finally {
            setLoading(false);
        }
    }, []);

    const reset = useCallback(() => {
        setLoading(false);
        setError(null);
        setImageUrl(null);
        setMetadata(null);
    }, []);

    return {
        generate,
        reset,
        loading,
        error,
        imageUrl,
        metadata,
    };
};
