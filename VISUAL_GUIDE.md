# 🎨 AtlasIQ Web - Visual Component Guide

## 🖼️ Page Layouts

### 1. Login Page (`/login`)

```
┌─────────────────────────────────────────────────────┐
│          Gradient Background (Blue/Primary)          │
│                                                      │
│     ┌─────────────────────────────────────────┐    │
│     │     Welcome to AtlasIQ                  │    │
│     │     Sign in to access your dashboard    │    │
│     │                                          │    │
│     │  ┌────────────────────────────────────┐ │    │
│     │  │ Email                              │ │    │
│     │  │ ┌────────────────────────────────┐ │ │    │
│     │  │ │ you@example.com                │ │ │    │
│     │  │ └────────────────────────────────┘ │ │    │
│     │  └────────────────────────────────────┘ │    │
│     │                                          │    │
│     │  ┌────────────────────────────────────┐ │    │
│     │  │ Password                           │ │    │
│     │  │ ┌────────────────────────────────┐ │ │    │
│     │  │ │ ••••••••                       │ │ │    │
│     │  │ └────────────────────────────────┘ │ │    │
│     │  └────────────────────────────────────┘ │    │
│     │                                          │    │
│     │  ┌────────────────────────────────────┐ │    │
│     │  │       Sign In                      │ │    │
│     │  └────────────────────────────────────┘ │    │
│     │                                          │    │
│     │  Don't have an account? Sign up         │    │
│     └─────────────────────────────────────────┘    │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### 2. Register Page (`/register`)

```
┌─────────────────────────────────────────────────────┐
│          Gradient Background (Blue/Primary)          │
│                                                      │
│     ┌─────────────────────────────────────────┐    │
│     │     Create Your Account                 │    │
│     │     Join AtlasIQ to start analyzing     │    │
│     │                                          │    │
│     │  [Full Name Input]                       │    │
│     │  [Email Input]                           │    │
│     │  [Password Input]                        │    │
│     │  [Confirm Password Input]                │    │
│     │                                          │    │
│     │  ┌────────────────────────────────────┐ │    │
│     │  │       Create Account               │ │    │
│     │  └────────────────────────────────────┘ │    │
│     │                                          │    │
│     │  Already have an account? Sign in       │    │
│     └─────────────────────────────────────────┘    │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### 3. Dashboard Page (`/dashboard`)

```
┌───────────────────────────────────────────────────────────────────┐
│  Header (White background with shadow)                            │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ AtlasIQ Dashboard          Welcome, John    [Logout ⟳]     │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  KPI Cards (Grid 4 columns)                                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ 🌍       │ │ 📊       │ │ 📈       │ │ 🕐       │          │
│  │ Countries│ │Indicators│ │Freshness │ │ Updated  │          │
│  │    4     │ │    127   │ │   2h     │ │ Oct 21   │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
│                                                                   │
│  Country Overview (Grid 2 columns)                               │
│  ┌─────────────────────────────┐ ┌─────────────────────────────┐│
│  │ Netherlands (NL)   🟢 Risk:25│ │ Belgium (BE)      🟡 Risk:45││
│  │ ─────────────────────────────│ │ ─────────────────────────────││
│  │ GDP Growth:  2.3% ↗         │ │ GDP Growth:  1.8% ↗         ││
│  │ Unemployment: 3.5%           │ │ Unemployment: 5.2%           ││
│  │ Inflation:   2.1%            │ │ Inflation:   2.8%            ││
│  │ Bus. Confidence: 102         │ │ Bus. Confidence: 98         ││
│  └─────────────────────────────┘ └─────────────────────────────┘│
│  ┌─────────────────────────────┐ ┌─────────────────────────────┐│
│  │ Luxembourg (LU)   🟢 Risk:20│ │ Germany (DE)      🟡 Risk:35││
│  │ ─────────────────────────────│ │ ─────────────────────────────││
│  │ GDP Growth:  3.1% ↗         │ │ GDP Growth:  1.2% ↗         ││
│  │ Unemployment: 2.8%           │ │ Unemployment: 4.5%           ││
│  │ Inflation:   1.9%            │ │ Inflation:   2.4%            ││
│  │ Bus. Confidence: 105         │ │ Bus. Confidence: 95         ││
│  └─────────────────────────────┘ └─────────────────────────────┘│
│                                                                   │
│  Charts (Grid 2 columns)                                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ GDP Growth by Country                                    │   │
│  │ ┌────────────────────────────────────────────────────┐  │   │
│  │ │    ▐██▌                                            │  │   │
│  │ │    ▐██▌   ▐██▌         ▐██▌   ▐██▌               │  │   │
│  │ │    ▐██▌   ▐██▌   ▐██▌  ▐██▌   ▐██▌               │  │   │
│  │ │ ───▐██▌───▐██▌───▐██▌──▐██▌───▐██▌──────────     │  │   │
│  │ │    NL     BE     LU     DE                        │  │   │
│  │ └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Risk Scores by Country                                   │   │
│  │ ┌────────────────────────────────────────────────────┐  │   │
│  │ │            ▐██▌                                    │  │   │
│  │ │    ▐██▌    ▐██▌         ▐██▌                       │  │   │
│  │ │    ▐██▌    ▐██▌   ▐██▌  ▐██▌                       │  │   │
│  │ │ ───▐██▌────▐██▌───▐██▌──▐██▌──────────────────    │  │   │
│  │ │    NL      BE     LU     DE                        │  │   │
│  │ └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

## 🎨 Component Specifications

### Button Component

```
Variants:
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Primary  │  │Secondary │  │  Danger  │  │  Ghost   │
│  (Blue)  │  │  (Gray)  │  │  (Red)   │  │(Transp.) │
└──────────┘  └──────────┘  └──────────┘  └──────────┘

