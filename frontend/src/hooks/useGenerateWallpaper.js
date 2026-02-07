import { useState, useCallback } from 'react';

// Backend API endpoint
const API_URL = 'https://generate-wallpaper-bj6vohqe7a-as.a.run.app';

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
     * @param {string} options.aspectRatio - Aspect ratio string (e.g., "9:19.5")
     * @param {string} options.designStyle - Design style ID
     * @param {string} options.theme - 'light' or 'dark'
     */
    const generate = useCallback(async (nusmodsUrl, options = {}) => {
        setLoading(true);
        setError(null);
        setImageUrl(null);
        setMetadata(null);

        const { aspectRatio = '9:19.5', designStyle = 'minimalist', theme = 'dark' } = options;

        try {
            const response = await fetch(API_URL, {
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

            // Convert base64 to data URL for image display
            const imageDataUrl = `data:image/png;base64,${data.image_base64}`;

            setImageUrl(imageDataUrl);
            setMetadata({
                modules: data.modules || [],
                aspectRatio,
                designStyle,
                theme,
            });
            return { success: true, imageUrl: imageDataUrl };
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
