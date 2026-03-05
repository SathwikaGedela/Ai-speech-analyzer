export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

export const validatePhone = (phone) => {
  const re = /^[\+]?[1-9][\d]{0,15}$/
  return re.test(phone.replace(/\s/g, ''))
}

export const validatePassword = (password) => {
  return password.length >= 6
}

export const validateName = (name) => {
  return name.trim().length >= 2
}

export const validateRequired = (value) => {
  return value && value.trim().length > 0
}