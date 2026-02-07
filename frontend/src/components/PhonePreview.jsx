import React from 'react';
import { ImageIcon } from 'lucide-react';

const PhonePreview = ({ imageUrl, loading }) => {
    return (
        <div className="flex flex-col items-center">
            {/* iPhone frame */}
            <div className="relative">
                {/* Phone outer frame */}
                <div className="relative w-[200px] md:w-[240px] h-[420px] md:h-[500px] rounded-[36px] bg-gradient-to-b from-gray-700 to-gray-900 p-1.5 shadow-2xl">
                    {/* Phone inner bezel */}
                    <div className="w-full h-full rounded-[32px] bg-black overflow-hidden relative">
                        {/* Dynamic Island */}
                        <div className="absolute top-3 left-1/2 -translate-x-1/2 w-24 h-6 bg-black rounded-full z-10" />

                        {/* Screen content */}
                        <div className="w-full h-full bg-gradient-to-b from-gray-900 to-gray-950 flex items-center justify-center">
                            {imageUrl ? (
                                <img
                                    src={imageUrl}
                                    alt="Generated wallpaper preview"
                                    className="w-full h-full object-cover"
                                />
                            ) : (
                                <div className="flex flex-col items-center text-gray-600">
                                    <ImageIcon className="w-12 h-12 mb-3 opacity-50" />
                                    <span className="text-sm">
                                        {loading ? 'Loading...' : 'Preview will appear here'}
                                    </span>
                                </div>
                            )}
                        </div>

                        {/* Home indicator */}
                        <div className="absolute bottom-2 left-1/2 -translate-x-1/2 w-24 h-1 bg-white/30 rounded-full" />
                    </div>
                </div>

                {/* Reflection effect */}
                <div className="absolute -inset-4 bg-gradient-to-tr from-nus-orange/5 via-transparent to-transparent rounded-[44px] pointer-events-none" />
            </div>

            {/* Device label */}
            <p className="mt-4 text-gray-500 text-sm">
                iPhone 14/15 Pro Preview
            </p>
        </div>
    );
};

export default PhonePreview;
