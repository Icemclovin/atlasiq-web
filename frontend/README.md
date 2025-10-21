# AtlasIQ Web Frontend

Modern React + TypeScript frontend for the AtlasIQ macroeconomic data dashboard.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Backend API running on http://localhost:8000

### Installation

```powershell
# Navigate to frontend directory
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web\frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at **http://localhost:3000**

### Build for Production

```powershell
npm run build
npm run preview
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   ├── Loading.tsx
│   │   └── ProtectedRoute.tsx
│   ├── context/             # React contexts
│   │   └── AuthContext.tsx  # Authentication state
│   ├── pages/               # Page components
│   │   ├── Login.tsx        # Login page
│   │   ├── Register.tsx     # Registration page
│   │   └── Dashboard.tsx    # Main dashboard
│   ├── services/            # API service layer
│   │   ├── api.ts           # Axios client with interceptors
│   │   ├── auth.ts          # Authentication API
│   │   └── data.ts          # Data fetching API
│   ├── types/               # TypeScript types
│   │   └── index.ts         # Type definitions
│   ├── App.tsx              # Root component with routing
│   ├── main.tsx             # Application entry point
│   └── index.css            # Global styles
├── public/                  # Static assets
├── index.html              # HTML template
├── package.json            # Dependencies
├── vite.config.ts          # Vite configuration
├── tailwind.config.js      # Tailwind CSS config
└── tsconfig.json           # TypeScript config
```

## 🎨 Features

### Authentication

- ✅ User registration with validation
- ✅ Login with JWT tokens
- ✅ Automatic token refresh
- ✅ Protected routes
- ✅ Persistent authentication

### Dashboard

- ✅ KPI cards (Countries, Indicators, Data Freshness)
- ✅ Country overview cards with risk scores
- ✅ Interactive charts (GDP Growth, Risk Scores)
- ✅ Responsive design for all devices
- ✅ Real-time data updates

### UI Components

- **Button**: Multiple variants (primary, secondary, danger, ghost)
- **Card**: Reusable card container with hover effects
- **Input**: Form input with label, error, and helper text
- **Loading**: Spinner and loading states
- **ProtectedRoute**: Authentication guard for routes

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### API Integration

The frontend connects to the backend API using Axios with automatic:

- JWT token injection
- Token refresh on 401 errors
- Error handling
- Request/response interceptors

## 🎯 Usage

### 1. Start the Backend

Make sure the backend server is running on port 8000:

```powershell
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web\backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start the Frontend

```powershell
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web\frontend
npm run dev
```

### 3. Access the Application

Open your browser and navigate to:

- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs

### 4. Create an Account

1. Click "Sign up" on the login page
2. Fill in your details (name, email, password)
3. Submit the form
4. You'll be automatically logged in and redirected to the dashboard

## 📊 Available Routes

- `/` - Redirects to dashboard (if authenticated) or login
- `/login` - Login page
- `/register` - Registration page
- `/dashboard` - Main dashboard (protected)

## 🛠️ Development

### Running in Development Mode

The development server supports:

- Hot Module Replacement (HMR)
- Fast refresh for React components
- TypeScript type checking
- ESLint linting

### Code Style

The project uses:

- TypeScript for type safety
- Tailwind CSS for styling
- Functional React components with hooks
- Async/await for API calls

### Adding New Pages

1. Create a new component in `src/pages/`
2. Add route in `src/App.tsx`
3. Use `<ProtectedRoute>` if authentication is required

Example:

```tsx
<Route
  path="/new-page"
  element={
    <ProtectedRoute>
      <NewPage />
    </ProtectedRoute>
  }
/>
```

## 📦 Dependencies

### Core

- **React 18**: UI library
- **React Router DOM**: Routing
- **TypeScript**: Type safety

### UI & Styling

- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Icon library
- **clsx**: Conditional class names

### Data & API

- **Axios**: HTTP client
- **Recharts**: Chart library for data visualization

## 🐛 Troubleshooting

### Port Already in Use

If port 3000 is already in use:

```powershell
# Edit vite.config.ts and change the port:
server: {
  port: 3001,  # Change to any available port
}
```

### API Connection Issues

1. Verify backend is running on port 8000
2. Check CORS settings in backend `.env`:
   ```
   CORS_ORIGINS=http://localhost:3000,http://localhost:5173
   ```
3. Check browser console for errors

### TypeScript Errors

Run type checking:

```powershell
npm run build
```

## 📈 Performance

The application is optimized for:

- Fast initial load with code splitting
- Lazy loading of routes
- Optimized bundle size
- Responsive images and assets

## 🔒 Security

- JWT tokens stored in localStorage
- Automatic token refresh
- Protected routes with authentication guards
- HTTPS recommended for production

## 🚀 Deployment

### Build for Production

```powershell
npm run build
```

The build output will be in the `dist/` directory.

### Deploy to Static Hosting

The frontend can be deployed to:

- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront
- Any static hosting service

Make sure to set the correct `VITE_API_BASE_URL` for production.

## 📝 License

MIT License - See LICENSE file for details

---

**Version**: 1.0.0  
**Last Updated**: October 21, 2025  
**Built with**: React + TypeScript + Vite + Tailwind CSS
