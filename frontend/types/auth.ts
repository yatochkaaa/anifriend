export interface Token {
  accessToken: string
  tokenType: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface UserCreate {
  email: string
  username: string
  password: string
  password_repeat: string
  date_of_birth: string // YYYY-MM-DD
}

export interface UserCreateFormData {
  email: string
  username: string
  password: string
  passwordRepeat: string
  dateOfBirth: Date
}

export interface UserLogin {
  username: string
  password: string
}
