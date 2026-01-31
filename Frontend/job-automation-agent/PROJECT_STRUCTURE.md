# JobAgent - Project Structure & File Guide

Complete guide to understanding the codebase structure and where to find everything.

## Directory Tree

```
jobagent/
├── app/                              # Next.js App Router pages
│   ├── layout.tsx                    # Root layout with AuthProvider
│   ├── globals.css                   # Global styles & animations
│   ├── page.tsx                      # Landing page
│   ├── login/
│   │   └── page.tsx                  # Login page with Google Sign-In
│   ├── register/
│   │   └── page.tsx                  # Registration with questionnaire & resume upload
│   └── dashboard/
│       ├── page.tsx                  # Main dashboard with chat interface
│       ├── settings/
│       │   └── page.tsx              # Profile & resume management
│       └── applications/
│           └── page.tsx              # Application tracking
│
├── components/                       # React components
│   ├── landing/                      # Landing page sections
│   │   ├── AnimatedHeader.tsx        # Animated navigation header
│   │   ├── HeroSection.tsx           # Hero with gradient text
│   │   └── FeaturesSection.tsx       # Features showcase
│   ├── chat/                         # Chat interface components
│   │   ├── ChatInterface.tsx         # Main chat component (ChatGPT-like)
│   │   ├── ChatMessage.tsx           # Individual message display
│   │   └── ThinkingAnimation.tsx     # Gemini-style thinking animation
│   ├── dashboard/                    # Dashboard layout components
│   │   ├── DashboardHeader.tsx       # Top navigation bar
│   │   └── DashboardSidebar.tsx      # Left sidebar navigation
│   ├── ui/                           # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   ├── textarea.tsx
│   │   ├── spinner.tsx
│   │   ├── badge.tsx
│   │   ├── alert.tsx
│   │   ├── dialog.tsx
│   │   ├── form.tsx
│   │   └── ... (50+ UI components)
│   └── theme-provider.tsx            # Theme wrapper
│
├── context/                          # React Context
│   └── AuthContext.tsx               # Firebase authentication context
│
├── lib/                              # Utilities & services
│   ├── firebase.ts                   # Firebase configuration & initialization
│   ├── gemini.ts                     # Gemini API integration service
│   └── utils.ts                      # Tailwind className utilities
│
├── hooks/                            # Custom React hooks
│   ├── use-mobile.ts                 # Responsive design hook
│   └── use-toast.ts                  # Toast notification hook
│
├── styles/                           # Additional styles
│   └── globals.css                   # (Duplicate, main one is in app/)
│
├── public/                           # Static assets
│   └── (images, icons, etc.)
│
├── .env.example                      # Environment variables template
├── README.md                         # Main documentation
├── SETUP_GUIDE.md                    # Detailed setup instructions
├── QUICKSTART.md                     # Quick start checklist
├── DEPLOYMENT.md                     # Deployment guide
├── PROJECT_STRUCTURE.md              # This file
├── package.json                      # Dependencies
├── tsconfig.json                     # TypeScript config
├── next.config.mjs                   # Next.js config
└── tailwind.config.js                # Tailwind configuration
```

## File Descriptions

### Core Application Files

#### `/app/layout.tsx`
- Root layout component
- Wraps entire app with AuthProvider
- Sets up metadata and viewport
- Imports all global styles

#### `/app/globals.css`
- **Color tokens** (purple, gold, dark backgrounds)
- **Custom animations** (gradient-shift, thinking-pulse, dot-bounce, etc.)
- **Tailwind CSS v4 imports**
- **Theme variables** for dark mode

#### `/app/page.tsx`
- Landing page entry point
- Imports: AnimatedHeader, HeroSection, FeaturesSection
- Shows demo of platform capabilities
- Links to login/register

### Page Routes

#### `/app/login/page.tsx`
- Email/password login form
- Google Sign-In button
- Link to register page
- Error handling for auth failures

#### `/app/register/page.tsx`
- Registration form (email/password)
- Job application questionnaire
- Resume file upload
- Form validation
- Success redirect to dashboard

#### `/app/dashboard/page.tsx`
- Main user dashboard
- Imports DashboardHeader and ChatInterface
- Protected route (requires auth)
- Chat with AI agent

#### `/app/dashboard/settings/page.tsx`
- User profile management
- Resume upload/management
- Job preferences editing
- Account settings
- Logout button

#### `/app/dashboard/applications/page.tsx`
- View submitted job applications
- Application history
- Status tracking
- Sorting and filtering

### Components - Landing Page

#### `components/landing/AnimatedHeader.tsx`
- Navigation bar
- Logo
- Auth links
- Animated background
- Responsive menu

#### `components/landing/HeroSection.tsx`
- Large hero image/gradient
- Main headline
- Subheading
- CTA buttons (Get Started, Learn More)
- Scroll animations

#### `components/landing/FeaturesSection.tsx`
- Feature cards grid
- Icon, title, description per feature
- Hover animations
- Responsive layout

### Components - Chat Interface

#### `components/chat/ChatInterface.tsx`
- Main chat component (ChatGPT-like)
- Message input area with file upload
- Message history display
- Scrolls to latest message
- Integrates with Gemini API
- Loading states

#### `components/chat/ChatMessage.tsx`
- Individual message display
- User vs Assistant styling
- Timestamp display
- Message formatting
- Markdown support (optional)

#### `components/chat/ThinkingAnimation.tsx`
- Google Gemini-style thinking animation
- Three bouncing dots
- Continuous animation
- Shows while AI is processing

### Components - Dashboard

#### `components/dashboard/DashboardHeader.tsx`
- Top navigation bar
- User profile dropdown
- Settings link
- Logout button
- Dark mode toggle (optional)
- User avatar

