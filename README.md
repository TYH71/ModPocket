<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Ducksss/ModPocket">
    <img src="images/logo.png" alt="Logo" width="150" height="150">
  </a>

  <h3 align="center">📱 ModPocket</h3>

  <p align="center">
    Transform your NUSMods timetable into a stunning iPhone wallpaper in seconds!
    <br />
    <a href="#getting-started"><strong>Get Started »</strong></a>
    <br />
    <br />
    <a href="#demo">View Demo</a>
    ·
    <a href="https://github.com/Ducksss/ModPocket/issues/new?labels=bug">Report Bug</a>
    ·
    <a href="https://github.com/Ducksss/ModPocket/issues/new?labels=enhancement">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#architecture">Architecture</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#api-reference">API Reference</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

---

<!-- ABOUT THE PROJECT -->
## About The Project

<div align="center">
  <img src="images/screenshot.png" alt="ModPocket Screenshot" width="800">
</div>

**ModPocket** is a web application that transforms NUSMods timetable links into beautiful, customizable iPhone wallpapers. Built for NUS students who want to keep their schedule accessible at a glance.

### 😩 The Problem

As NUS students, we've all been there:
- **Missed a class** because we forgot to check NUSMods that morning
- **Showed up to the wrong venue** because we couldn't remember if it was LT27 or LT19
- **Opened NUSMods 10+ times a day** just to check our next class
- **Panicked before exams** trying to remember our schedule

NUSMods is great—but it requires you to *actively* open the app. What if your schedule was **already there** every time you glanced at your phone?

### 📱 Why Mobile-First?

We spend **4+ hours daily** on our phones. Our lock screen is the first thing we see when we wake up and the last thing before we sleep. Yet, most students are still:
- Fumbling through apps to check their schedule
- Screenshotting their NUSMods timetable (ugly and outdated)
- Missing classes because "I forgot to check"

**ModPocket makes your timetable impossible to miss.** It's not just a wallpaper—it's a **lifestyle upgrade** for busy students.

> *"The best interface is no interface."* — Our phones are already in our hands. Why not make the lock screen useful?

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔗 **Instant Generation** | Paste your NUSMods share link and get a wallpaper in ~3 seconds |
| 📐 **Multi-Device Support** | iPhone 14/15 Pro, Pro Max, SE, and Android |
| 🎨 **7 Design Styles** | Minimal, Gradient, Neon, Pastel, Glass, Kawaii, Retro |
| 🌗 **Theme Options** | Light and Dark mode support |
| 💾 **One-Click Download** | Save directly to your device |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

#### Frontend
[![React][React.js]][React-url]
[![TailwindCSS][TailwindCSS]][Tailwind-url]
[![JavaScript][JavaScript]][JavaScript-url]

