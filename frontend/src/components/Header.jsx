import React from 'react';
import { Smartphone } from 'lucide-react';

const Header = () => {
    return (
        <header className="text-center mb-8 md:mb-12">
            {/* Logo */}
            <div className="inline-flex items-center justify-center w-16 h-16 md:w-20 md:h-20 rounded-2xl bg-gradient-to-br from-nus-orange to-orange-600 mb-4 shadow-lg glow-orange">
                <Smartphone className="w-8 h-8 md:w-10 md:h-10 text-white" />
            </div>

            {/* Title */}
            <h1 className="text-3xl md:text-5xl font-bold mb-2">
                <span className="gradient-text">ModPocket</span>
            </h1>

            {/* Tagline */}
            <p className="text-gray-400 text-base md:text-lg max-w-md mx-auto">
                Transform your NUSMods timetable into a stunning iPhone wallpaper
            </p>
        </header>
    );
};

export default Header;
