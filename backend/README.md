# ModPocket Backend

Firebase Functions backend for generating NUSMods timetable wallpapers.

## API Endpoint

**URL:** `https://asia-southeast1-modpocket-369.cloudfunctions.net/generate_wallpaper`  
**Method:** `POST`  
**Content-Type:** `application/json`

## Sample Request

```json
{
    "nusmods_url": "https://nusmods.com/timetable/sem-2/share?BT2102=LAB:(7);LEC:(11)&CS2040=TUT:(33);LAB:(20);LEC:(34,35)&MA1521=LEC:(0,2)&UTW1001T=SEC:(2)",
    "aspect_ratio": "9:19.5",
    "design_style": "minimalist",
    "theme": "dark"
}
```

## Parameters

| Parameter | Type | Required | Default | Values |
|-----------|------|----------|---------|--------|
| `nusmods_url` | string | Yes | - | NUSMods share URL |
| `design_style` | string | No | `"minimalist"` | `"minimalist"`, `"gradient"`, `"neon"`, `"pastel"`, `"glass"`, `"retro"` |
| `theme` | string | No | `"light"` | `"light"`, `"dark"` |
| `aspect_ratio` | string | No | `"9:19.5"` | See table below |

### Aspect Ratios

| Value | Device |
|-------|--------|
| `9:19.5` | iPhone 14/15 Pro |
| `9:21` | iPhone Pro Max |
| `9:16` | iPhone SE / Standard |
| `9:20` | Android (1080p) |

## Response

```json
{
    "success": true,
    "image_base64": "<base64-encoded-png>",
    "modules": ["BT2102", "CS2040", "MA1521", "UTW1001T"]
}
```

## Design Styles

| Style | Description |
|-------|-------------|
| `minimalist` | Clean, professional, paper-like |
| `gradient` | Smooth color transitions |
| `neon` | Cyberpunk with glowing colors |
| `pastel` | Soft kawaii-style |
| `glass` | Glassmorphism effects |
| `retro` | Vintage 70s/80s aesthetic |

## Development

```bash
cd functions && uv sync
./export_deps.sh
firebase deploy --only functions
```
