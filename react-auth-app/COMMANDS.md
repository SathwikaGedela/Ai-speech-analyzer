# React Auth App - Commands Reference

## Development Commands

### Start Development Server
```bash
cd react-auth-app
npm run dev
```
**Output**: Server runs on `http://localhost:5174/` (or next available port)

### Build for Production
```bash
npm run build
```
**Output**: Creates `dist/` folder with optimized production files

### Preview Production Build
```bash
npm run preview
```
**Output**: Serves the production build locally

### Install Dependencies
```bash
npm install
```

### Add New Dependencies
```bash
# Add runtime dependency
npm install package-name

# Add development dependency  
npm install -D package-name
```

## Project Setup (Already Done)

### Create Vite React Project
```bash
npm create vite@latest react-auth-app -- --template react
cd react-auth-app
npm install
```

### Install Tailwind CSS
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Configure Tailwind (Already Configured)
- `tailwind.config.js` - Tailwind configuration with custom animations
- `postcss.config.js` - PostCSS configuration
- `src/index.css` - Tailwind directives and custom styles

## File Structure Commands

### View Project Structure
```bash
tree /f
# or
dir /s
```

### Check Package Info
```bash
npm list
npm outdated
npm audit
```

## Development Tips

### Hot Reload
- Changes to `.jsx`, `.js`, `.css` files trigger automatic reload
- No need to restart server for most changes

### Debugging
- Open browser DevTools (F12)
- Check Console for errors
- Use React DevTools extension

### Port Issues
If port 5173 is busy, Vite automatically tries the next available port (5174, 5175, etc.)

## Deployment Commands

### Build and Deploy to Static Hosting
```bash
npm run build
# Upload dist/ folder to your hosting provider
```

### Deploy to Netlify
```bash
npm run build
# Drag and drop dist/ folder to Netlify
```

### Deploy to Vercel
```bash
npm install -g vercel
vercel
```

## Troubleshooting Commands

### Clear Node Modules
```bash
rmdir /s node_modules
npm install
```

### Clear npm Cache
```bash
npm cache clean --force
```

### Check Node/npm Versions
```bash
node --version
npm --version
```

### Fix Permission Issues (if any)
```bash
npm config set registry https://registry.npmjs.org/
```

## Current Status
✅ **Development server running on**: `http://localhost:5174/`
✅ **All components created and configured**
✅ **Tailwind CSS properly set up**
✅ **Ready for development and testing**