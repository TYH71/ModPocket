import React from 'react';
import { Link2, X, AlertCircle } from 'lucide-react';
import { cn } from '../lib/utils';

const LinkInput = ({ value, onChange, error, disabled }) => {
    const handleClear = () => {
        onChange('');
    };

    return (
        <div className="w-full max-w-xl mx-auto mb-6">
            <div className="relative">
                {/* Input container with glass effect */}
                <div className={cn(
                    "glass rounded-xl overflow-hidden transition-all duration-300",
                    error ? "border-red-500/50 shadow-red-500/20 shadow-lg" : "hover:border-nus-orange/30",
                    disabled && "opacity-50 cursor-not-allowed"
                )}>
                    {/* Icon */}
                    <div className="absolute left-4 top-1/2 -translate-y-1/2">
                        <Link2 className="w-5 h-5 text-gray-400" />
                    </div>

                    {/* Input */}
                    <input
                        type="url"
                        value={value}
                        onChange={(e) => onChange(e.target.value)}
                        placeholder="Paste your NUSMods share link here..."
                        disabled={disabled}
                        className={cn(
                            "w-full bg-transparent text-white placeholder-gray-500",
                            "py-4 pl-12 pr-12 text-base md:text-lg",
                            "focus:outline-none focus:ring-0",
                            "transition-all duration-200",
                            disabled && "cursor-not-allowed"
                        )}
                    />

                    {/* Clear button */}
                    {value && !disabled && (
                        <button
                            onClick={handleClear}
                            className="absolute right-4 top-1/2 -translate-y-1/2 p-1 rounded-full hover:bg-white/10 transition-colors"
                            aria-label="Clear input"
                        >
                            <X className="w-4 h-4 text-gray-400 hover:text-white" />
                        </button>
                    )}
                </div>
            </div>

            {/* Error message */}
            {error && (
                <div className="flex items-center gap-2 mt-3 text-red-400 text-sm animate-pulse">
                    <AlertCircle className="w-4 h-4 flex-shrink-0" />
                    <span>{error}</span>
                </div>
            )}

            {/* Helper text */}
            {!error && (
                <p className="mt-3 text-gray-500 text-sm text-center">
                    Go to NUSMods → Click "Share/Sync" → Copy the link
                </p>
            )}
        </div>
    );
};

export default LinkInput;
