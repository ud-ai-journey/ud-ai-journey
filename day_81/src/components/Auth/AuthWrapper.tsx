import React, { useState } from 'react'
import { LoginForm } from './LoginForm'
import { SignUpForm } from './SignUpForm'

export function AuthWrapper() {
  const [isLogin, setIsLogin] = useState(true)

  const toggleMode = () => setIsLogin(!isLogin)

  return isLogin ? (
    <LoginForm onToggleMode={toggleMode} />
  ) : (
    <SignUpForm onToggleMode={toggleMode} />
  )
}