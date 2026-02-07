import React from 'react';
import { Sparkles, Loader2 } from 'lucide-react';
import { cn } from '../lib/utils';

const GenerateButton = ({ onClick, loading, disabled }) => {
    return (
        <button
            onClick={onClick}
            disabled={disabled || loading}
            className={cn(
                "group relative inline-flex items-center justify-center gap-3",
                "px-8 py-4 rounded-xl font-semibold text-lg",
                "bg-gradient-to-r from-nus-orange to-orange-600",
                "text-white shadow-lg",
                "transition-all duration-300 ease-out",
                "hover:shadow-xl hover:shadow-nus-orange/30",
                "hover:scale-105 active:scale-100",
                "disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100",
                loading && "animate-pulse-glow"
            )}
        >
            {/* Background glow effect */}
            <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-nus-orange to-orange-600 opacity-0 group-hover:opacity-30 blur-xl transition-opacity duration-300" />

            {/* Icon */}
            {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
                <Sparkles className="w-5 h-5 transition-transform group-hover:rotate-12" />
            )}

            {/* Text */}
            <span className="relative">
                {loading ? 'Generating...' : 'Generate Wallpaper'}
            </span>
        </button>
    );
};

export default GenerateButton;