#### `components/dashboard/DashboardSidebar.tsx`
- Left sidebar navigation
- Links to: Dashboard, Settings, Applications
- Collapsible on mobile
- User info section
- Active route highlighting

### Integration Services

#### `/lib/firebase.ts`
- Firebase configuration (from env vars)
- Auth initialization
- Firestore initialization
- Cloud Storage initialization
- Emulator setup (development only)
- Exports: `auth`, `db`, `storage`, `app`

#### `/lib/gemini.ts`
- GeminiService class
- `sendMessage()` - Send chat messages
- `analyzeJobForm()` - Analyze form HTML
- `fillFormWithData()` - Auto-fill form fields
- `extractResumeData()` - Parse resume text
- System prompt for job filling context
- API error handling

#### `/lib/utils.ts`
- `cn()` - Classname utility (Tailwind)
- Type utilities
- Helper functions

### Context & Authentication

#### `/context/AuthContext.tsx`
- AuthProvider component
- useAuth() hook
- User state management
- Sign up / Sign in / Sign out methods
- Resume data management
- Job application form data
- Persists auth state

### UI Components

The `components/ui/` directory contains 50+ shadcn/ui components:
- **Form Components**: input, textarea, form, field, input-group
- **Display**: card, badge, alert, avatar, progress, skeleton
- **Interactive**: button, button-group, checkbox, radio-group, select, switch, toggle
- **Navigation**: tabs, breadcrumb, navigation-menu, pagination, sidebar
- **Modals**: dialog, alert-dialog, drawer, popover, dropdown-menu
- **Data**: table, carousel, scroll-area
- **Utility**: spinner, kbd, empty, item

---

## Data Flow

### Authentication Flow
```
User → Register/Login Page → Firebase Auth → AuthContext → Protected Routes
```

### Chat Flow
```
User Input → ChatInterface → Gemini API → AI Response → ChatMessage Display
```

### Resume Upload Flow
```
Resume File → Register/Settings → Firebase Storage → User Profile
```

### Form Filling Flow
```
User URL → Chat → Gemini Analysis → Form Detection → Auto-fill → Completion
```

---

## Key Technologies

| Technology | Purpose | File |
|-----------|---------|------|
| Next.js 16 | Framework | app/, next.config.mjs |
| React 19 | UI Library | components/ |
| Tailwind v4 | Styling | app/globals.css |
| TypeScript | Type Safety | tsconfig.json |
| Firebase Auth | Authentication | lib/firebase.ts |
| Firestore | Database | lib/firebase.ts |
| Cloud Storage | File Upload | lib/firebase.ts |
| Google Gemini | AI | lib/gemini.ts |

---

## Adding New Features

### Add a New Page
1. Create directory under `/app`
2. Create `page.tsx` file
3. Import components as needed
4. Update navigation in DashboardSidebar

### Add a New Component
1. Create file in appropriate `/components/` subdirectory
2. Name: `PascalCase.tsx`
3. Use 'use client' if interactive
4. Export component as default

### Add New Animations
1. Edit `/app/globals.css`
2. Add `@keyframes` in `@layer utilities`
3. Add utility class
4. Use class in components

### Modify Theme Colors
1. Edit `:root` and `.dark` in `/app/globals.css`
2. Update `--primary`, `--accent`, etc.
3. Rebuild and test

---

## Environment Variables

All variables must be set for full functionality:

```bash
# Firebase (from Firebase Console)
NEXT_PUBLIC_FIREBASE_API_KEY
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN
NEXT_PUBLIC_FIREBASE_PROJECT_ID
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID
NEXT_PUBLIC_FIREBASE_APP_ID

# Gemini API (from Google AI Studio)
NEXT_PUBLIC_GEMINI_API_KEY
```

See `.env.example` for template.

---

## Important Notes

1. **Public vs Protected Routes**
   - Public: `/`, `/login`, `/register`
   - Protected: `/dashboard/*` (requires auth)

2. **Dark Mode**
   - Always enabled (check `layout.tsx`)
   - To support light mode, extend `globals.css`

3. **Animations**
   - Defined in `globals.css` @keyframes
   - Applied as utility classes
   - Smooth, performant CSS animations

4. **Firebase Security**
   - Uses environment variables (never exposed)
   - Client-side SDK with Auth
   - Security rules should be configured
   - See DEPLOYMENT.md for rules

5. **Gemini Integration**
   - Streaming responses for fast feedback
   - Thinking animation while processing
   - Error handling with fallbacks
   - API key from `NEXT_PUBLIC_GEMINI_API_KEY`

---

## File Naming Conventions

- **Pages**: `page.tsx` (must be exact name)
- **Components**: `PascalCase.tsx`
- **Utilities**: `camelCase.ts`
- **Styles**: `globals.css` or component.module.css
- **Types/Interfaces**: Inline or separate `.types.ts`

---

## Import Paths

Use absolute imports with `@/` alias:
```typescript
// Good
import { ChatInterface } from '@/components/chat/ChatInterface'
import { geminiService } from '@/lib/gemini'
import { useAuth } from '@/context/AuthContext'

// Avoid
import { ChatInterface } from '../../../components/chat/ChatInterface'
```

---

## Next Steps for Customization

1. **Change Colors** → Edit `/app/globals.css`
2. **Add AI Prompts** → Modify `/lib/gemini.ts`
3. **Add Pages** → Create `/app/[path]/page.tsx`
4. **Custom Components** → Add to `/components/`
5. **New Animations** → Add `@keyframes` to globals.css

---

See README.md for full documentation and DEPLOYMENT.md for production setup.
