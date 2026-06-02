import { PlanComida } from './plan-comida';

export type ObjetivoPlan = 'bajar_grasa' | 'mantener_peso' | 'aumentar_masa' | 'mejorar_habitos';
export type NivelActividadPlan = 'bajo' | 'moderado' | 'alto';
export type PreferenciaCompatiblePlan = 'todas' | 'vegetariana' | 'alta_proteina' | 'baja_calorias';

export interface Plan {
  id_plan: number;
  codigo: string | null;
  nombre_plan: string;
  descripcion: string;
  duracion_dias: number;
  calorias_objetivo: string;
  objetivo: ObjetivoPlan;
  nivel_actividad: NivelActividadPlan;
  preferencia_compatible: PreferenciaCompatiblePlan;
  observaciones: string;
  activo: boolean;
}

export interface PlanDetalle extends Plan {
  comidas_plan: PlanComida[];
}