#### Backend
[![Python][Python]][Python-url]
[![Google Cloud][GoogleCloud]][GoogleCloud-url]
[![Gemini][Gemini]][Gemini-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- ARCHITECTURE -->
## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ModPocket Architecture                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐     HTTPS POST      ┌──────────────────┐     ┌─────────────┐
│             │ ──────────────────► │                  │ ──► │             │
│   Frontend  │   {nusmods_url,     │   Cloud Run      │     │  Gemini AI  │
│   (React)   │    aspect_ratio,    │   (Python)       │ ◄── │  (Vision)   │
│             │    design_style,    │                  │     │             │
│             │    theme}           │                  │     └─────────────┘
│             │ ◄────────────────── │                  │
│             │   {image_base64,    │                  │
│             │    modules[]}       │                  │
└─────────────┘                     └──────────────────┘
      │                                     │
      ▼                                     ▼
┌─────────────┐                     ┌──────────────────┐
│  Tailwind   │                     │   NUSMods API    │
│  + Lucide   │                     │   (Parsing)      │
└─────────────┘                     └──────────────────┘
```

### Data Flow

1. **User Input** → Paste NUSMods share link + select customization options
2. **API Request** → Frontend sends POST request to Cloud Run endpoint
3. **URL Parsing** → Backend extracts module data from NUSMods URL
4. **AI Generation** → Gemini AI generates wallpaper based on timetable + style
5. **Response** → Base64-encoded image returned to frontend
6. **Display** → Wallpaper rendered in phone mockup with download option

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- GETTING STARTED -->
## Getting Started

Follow these steps to get a local copy up and running.

### Prerequisites

* Node.js 18+ and npm
  ```sh
  node --version  # Should be v18.x or higher
  ```

### Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/Ducksss/ModPocket.git
   cd ModPocket
   ```

2. **Install frontend dependencies**
   ```sh
   cd frontend
   npm install
   ```

3. **Start the development server**
   ```sh
   npm start
   ```

4. **Open your browser**
   
   Navigate to [http://localhost:3000](http://localhost:3000)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- USAGE -->
## Usage

### How to Get Your NUSMods Link

1. Go to [NUSMods](https://nusmods.com)
2. Navigate to **Timetable** → **Share/Sync**
3. Click **Copy Link**
4. Paste into ModPocket!

### Demo

<div align="center">
  <img src="images/demo.webp" alt="ModPocket Demo" width="600">
</div>

### Design Styles Preview

| Style | Preview | Description |
|-------|---------|-------------|
| Minimal | 🎨 | Clean & elegant |
| Gradient | 🌈 | Vibrant flow |
| Neon | 💚 | Cyberpunk glow |
| Pastel | 🌸 | Soft & calm |
| Glass | 🧊 | Frosted blur |
| Kawaii | ✿ | Cute doodles |
| Retro | 🔥 | Warm vintage |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- API REFERENCE -->
## API Reference

### Generate Wallpaper

```http
POST https://generate-wallpaper-bj6vohqe7a-as.a.run.app
```

#### Request Body

```json
{
  "nusmods_url": "https://nusmods.com/timetable/sem-2/share?CS2040=...",
  "aspect_ratio": "9:19.5",
  "design_style": "neon",
  "theme": "dark"
}
```

#### Response

```json
{
  "success": true,
  "image_base64": "<base64-encoded-png>",
  "modules": ["CS2040", "MA1521", "BT2102"]
}
```

### Parameters

| Parameter | Type | Options |
|-----------|------|---------|
| `aspect_ratio` | string | `9:19.5` (iPhone Pro), `9:21` (Pro Max), `9:16` (SE), `9:20` (Android) |
| `design_style` | string | `minimalist`, `gradient`, `neon`, `pastel`, `glassmorphism`, `kawaii`, `retro` |
| `theme` | string | `light`, `dark` |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- ROADMAP -->
## Roadmap

- [x] Core wallpaper generation
- [x] 7 design styles
- [x] Multi-device aspect ratios
- [x] Light/Dark theme support
- [ ] Semester-aware color schemes
- [ ] Custom color picker
- [ ] Widget support for iOS
- [ ] Gallery of generated wallpapers

See the [open issues](https://github.com/Ducksss/ModPocket/issues) for a full list of proposed features and known issues.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- LICENSE -->
## License

Distributed under the CC0 1.0 Universal License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- CONTACT -->
## Contact

**ModPocket Team** - Built with 🧡 at NUS

* [Chai Pin Zheng](https://www.linkedin.com/in/chai-pin-zheng)
* [Yu Hoe Tan](https://www.linkedin.com/in/yu-hoe-tan/)
* [Anton Ang](https://www.linkedin.com/in/anton-ang/)

Project Link: [https://github.com/Ducksss/ModPocket](https://github.com/Ducksss/ModPocket)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [NUSMods](https://nusmods.com) - For the amazing timetable platform
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [Lucide Icons](https://lucide.dev)
* [Tailwind CSS](https://tailwindcss.com)
* [Google Gemini AI](https://deepmind.google/technologies/gemini/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<div align="center">
  <strong>🏆 NUS Hackathon 2026</strong>
</div>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/Ducksss/ModPocket.svg?style=for-the-badge
[contributors-url]: https://github.com/Ducksss/ModPocket/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Ducksss/ModPocket.svg?style=for-the-badge
[forks-url]: https://github.com/Ducksss/ModPocket/network/members
[stars-shield]: https://img.shields.io/github/stars/Ducksss/ModPocket.svg?style=for-the-badge
[stars-url]: https://github.com/Ducksss/ModPocket/stargazers
[issues-shield]: https://img.shields.io/github/issues/Ducksss/ModPocket.svg?style=for-the-badge
[issues-url]: https://github.com/Ducksss/ModPocket/issues
[license-shield]: https://img.shields.io/github/license/Ducksss/ModPocket.svg?style=for-the-badge
[license-url]: https://github.com/Ducksss/ModPocket/blob/main/LICENSE

[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[TailwindCSS]: https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white
[Tailwind-url]: https://tailwindcss.com/
[JavaScript]: https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black
[JavaScript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[GoogleCloud]: https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white
[GoogleCloud-url]: https://cloud.google.com/
[Gemini]: https://img.shields.io/badge/Gemini_AI-8E75B2?style=for-the-badge&logo=google&logoColor=white
[Gemini-url]: https://deepmind.google/technologies/gemini/