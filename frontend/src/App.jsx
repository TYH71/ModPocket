import React, { useState, useCallback } from 'react';
import { Sparkles, ArrowRight, Link2, Loader2, Download, RotateCcw, ImageIcon, AlertCircle, Github, ChevronDown, Smartphone, Sun, Moon, Zap, Users, Check } from 'lucide-react';
import { validateNusmodsUrl, extractModules } from './utils/validateNusmodsUrl';
import { useGenerateWallpaper } from './hooks/useGenerateWallpaper';

// Aspect ratio options - using ratio format for backend
const ASPECT_RATIOS = [
    { id: '9:19.5', label: 'iPhone 14/15 Pro', value: '9:19.5' },
    { id: '9:21', label: 'iPhone Pro Max', value: '9:21' },
    { id: '9:16', label: 'iPhone SE / Standard', value: '9:16' },
    { id: '9:20', label: 'Android (1080p)', value: '9:20' },
];

// Design style options with preview classes
const DESIGN_STYLES = [
    { id: 'minimalist', label: 'Minimal', description: 'Clean & elegant', preview: 'minimalist' },
    { id: 'gradient', label: 'Gradient', description: 'Vibrant flow', preview: 'gradient' },
    { id: 'neon', label: 'Neon', description: 'Cyberpunk glow', preview: 'neon' },
    { id: 'pastel', label: 'Pastel', description: 'Soft & calm', preview: 'pastel' },
    { id: 'glassmorphism', label: 'Glass', description: 'Frosted blur', preview: 'glassmorphism' },
    { id: 'kawaii', label: 'Kawaii', description: 'Cute doodles', preview: 'kawaii' },
    { id: 'retro', label: 'Retro', description: 'Warm vintage', preview: 'retro' },
];

// Floating particles component
const Particles = () => (
    <div className="particles">
        {[...Array(6)].map((_, i) => (
            <div key={i} className="particle" />
        ))}
    </div>
);

// Custom Select Component
const Select = ({ value, onChange, options, icon: Icon, label }) => {
    const [isOpen, setIsOpen] = useState(false);
    const selectedOption = options.find(opt => opt.id === value);

    return (
        <div className="relative">
            <label className="block text-xs text-[hsl(var(--muted-foreground))] mb-1.5 font-medium">{label}</label>
            <button
                type="button"
                onClick={() => setIsOpen(!isOpen)}
                className="select-trigger w-full"
            >
                <div className="flex items-center gap-2">
                    {Icon && <Icon className="w-3.5 h-3.5 text-orange-400" />}
                    <span className="text-white">{selectedOption?.label}</span>
                </div>
                <ChevronDown className={`w-3.5 h-3.5 text-[hsl(var(--muted-foreground))] transition-transform ${isOpen ? 'rotate-180' : ''}`} />
            </button>

            {isOpen && (
                <>
                    <div className="fixed inset-0 z-40" onClick={() => setIsOpen(false)} />
                    <div className="select-dropdown">
                        {options.map((option) => (
                            <button
                                key={option.id}
                                onClick={() => { onChange(option.id); setIsOpen(false); }}
                                className={`w-full px-3 py-2 text-sm text-left rounded-md transition-colors flex items-center justify-between ${value === option.id ? 'bg-orange-500/10 text-orange-400' : 'hover:bg-white/5'
                                    }`}
                            >
                                <span>{option.label}</span>
                                {value === option.id && <Check className="w-3.5 h-3.5" />}
                            </button>
                        ))}
                    </div>
                </>
            )}
        </div>
    );
};

// Theme Toggle
const ThemeToggle = ({ value, onChange }) => (
    <div>
        <label className="block text-xs text-[hsl(var(--muted-foreground))] mb-1.5 font-medium">Theme</label>
        <div className="theme-toggle">
            <button
                type="button"
                onClick={() => onChange('light')}
                className={`theme-btn ${value === 'light' ? 'active' : ''}`}
            >
                <Sun className="w-3.5 h-3.5" />
                Light
            </button>
            <button
                type="button"
                onClick={() => onChange('dark')}
                className={`theme-btn ${value === 'dark' ? 'active dark-active' : ''}`}
            >
                <Moon className="w-3.5 h-3.5" />
                Dark
            </button>
        </div>
    </div>
);

