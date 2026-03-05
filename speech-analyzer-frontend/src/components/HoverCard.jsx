import { forwardRef } from 'react'

/**
 * Reusable Card wrapper component with subtle hover effects
 * 
 * @param {Object} props - Component props
 * @param {string} props.className - Additional CSS classes
 * @param {React.ReactNode} props.children - Card content
 * @param {boolean} props.interactive - Whether card should have interactive hover effects
 * @param {string} props.variant - Card variant: 'default', 'glass', 'elevated'
 * @param {function} props.onClick - Click handler for interactive cards
 */
const HoverCard = forwardRef(({ 
  className = '', 
  children, 
  interactive = false,
  variant = 'default',
  onClick,
  ...props 
}, ref) => {
  
  const baseClasses = "transition-all duration-300 ease-out"
  
  const variantClasses = {
    default: "bg-white rounded-xl border border-gray-200",
    glass: "glass-card rounded-3xl",
    elevated: "bg-white rounded-xl shadow-sm border border-gray-100"
  }
  
  const hoverClasses = interactive 
    ? "hover:shadow-lg hover:-translate-y-1 hover:scale-[1.01] cursor-pointer active:scale-[0.99] active:translate-y-0"
    : "hover:shadow-md hover:-translate-y-0.5"
  
  const combinedClasses = `
    ${baseClasses}
    ${variantClasses[variant]}
    ${hoverClasses}
    ${className}
  `.trim()

  return (
    <div
      ref={ref}
      className={combinedClasses}
      onClick={onClick}
      {...props}
    >
      {children}
    </div>
  )
})

HoverCard.displayName = 'HoverCard'

export default HoverCard