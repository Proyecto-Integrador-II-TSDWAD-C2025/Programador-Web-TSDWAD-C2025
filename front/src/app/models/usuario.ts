import { Rol } from './rol';

export interface Usuario {
  id_usuario: number;
  nombre: string;
  apellido: string;
  email: string;
  contrasena?: string;
  fecha_registro?: string;
  id_rol: number | Rol;
}

export interface UsuarioRead {
  id_usuario: number;
  nombre: string;
  apellido: string;
  email: string;
  fecha_registro: string;
  id_rol: Rol;
}

export interface LoginRequest {
  email: string;
  contrasena: string;
}

export interface RegistroRequest {
  nombre: string;
  apellido: string;
  email: string;
  contrasena: string;
  id_rol: number;
}