// Style Card Component
const StyleCard = ({ style, selected, onClick }) => (
    <button
        type="button"
        onClick={onClick}
        className={`style-card ${selected ? 'selected' : ''}`}
    >
        <div className={`style-preview ${style.preview}`}>
            {style.id === 'neon' && (
                <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-6 h-6 rounded-full bg-green-500/30 blur-md" />
                </div>
            )}
        </div>
        <div className="text-xs font-medium">{style.label}</div>
        <div className="text-[10px] text-[hsl(var(--muted-foreground))]">{style.description}</div>
        {selected && (
            <div className="absolute top-2 right-2">
                <Check className="w-3.5 h-3.5 text-orange-400" />
            </div>
        )}
    </button>
);

// Phone Mockup
const PhoneMockup = ({ imageUrl, loading, placeholder }) => (
    <div className="phone-container">
        <div className="phone-frame">
            <div className="phone-notch" />
            <div className="phone-screen">
                {loading ? (
                    <Loader2 className="w-8 h-8 text-orange-500 animate-spin" />
                ) : imageUrl ? (
                    <img src={imageUrl} alt="Generated wallpaper" className="w-full h-full object-cover" />
                ) : placeholder ? (
                    <div className="flex flex-col items-center text-[hsl(var(--muted-foreground))]">
                        <ImageIcon className="w-8 h-8 mb-2 opacity-40" />
                        <span className="text-xs opacity-60">Your wallpaper</span>
                    </div>
                ) : null}
            </div>
            <div className="phone-home-bar" />
        </div>
    </div>
);

