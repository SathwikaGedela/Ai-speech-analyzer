import EnhancedLoadingSpinner from './EnhancedLoadingSpinner'

const LoadingSpinner = ({ size = 'medium', message = 'Loading...', showMessage = true }) => {
  return <EnhancedLoadingSpinner size={size} message={message} showMessage={showMessage} />
}

export default LoadingSpinner