Sizes:
┌──────┐    ┌──────────┐    ┌────────────┐
│ Small│    │  Medium  │    │   Large    │
└──────┘    └──────────┘    └────────────┘

States:
[Normal]  [Hover]  [Loading ⟳]  [Disabled]
```

### Card Component

```
┌──────────────────────────────────┐
│                                  │
│  Card Content                    │
│  - Clean white background        │
│  - Subtle shadow                 │
│  - Rounded corners               │
│  - Hover effect (shadow grows)   │
│                                  │
└──────────────────────────────────┘

Padding Options: None | Small | Medium | Large
```

### Input Component

```
Label
┌──────────────────────────────────┐
│ Placeholder text                 │
└──────────────────────────────────┘
Helper text

Error State:
Label
┌──────────────────────────────────┐
│ Invalid input (red border)       │
└──────────────────────────────────┘
⚠ Error message in red
```

### Loading Component

```
Spinner Sizes:

 ⟳ Small    ⟳  Medium    ⟳   Large

Full Page Loading:
┌─────────────────────────┐
│                         │
│         ⟳              │
│    Loading...           │
│                         │
└─────────────────────────┘
```

## 🎨 Color Palette

### Primary Colors

```
Primary-50:  #eff6ff (Very Light Blue)
Primary-100: #dbeafe (Light Blue)
Primary-200: #bfdbfe
Primary-300: #93c5fd
Primary-400: #60a5fa
Primary-500: #3b82f6 (Main Blue)
Primary-600: #2563eb (Dark Blue)
Primary-700: #1d4ed8
Primary-800: #1e40af
Primary-900: #1e3a8a (Very Dark Blue)
```

### Semantic Colors

```
Success: 🟢 Green (#10b981)
Warning: 🟡 Yellow (#f59e0b)
Danger:  🔴 Red (#ef4444)
Info:    🔵 Blue (#3b82f6)
```

### Gray Scale

```
Gray-50:  #f9fafb (Background)
Gray-100: #f3f4f6
Gray-200: #e5e7eb (Borders)
Gray-300: #d1d5db
Gray-400: #9ca3af
Gray-500: #6b7280
Gray-600: #4b5563 (Secondary Text)
Gray-700: #374151
Gray-800: #1f2937
Gray-900: #111827 (Primary Text)
```

### Risk Score Colors

```
Low Risk (0-39):     🟢 Green background, Green text
Medium Risk (40-69): 🟡 Yellow background, Yellow text
High Risk (70-100):  🔴 Red background, Red text
```

## 📐 Layout Grid

### Desktop (lg: 1024px+)

```
┌─────┬─────┬─────┬─────┐
│  1  │  2  │  3  │  4  │  KPI Cards (4 columns)
└─────┴─────┴─────┴─────┘
┌──────────────┬──────────────┐
│      1       │      2       │  Country Cards (2 columns)
├──────────────┼──────────────┤
│      3       │      4       │
└──────────────┴──────────────┘
┌──────────────┬──────────────┐
│   Chart 1    │   Chart 2    │  Charts (2 columns)
└──────────────┴──────────────┘
```

### Tablet (md: 768px)

```
┌───────┬───────┐
│   1   │   2   │  KPI Cards (2 columns)
├───────┼───────┤
│   3   │   4   │
└───────┴───────┘
┌─────────────────┐
│    Country 1    │  Country Cards (1 column)
├─────────────────┤
│    Country 2    │
├─────────────────┤
│    Country 3    │
├─────────────────┤
│    Country 4    │
└─────────────────┘
┌─────────────────┐
│    Chart 1      │  Charts (1 column)
├─────────────────┤
│    Chart 2      │
└─────────────────┘
```

### Mobile (sm: < 768px)

```
┌─────────────────┐
│    KPI 1        │  KPI Cards (1 column)
├─────────────────┤
│    KPI 2        │
├─────────────────┤
│    KPI 3        │
├─────────────────┤
│    KPI 4        │
└─────────────────┘
(same for countries and charts)
```

## 🎯 Icon Usage

```
🌍 Globe        - Countries, International
📊 Activity     - Indicators, Metrics
📈 TrendingUp   - Positive growth
📉 TrendingDown - Negative growth
🔒 Lock         - Security, Login
⟳  LogOut       - Logout action
⚠  AlertTriangle- Warnings, Errors
✓  Check        - Success, Completed
ℹ  Info         - Information
⚙  Settings     - Configuration
```

## 📱 Responsive Breakpoints

```
sm:  640px  (Small phones)
md:  768px  (Tablets)
lg:  1024px (Laptops)
xl:  1280px (Desktops)
2xl: 1536px (Large screens)
```

## 🎨 Typography

```
Headings:
h1: 2xl (24px) - Bold - Page titles
h2: xl (20px)  - Bold - Section titles
h3: lg (18px)  - Semibold - Card titles

Body:
base (16px) - Regular - Main text
sm (14px)   - Regular - Secondary text
xs (12px)   - Regular - Helper text

Font Family: Inter, system-ui, sans-serif
```

## 🌈 Animation & Transitions

```
Hover Effects:
- Buttons: background color change
- Cards: shadow grows (hover:shadow-lg)
- Links: color change

Loading:
- Spinner: rotate animation
- Duration: infinite

Transitions:
- All: transition-colors (smooth color changes)
- Shadow: transition-shadow
```

---

**This visual guide helps developers understand the UI structure and styling decisions made in the AtlasIQ Web frontend.**
