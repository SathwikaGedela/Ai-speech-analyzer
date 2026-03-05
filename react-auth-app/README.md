# Interactive Authentication System

A modern React application with Vite and Tailwind CSS featuring interactive signup, signin, and dashboard functionality with smooth animations.

## Features

### 🔐 Authentication System
- **Signup Page**: First name, last name, email, phone, password, confirm password
- **Signin Page**: Email and password authentication
- **Dashboard**: User details display with logout functionality

### 🎨 Modern UI/UX
- **Tailwind CSS**: Utility-first CSS framework for rapid styling
- **Glass Morphism**: Modern glass card design with backdrop blur
- **Smooth Animations**: Fade-in, bounce-in, slide-out transitions
- **Loading States**: Spinner animations during form submission
- **Form Validation**: Real-time validation with error messages
- **Responsive Design**: Works on all device sizes

### ⚡ Technical Features
- **React + Vite**: Fast development and build tooling
- **Local Storage**: Persistent user data storage
- **Custom Hooks**: Reusable authentication logic
- **Component Architecture**: Modular and maintainable code structure
- **Form Handling**: Controlled components with validation

## Project Structure

```
react-auth-app/
├── src/
│   ├── components/
│   │   ├── SignupForm.jsx      # Signup form with validation
│   │   ├── SigninForm.jsx      # Signin form with authentication
│   │   ├── Dashboard.jsx       # User dashboard with details
│   │   └── LoadingSpinner.jsx  # Loading animation component
│   ├── hooks/
│   │   └── useAuth.js          # Authentication hook
│   ├── utils/
│   │   └── validation.js       # Form validation utilities
│   ├── App.jsx                 # Main application component
│   ├── main.jsx               # React entry point
│   └── index.css              # Tailwind CSS with custom styles
├── tailwind.config.js         # Tailwind configuration
├── postcss.config.js          # PostCSS configuration
└── package.json               # Dependencies and scripts
```

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd react-auth-app
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5173`

### Build for Production

```bash
npm run build
```

## Usage Flow

1. **Initial Load** → Signup page is displayed
2. **After Signup** → Automatically transitions to signin page with email pre-filled
3. **After Signin** → Dashboard displays user details and logout option
4. **Logout** → Returns to signup page with slide-out animation

## Validation Rules

- **Names**: Minimum 2 characters
- **Email**: Valid email format, unique registration
- **Phone**: Valid phone number format
- **Password**: Minimum 6 characters
- **Confirm Password**: Must match password

## Animations

- **Page Transitions**: Bounce-in effect for smooth page changes
- **Form Interactions**: Hover and focus states with subtle transforms
- **Loading States**: Spinning loader during form submission
- **Error Messages**: Fade-in animation for validation errors
- **Logout**: Slide-out animation before page transition

## Customization

### Colors
Edit `tailwind.config.js` to customize the color scheme:

```javascript
theme: {
  extend: {
    colors: {
      // Add custom colors here
    }
  }
}
```

### Animations
Add custom animations in `tailwind.config.js`:

```javascript
animation: {
  'custom-animation': 'customKeyframe 1s ease-in-out',
}
```

## Technologies Used

- **React 18**: Modern React with hooks
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **PostCSS**: CSS processing tool
- **Local Storage**: Browser storage for data persistence

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - feel free to use this project for learning and development purposes.