function App() {
    const [url, setUrl] = useState('');
    const [validationError, setValidationError] = useState(null);
    const [aspectRatio, setAspectRatio] = useState('9:19.5');
    const [designStyle, setDesignStyle] = useState('minimalist');
    const [theme, setTheme] = useState('dark');
    const { generate, reset, loading, error, imageUrl, metadata } = useGenerateWallpaper();

    const handleUrlChange = useCallback((e) => {
        setUrl(e.target.value);
        if (validationError) setValidationError(null);
    }, [validationError]);

    const handleGenerate = useCallback(async () => {
        const validation = validateNusmodsUrl(url);
        if (!validation.valid) {
            setValidationError(validation.error);
            return;
        }
        setValidationError(null);
        const modules = extractModules(url);
        console.log('Generating:', { url, modules, aspectRatio, designStyle, theme });
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
            {/* Animated Background */}
            <div className="animated-bg" />
            <Particles />

            {/* Navigation */}
            <nav className="relative z-10 flex items-center justify-between px-6 py-4 max-w-6xl mx-auto">
                <div className="flex items-center gap-2.5">
                    <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-orange-400 to-orange-600 flex items-center justify-center shadow-lg shadow-orange-500/20">
                        <Sparkles className="w-4.5 h-4.5 text-white" />
                    </div>
                    <span className="font-bold text-lg tracking-tight">ModPocket</span>
                </div>
                <a
                    href="https://github.com/Ducksss/ModPocket"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-secondary text-sm"
                >
                    <Github className="w-4 h-4" />
                    Star on GitHub
                </a>
            </nav>

            {/* Hero Section */}
            <main className="relative z-10 max-w-5xl mx-auto px-6 pt-8 pb-16">
                {/* Badge */}
                <div className="flex justify-center mb-6 animate-fade-up">
                    <div className="badge shimmer">
                        <span>🎓 Built for NUS Students</span>
                        <span className="badge-highlight">v1.0 Launch →</span>
                    </div>
                </div>

                {/* Headline */}
                <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-center leading-[1.1] mb-4 animate-fade-up animate-delay-1">
                    Your timetable,<br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-orange-400 to-orange-500">
                        your wallpaper
                    </span>
                </h1>

                {/* Subheadline */}
                <p className="text-center text-base md:text-lg text-[hsl(var(--muted-foreground))] max-w-md mx-auto mb-6 animate-fade-up animate-delay-2">
                    Transform your NUSMods link into a stunning iPhone wallpaper in seconds.
                </p>

                {/* Stats Bar */}
                <div className="stats-bar mb-8 animate-fade-up animate-delay-2">
                    <div className="stat-item">
                        <div className="stat-value">500+</div>
                        <div className="stat-label">Wallpapers Made</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-value flex items-center gap-1"><Zap className="w-4 h-4" /> 3s</div>
                        <div className="stat-label">Generation Time</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-value flex items-center gap-1"><Users className="w-4 h-4" /> 200+</div>
                        <div className="stat-label">NUS Students</div>
                    </div>
                </div>

                {/* Main Content */}
                {!imageUrl && (
                    <div className="flex flex-col lg:flex-row gap-8 items-center animate-fade-up animate-delay-3">
                        {/* Left: Form */}
                        <div className="flex-1 w-full max-w-lg">
                            {/* URL Input */}
                            <div className="relative mb-5">
                                <Link2 className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-[hsl(var(--muted-foreground))] pointer-events-none" />
                                <input
                                    type="url"
                                    value={url}
                                    onChange={handleUrlChange}
                                    placeholder="Paste your NUSMods share link..."
                                    disabled={loading}
                                    className="input-shadcn"
                                />
                            </div>

                            {/* Device & Theme */}
                            <div className="grid grid-cols-2 gap-3 mb-4">
                                <Select
                                    label="Device"
                                    value={aspectRatio}
                                    onChange={setAspectRatio}
                                    options={ASPECT_RATIOS}
                                    icon={Smartphone}
                                />
                                <ThemeToggle value={theme} onChange={setTheme} />
                            </div>

                            {/* Style Selection */}
                            <div className="mb-6">
                                <label className="block text-xs text-[hsl(var(--muted-foreground))] mb-2 font-medium">Choose a Style</label>
                                <div className="grid grid-cols-3 gap-2">
                                    {DESIGN_STYLES.map((style) => (
                                        <StyleCard
                                            key={style.id}
                                            style={style}
                                            selected={designStyle === style.id}
                                            onClick={() => setDesignStyle(style.id)}
                                        />
                                    ))}
                                </div>
                            </div>

                            {/* Errors */}
                            {(validationError || error) && (
                                <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 mb-4">
                                    <div className="flex items-center gap-2 text-red-400 text-sm">
                                        <AlertCircle className="w-4 h-4 flex-shrink-0" />
                                        <span>{validationError || error}</span>
                                    </div>
                                </div>
                            )}

                            {/* CTA Buttons */}
                            <div className="flex gap-3">
                                <button
                                    onClick={handleGenerate}
                                    disabled={!isValidUrl || loading}
                                    className="btn-primary flex-1"
                                >
                                    {loading ? (
                                        <>
                                            <Loader2 className="w-4 h-4 animate-spin" />
                                            Generating...
                                        </>
                                    ) : (
                                        <>
                                            Generate Wallpaper
                                            <ArrowRight className="w-4 h-4" />
                                        </>
                                    )}
                                </button>
                                <a
                                    href="https://nusmods.com"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="btn-secondary"
                                >
                                    NUSMods
                                </a>
                            </div>

                            <p className="text-center text-xs text-[hsl(var(--muted-foreground))] mt-3">
                                NUSMods → Share/Sync → Copy link → Paste above
                            </p>
                        </div>

                        {/* Right: Phone Preview */}
                        <div className="flex-shrink-0">
                            <PhoneMockup loading={loading} placeholder={!loading} />
                        </div>
                    </div>
                )}

                {/* Success State */}
                {imageUrl && (
                    <div className="flex flex-col items-center animate-fade-up">
                        <PhoneMockup imageUrl={imageUrl} />

                        {metadata && (
                            <p className="text-sm text-[hsl(var(--muted-foreground))] mt-4 mb-4">
                                {metadata.modules?.length || 0} modules • {DESIGN_STYLES.find(s => s.id === designStyle)?.label} • {theme === 'dark' ? 'Dark' : 'Light'}
                            </p>
                        )}

                        <div className="flex gap-3">
                            <button onClick={() => window.open(imageUrl, '_blank')} className="btn-primary">
                                <Download className="w-4 h-4" />
                                Download Wallpaper
                            </button>
                            <button onClick={handleReset} className="btn-secondary">
                                <RotateCcw className="w-4 h-4" />
                                Make Another
                            </button>
                        </div>
                    </div>
                )}
            </main>

            {/* Footer */}
            <footer className="relative z-10 text-center py-6 text-sm text-[hsl(var(--muted-foreground))]">
                Made with 🧡 at NUS • Powered by{' '}
                <a href="https://nusmods.com" target="_blank" rel="noopener noreferrer" className="text-orange-400 hover:underline">NUSMods</a>
            </footer>
        </div>
    );
}

export default App;
