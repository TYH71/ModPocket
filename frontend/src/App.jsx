import React, { useState, useCallback } from 'react';
import { Sparkles, ArrowRight, Link2, Loader2, Download, RotateCcw, ImageIcon, AlertCircle, Github, ChevronDown, Smartphone, Palette, Sun, Moon } from 'lucide-react';
import { validateNusmodsUrl, extractModules } from './utils/validateNusmodsUrl';
import { useGenerateWallpaper } from './hooks/useGenerateWallpaper';

// Aspect ratio options
const ASPECT_RATIOS = [
    { id: 'iphone-14-pro', label: 'iPhone 14/15 Pro', value: '1179x2556' },
    { id: 'iphone-14-pro-max', label: 'iPhone 14/15 Pro Max', value: '1290x2796' },
    { id: 'iphone-se', label: 'iPhone SE', value: '750x1334' },
    { id: 'iphone-14', label: 'iPhone 14/15', value: '1170x2532' },
    { id: 'android-1080p', label: 'Android (1080p)', value: '1080x2400' },
];

// Design style options
const DESIGN_STYLES = [
    { id: 'minimalist', label: 'Minimalist', description: 'Clean & simple' },
    { id: 'gradient', label: 'Gradient', description: 'Vibrant colors' },
    { id: 'neon', label: 'Neon', description: 'Glowing accents' },
    { id: 'pastel', label: 'Pastel', description: 'Soft tones' },
    { id: 'glassmorphism', label: 'Glass', description: 'Frosted effect' },
    { id: 'retro', label: 'Retro', description: 'Vintage vibes' },
];

// Custom Select Component
const Select = ({ value, onChange, options, icon: Icon, label }) => {
    const [isOpen, setIsOpen] = useState(false);
    const selectedOption = options.find(opt => opt.id === value);

    return (
        <div className="relative">
            <label className="block text-xs text-[hsl(var(--muted-foreground))] mb-1.5">{label}</label>
            <button
                type="button"
                onClick={() => setIsOpen(!isOpen)}
                className="w-full flex items-center justify-between gap-2 px-3 py-2.5 bg-[hsl(var(--secondary))] border border-[hsl(var(--border))] rounded-lg text-sm text-left hover:border-[hsl(var(--muted-foreground))] transition-colors"
            >
                <div className="flex items-center gap-2">
                    {Icon && <Icon className="w-4 h-4 text-[hsl(var(--muted-foreground))]" />}
                    <span>{selectedOption?.label || 'Select...'}</span>
                </div>
                <ChevronDown className={`w-4 h-4 text-[hsl(var(--muted-foreground))] transition-transform ${isOpen ? 'rotate-180' : ''}`} />
            </button>

            {isOpen && (
                <>
                    <div className="fixed inset-0 z-40" onClick={() => setIsOpen(false)} />
                    <div className="absolute z-50 w-full mt-1 py-1 bg-[hsl(var(--background))] border border-[hsl(var(--border))] rounded-lg shadow-xl max-h-48 overflow-y-auto">
                        {options.map((option) => (
                            <button
                                key={option.id}
                                onClick={() => {
                                    onChange(option.id);
                                    setIsOpen(false);
                                }}
                                className={`w-full px-3 py-2 text-sm text-left hover:bg-[hsl(var(--accent))] flex items-center justify-between ${value === option.id ? 'text-orange-400' : ''
                                    }`}
                            >
                                <span>{option.label}</span>
                                {option.description && (
                                    <span className="text-xs text-[hsl(var(--muted-foreground))]">{option.description}</span>
                                )}
                            </button>
                        ))}
                    </div>
                </>
            )}
        </div>
    );
};

