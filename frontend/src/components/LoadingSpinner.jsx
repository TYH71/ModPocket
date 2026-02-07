import React from 'react';
import { Loader2 } from 'lucide-react';

const LoadingSpinner = ({ message = 'Generating your wallpaper...' }) => {
    return (
        <div className="flex flex-col items-center justify-center py-12">
            {/* Spinner container */}
            <div className="relative">
                {/* Outer ring */}
                <div className="w-20 h-20 rounded-full border-4 border-nus-orange/20" />

                {/* Spinning ring */}
                <div className="absolute inset-0 w-20 h-20 rounded-full border-4 border-transparent border-t-nus-orange animate-spin" />

                {/* Center icon */}
                <div className="absolute inset-0 flex items-center justify-center">
                    <Loader2 className="w-8 h-8 text-nus-orange animate-spin-slow" />
                </div>
            </div>

            {/* Loading message */}
            <p className="mt-6 text-gray-400 text-center animate-pulse">
                {message}
            </p>

            {/* Progress dots */}
            <div className="flex gap-1.5 mt-4">
                {[0, 1, 2].map((i) => (
                    <div
                        key={i}
                        className="w-2 h-2 rounded-full bg-nus-orange"
                        style={{
                            animation: 'pulse 1.5s ease-in-out infinite',
                            animationDelay: `${i * 0.2}s`,
                        }}
                    />
                ))}
            </div>
        </div>
    );
};

export default LoadingSpinner;
