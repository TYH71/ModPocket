import React from 'react';
import { AlertTriangle, XCircle, RefreshCw } from 'lucide-react';
import { cn } from '../lib/utils';

const ErrorMessage = ({ error, onRetry }) => {
    if (!error) return null;

    return (
        <div className={cn(
            "w-full max-w-xl mx-auto mt-6 p-4 rounded-xl",
            "glass border-red-500/30",
            "animate-pulse"
        )}>
            <div className="flex items-start gap-3">
                {/* Error icon */}
                <div className="flex-shrink-0 mt-0.5">
                    <XCircle className="w-5 h-5 text-red-400" />
                </div>

                {/* Error content */}
                <div className="flex-1">
                    <h4 className="font-medium text-red-400 mb-1">
                        Something went wrong
                    </h4>
                    <p className="text-gray-400 text-sm">
                        {error}
                    </p>
                </div>

                {/* Retry button */}
                {onRetry && (
                    <button
                        onClick={onRetry}
                        className={cn(
                            "flex-shrink-0 p-2 rounded-lg",
                            "hover:bg-white/10 transition-colors",
                            "text-gray-400 hover:text-white"
                        )}
                        aria-label="Retry"
                    >
                        <RefreshCw className="w-4 h-4" />
                    </button>
                )}
            </div>

            {/* Help text */}
            <div className="flex items-center gap-2 mt-3 pt-3 border-t border-white/10">
                <AlertTriangle className="w-4 h-4 text-yellow-500" />
                <span className="text-xs text-gray-500">
                    Make sure your NUSMods link is from the "Share/Sync" button
                </span>
            </div>
        </div>
    );
};

export default ErrorMessage;
