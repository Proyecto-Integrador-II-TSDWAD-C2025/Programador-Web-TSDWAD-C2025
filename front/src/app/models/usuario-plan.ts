import { UsuarioRead } from './usuario';
import { Plan } from './plan';

export interface UsuarioPlan {
  id_usuario_plan: number;
  id_usuario: number | UsuarioRead;
  id_plan: number | Plan;
  fecha_inicio: string;
  fecha_fin: string;
  estado: string;
}