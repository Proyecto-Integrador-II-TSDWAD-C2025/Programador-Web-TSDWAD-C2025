export interface EjercicioRutina {
  id_ejercicio: number;
  dia: number;
  orden: number;
  nombre: string;
  descripcion: string;
  series: number | null;
  repeticiones: string;
  duracion_minutos: number | null;
  completado_hoy: boolean;
}

export interface Rutina {
  id_rutina: number;
  nombre: string;
  descripcion: string;
  objetivo: string;
  nivel: string;
  dias_por_semana: number;
  duracion_semanas: number;
  ejercicios: EjercicioRutina[];
}

export interface UsuarioRutina {
  id_usuario_rutina: number;
  motivo: string;
  fecha_asignacion: string;
  rutina: Rutina;
}

export interface MiRutinaResponse {
  requiere_revision: boolean;
  mensaje: string;
  asignacion: UsuarioRutina | null;
}

export interface CompletarEjercicioResponse {
  ejercicio_id: number;
  completado_hoy: boolean;
}
