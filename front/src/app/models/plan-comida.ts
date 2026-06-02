import { Plan } from './plan';
import { Comida } from './comida';

export interface PlanComida {
  id_plan_comida: number;
  id_plan: number | Plan;
  id_comida: number | Comida;
  dia: number;
  orden: number;
  tipo_comida: string;
  porcion: string;
  alternativa: string;
  completada_hoy?: boolean;
}