// Theme Toggle Component
const ThemeToggle = ({ value, onChange }) => {
    return (
        <div>
            <label className="block text-xs text-[hsl(var(--muted-foreground))] mb-1.5">Theme</label>
            <div className="flex bg-[hsl(var(--secondary))] border border-[hsl(var(--border))] rounded-lg p-1">
                <button
                    type="button"
                    onClick={() => onChange('light')}
                    className={`flex-1 flex items-center justify-center gap-1.5 py-2 px-3 rounded-md text-sm transition-all ${value === 'light'
                            ? 'bg-white text-black'
                            : 'text-[hsl(var(--muted-foreground))] hover:text-white'
                        }`}
                >
                    <Sun className="w-4 h-4" />
                    Light
                </button>
                <button
                    type="button"
                    onClick={() => onChange('dark')}
                    className={`flex-1 flex items-center justify-center gap-1.5 py-2 px-3 rounded-md text-sm transition-all ${value === 'dark'
                            ? 'bg-[hsl(var(--foreground))] text-[hsl(var(--background))]'
                            : 'text-[hsl(var(--muted-foreground))] hover:text-white'
                        }`}
                >
                    <Moon className="w-4 h-4" />
                    Dark
                </button>
            </div>
        </div>
    );
};

function App() {
    const [url, setUrl] = useState('');
    const [validationError, setValidationError] = useState(null);
    const [aspectRatio, setAspectRatio] = useState('iphone-14-pro');
    const [designStyle, setDesignStyle] = useState('minimalist');
    const [theme, setTheme] = useState('dark');
    const { generate, reset, loading, error, imageUrl, metadata } = useGenerateWallpaper();

    const handleUrlChange = useCallback((e) => {
        setUrl(e.target.value);
        if (validationError) {
            setValidationError(null);
        }
    }, [validationError]);

    const handleGenerate = useCallback(async () => {
        const validation = validateNusmodsUrl(url);
        if (!validation.valid) {
            setValidationError(validation.error);
            return;
        }
        setValidationError(null);
        const modules = extractModules(url);
        console.log('Generating wallpaper:', {
            url,
            modules,
            aspectRatio: ASPECT_RATIOS.find(a => a.id === aspectRatio)?.value,
            designStyle,
            theme,
        });
        await generate(url, { aspectRatio, designStyle, theme });
    }, [url, aspectRatio, designStyle, theme, generate]);

    const handleReset = useCallback(() => {
        setUrl('');
        setValidationError(null);
        reset();
    }, [reset]);

    const isValidUrl = url.trim() !== '' && !validationError;

    return (
        <div className="min-h-screen relative">
            {/* Background gradient orb */}
            <div className="bg-gradient-orb" />

            {/* Navigation */}
            <nav className="relative z-10 flex items-center justify-between px-6 py-4 max-w-6xl mx-auto">
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-orange-400 to-orange-600 flex items-center justify-center">
                        <Sparkles className="w-4 h-4 text-white" />
                    </div>
                    <span className="font-semibold text-lg">ModPocket</span>
                </div>
                <a
                    href="https://github.com"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-secondary"
                >
                    <Github className="w-4 h-4" />
                    GitHub
                </a>
            </nav>

            {/* Hero Section */}
            <main className="relative z-10 max-w-4xl mx-auto px-6 pt-12 pb-24">
                {/* Badge */}
                <div className="flex justify-center mb-6 animate-fade-in">
                    <div className="badge">
                        <span>🎓 Built for NUS Students</span>
                        <span className="badge-highlight">Try it now →</span>
                    </div>
                </div>

                {/* Headline */}
                <h1 className="text-4xl md:text-5xl font-bold text-center leading-tight mb-4 animate-fade-in-delay-1">
                    Your NUSMods timetable,<br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-orange-500">
                        on your iPhone
                    </span>
                </h1>

                {/* Subheadline */}
                <p className="text-center text-base md:text-lg text-[hsl(var(--muted-foreground))] max-w-xl mx-auto mb-8 animate-fade-in-delay-2">
                    Transform your NUSMods share link into a beautiful wallpaper.
                </p>

                {/* Input Section */}
                {!imageUrl && (
                    <div className="max-w-xl mx-auto animate-fade-in-delay-3">
                        {/* URL Input */}
                        <div className="relative mb-4">
                            <Link2 className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-[hsl(var(--muted-foreground))]" />
                            <input
                                type="url"
                                value={url}
                                onChange={handleUrlChange}
                                placeholder="Paste your NUSMods share link..."
                                disabled={loading}
                                className="input-shadcn pl-11"
                            />
                        </div>

                        {/* Options Grid */}
                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-4">
                            <Select
                                label="Device"
                                value={aspectRatio}
                                onChange={setAspectRatio}
                                options={ASPECT_RATIOS}
                                icon={Smartphone}
                            />
                            <Select
                                label="Style"
                                value={designStyle}
                                onChange={setDesignStyle}
                                options={DESIGN_STYLES}
                                icon={Palette}
                            />
                            <ThemeToggle value={theme} onChange={setTheme} />
                        </div>

                        {/* Error */}
                        {validationError && (
                            <div className="flex items-center gap-2 text-red-400 text-sm mb-4">
                                <AlertCircle className="w-4 h-4" />
                                <span>{validationError}</span>
                            </div>
                        )}

                        {/* API Error */}
                        {error && (
                            <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 mb-4">
                                <div className="flex items-center gap-2 text-red-400 text-sm">
                                    <AlertCircle className="w-4 h-4" />
                                    <span>{error}</span>
                                </div>
                            </div>
                        )}

                        {/* CTA Buttons */}
                        <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
                            <button
                                onClick={handleGenerate}
                                disabled={!isValidUrl || loading}
                                className="btn-primary btn-orange w-full sm:w-auto"
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="w-4 h-4 animate-spin" />
                                        Generating...
                                    </>
                                ) : (
                                    <>
                                        Get Wallpaper
                                        <ArrowRight className="w-4 h-4" />
                                    </>
                                )}
                            </button>
                            <a
                                href="https://nusmods.com"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="btn-secondary w-full sm:w-auto"
                            >
                                Open NUSMods
                            </a>
                        </div>

                        {/* Helper text */}
                        <p className="text-center text-xs text-[hsl(var(--muted-foreground))] mt-3">
                            Go to NUSMods → Click "Share/Sync" → Copy the link
                        </p>
                    </div>
                )}

                {/* Success/Preview Section */}
                {imageUrl && (
                    <div className="flex flex-col items-center animate-fade-in">
                        <div className="phone-frame mb-6">
                            <div className="phone-notch" />
                            <div className="phone-screen">
                                <img src={imageUrl} alt="Generated wallpaper" className="w-full h-full object-cover" />
                            </div>
                            <div className="phone-home-bar" />
                        </div>

                        {metadata && (
                            <p className="text-sm text-[hsl(var(--muted-foreground))] mb-6">
                                {metadata.modules?.length || 0} modules • {DESIGN_STYLES.find(s => s.id === designStyle)?.label} • {theme === 'dark' ? 'Dark' : 'Light'}
                            </p>
                        )}

                        <div className="flex flex-col sm:flex-row items-center gap-3">
                            <button onClick={() => window.open(imageUrl, '_blank')} className="btn-primary btn-orange">
                                <Download className="w-4 h-4" />
                                Download Wallpaper
                            </button>
                            <button onClick={handleReset} className="btn-secondary">
                                <RotateCcw className="w-4 h-4" />
                                Generate Another
                            </button>
                        </div>
                    </div>
                )}

                {/* Phone Preview Placeholder */}
                {!imageUrl && !loading && (
                    <div className="flex justify-center mt-12 animate-fade-in-delay-3">
                        <div className="phone-frame opacity-50 scale-90">
                            <div className="phone-notch" />
                            <div className="phone-screen">
                                <div className="flex flex-col items-center text-[hsl(var(--muted-foreground))]">
                                    <ImageIcon className="w-8 h-8 mb-2 opacity-50" />
                                    <span className="text-xs">Preview</span>
                                </div>
                            </div>
                            <div className="phone-home-bar" />
                        </div>
                    </div>
                )}

                {/* Loading State */}
                {loading && (
                    <div className="flex justify-center mt-12">
                        <div className="phone-frame animate-pulse">
                            <div className="phone-notch" />
                            <div className="phone-screen">
                                <Loader2 className="w-8 h-8 text-orange-500 animate-spin" />
                            </div>
                            <div className="phone-home-bar" />
                        </div>
                    </div>
                )}
            </main>

            {/* Footer */}
            <footer className="relative z-10 text-center py-6 text-sm text-[hsl(var(--muted-foreground))]">
                <p>
                    Made with 🧡 for NUS Students •{' '}
                    <a href="https://nusmods.com" target="_blank" rel="noopener noreferrer" className="text-orange-400 hover:underline">
                        NUSMods
                    </a>
                </p>
            </footer>
        </div>
    );
}

export default App;
