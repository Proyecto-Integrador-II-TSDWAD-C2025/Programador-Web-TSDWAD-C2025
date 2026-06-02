export type ObjetivoPerfil = 'bajar_grasa' | 'aumentar_masa' | 'mantener_peso' | 'mejorar_habitos';
export type ActividadPerfil = 'bajo' | 'moderado' | 'alto';
export type PreferenciaPerfil = 'sin_preferencia' | 'vegetariana' | 'alta_proteina' | 'baja_calorias';

export interface PerfilPayload {
  edad: number;
  peso_actual: number;
  altura_cm: number;
  peso_objetivo: number;
  objetivo: ObjetivoPerfil;
  actividad: ActividadPerfil;
  preferencia: PreferenciaPerfil;
  dias_entrenamiento: number;
  limitaciones: string;
  consideraciones_alimentarias: string;
}

export interface PerfilUsuario extends Omit<PerfilPayload, 'peso_actual' | 'peso_objetivo'> {
  id_perfil: number;
  peso_actual: string;
  peso_objetivo: string;
  fecha_actualizacion: string;
}

export interface PerfilResponse {
  perfil: PerfilUsuario;
  requiere_revision: boolean;
  mensaje: string;
}
