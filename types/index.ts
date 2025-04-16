// User related types
export interface User {
  id: number;
  cedula: string;
  nombre: string;
  apellido: string;
  fecha_de_nacimiento: string;
  email: string;
  password?: string;
  reset_token?: string | null;
  reset_expires?: Date | null;
  created_at?: Date;
  updated_at?: Date;
}

export interface JWTPayload {
  id: number;
  cedula: string;
  nombre: string;
  apellido: string;
  email: string;
  iat?: number;
  exp?: number;
}

export interface DatabaseResult {
  [key: string]: any;
}

export interface QueryResult extends Array<DatabaseResult> {}
