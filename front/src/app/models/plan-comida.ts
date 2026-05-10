import { Plan } from './plan';
import { Comida } from './comida';

export interface PlanComida {
  id_plan_comida: number;
  id_plan: number | Plan;
  id_comida: number | Comida;
  tipo_comida: string;
}