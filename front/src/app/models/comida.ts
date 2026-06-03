export type CategoriaComida =
  | 'frutas_verduras'
  | 'cereales_legumbres'
  | 'proteinas'
  | 'lacteos'
  | 'grasas_saludables'
  | 'preparacion';

export interface Comida {
  id_comida: number;
  nombre: string;
  categoria: CategoriaComida;
  porcion_referencia: string;
  calorias: string;
  proteinas: string;
  carbohidratos: string;
  grasas: string;
}
