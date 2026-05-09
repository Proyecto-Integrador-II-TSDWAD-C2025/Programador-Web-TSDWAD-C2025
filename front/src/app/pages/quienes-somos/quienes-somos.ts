import { Component } from '@angular/core';

@Component({
  selector: 'app-quienes-somos',
  imports: [],
  templateUrl: './quienes-somos.html',
  styleUrl: './quienes-somos.css',
})
export class QuienesSomosComponent {
  servicios = [
    {
      titulo: 'Planes alimenticios',
      descripcion:
        'Recomendaciones de alimentación adaptadas a los objetivos y necesidades del usuario.'
    },
    {
      titulo: 'Rutinas de entrenamiento',
      descripcion:
        'Ejercicios organizados según el objetivo físico, nivel de actividad y progreso del usuario.'
    },
    {
      titulo: 'Seguimiento personalizado',
      descripcion:
        'Visualización de objetivos, planes, progreso y datos importantes desde un panel personalizado.'
    },
    {
      titulo: 'Conexión con nutricionistas',
      descripcion:
        'Posibilidad de recibir acompañamiento profesional para mejorar la experiencia del usuario.'
    }
  ];

  beneficios = [
    {
      titulo: 'Todo en un solo lugar',
      descripcion:
        'NutriApp reúne alimentación, entrenamiento y seguimiento dentro de una misma plataforma.'
    },
    {
      titulo: 'Experiencia intuitiva',
      descripcion:
        'La interfaz está pensada para que cualquier usuario pueda utilizarla de forma simple.'
    },
    {
      titulo: 'Adaptado al usuario',
      descripcion:
        'La información se organiza según el perfil, objetivo físico y plan seleccionado.'
    }
  ];
}