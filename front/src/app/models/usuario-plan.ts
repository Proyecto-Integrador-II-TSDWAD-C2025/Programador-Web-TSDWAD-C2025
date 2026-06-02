import { UsuarioRead } from './usuario';
import { Plan, PlanDetalle } from './plan';

export interface UsuarioPlan {
  id_usuario_plan: number;
  id_usuario: number | UsuarioRead;
  id_plan: number | Plan;
  fecha_inicio: string;
  fecha_fin: string;
  estado: string;
  origen: 'orientativo' | 'profesional';
  motivo: string;
}

export interface UsuarioPlanDetalle extends Omit<UsuarioPlan, 'id_plan' | 'id_usuario'> {
  plan: PlanDetalle;
}

export interface MiPlanAlimenticioResponse {
  requiere_revision: boolean;
  mensaje: string;
  asignacion: UsuarioPlanDetalle | null;
}

export interface CompletarComidaPlanResponse {
  plan_comida_id: number;
  completada_hoy: boolean;
}
