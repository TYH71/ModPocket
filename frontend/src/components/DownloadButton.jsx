import React from 'react';
import { Download, RefreshCw } from 'lucide-react';
import { cn } from '../lib/utils';

const DownloadButton = ({ imageUrl, onReset }) => {
    const handleDownload = async () => {
        if (!imageUrl) return;

        try {
            const response = await fetch(imageUrl);
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `modpocket-wallpaper-${Date.now()}.png`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
        } catch (error) {
            // Fallback: open in new tab
            window.open(imageUrl, '_blank');
        }
    };

    return (
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-6">
            {/* Download button */}
            <button
                onClick={handleDownload}
                disabled={!imageUrl}
                className={cn(
                    "inline-flex items-center justify-center gap-2",
                    "px-6 py-3 rounded-xl font-medium",
                    "bg-gradient-to-r from-green-500 to-emerald-600",
                    "text-white shadow-lg",
                    "transition-all duration-300",
                    "hover:shadow-xl hover:shadow-green-500/30 hover:scale-105",
                    "disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                )}
            >
                <Download className="w-5 h-5" />
                <span>Download PNG</span>
            </button>

            {/* Generate another button */}
            <button
                onClick={onReset}
                className={cn(
                    "inline-flex items-center justify-center gap-2",
                    "px-6 py-3 rounded-xl font-medium",
                    "glass hover:bg-white/10",
                    "text-gray-300 hover:text-white",
                    "transition-all duration-300"
                )}
            >
                <RefreshCw className="w-5 h-5" />
                <span>Generate Another</span>
            </button>
        </div>
    );
};

export default DownloadButton;
