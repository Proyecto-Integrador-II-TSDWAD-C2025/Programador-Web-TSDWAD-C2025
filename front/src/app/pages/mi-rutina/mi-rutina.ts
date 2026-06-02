import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { EjercicioRutina, MiRutinaResponse } from '../../models';
import { RutinaService } from '../../services/rutina.service';

@Component({
  selector: 'app-mi-rutina',
  imports: [CommonModule, RouterLink],
  templateUrl: './mi-rutina.html',
  styleUrl: './mi-rutina.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MiRutina implements OnInit {
  private rutinaService = inject(RutinaService);

  respuesta = signal<MiRutinaResponse | null>(null);
  cargando = signal(true);
  mensajeError = signal('');
  actualizando = signal<number | null>(null);

  ngOnInit(): void {
    this.cargarRutina();
  }

  cargarRutina(): void {
    this.cargando.set(true);
    this.mensajeError.set('');
    this.rutinaService.getMiRutina().subscribe({
      next: (respuesta) => {
        this.respuesta.set(respuesta);
        this.cargando.set(false);
      },
      error: (error) => {
        this.mensajeError.set(
          error.status === 404
            ? 'Completa tu perfil para que podamos recomendarte una rutina inicial.'
            : 'No pudimos cargar tu rutina. Intenta nuevamente.'
        );
        this.cargando.set(false);
      },
    });
  }

  dias(): number[] {
    const ejercicios = this.respuesta()?.asignacion?.rutina.ejercicios ?? [];
    return [...new Set(ejercicios.map((ejercicio) => ejercicio.dia))];
  }

  ejerciciosDelDia(dia: number): EjercicioRutina[] {
    return this.respuesta()?.asignacion?.rutina.ejercicios.filter((ejercicio) => ejercicio.dia === dia) ?? [];
  }

  totalEjercicios(): number {
    return this.respuesta()?.asignacion?.rutina.ejercicios.length ?? 0;
  }

  ejerciciosCompletados(): number {
    return this.respuesta()?.asignacion?.rutina.ejercicios.filter((ejercicio) => ejercicio.completado_hoy).length ?? 0;
  }

  detalleEjercicio(ejercicio: EjercicioRutina): string {
    if (ejercicio.duracion_minutos) {
      return `${ejercicio.duracion_minutos} min`;
    }

    if (ejercicio.series && ejercicio.repeticiones) {
      return `${ejercicio.series} series x ${ejercicio.repeticiones}`;
    }

    return ejercicio.repeticiones;
  }

  alternarEjercicio(ejercicioId: number): void {
    this.actualizando.set(ejercicioId);
    this.rutinaService.alternarEjercicio(ejercicioId).subscribe({
      next: ({ completado_hoy }) => {
        this.respuesta.update((respuesta) => {
          const asignacion = respuesta?.asignacion;
          if (!respuesta || !asignacion) {
            return respuesta;
          }

          return {
            ...respuesta,
            asignacion: {
              ...asignacion,
              rutina: {
                ...asignacion.rutina,
                ejercicios: asignacion.rutina.ejercicios.map((ejercicio) =>
                  ejercicio.id_ejercicio === ejercicioId
                    ? { ...ejercicio, completado_hoy }
                    : ejercicio
                ),
              },
            },
          };
        });
        this.actualizando.set(null);
      },
      error: () => {
        this.mensajeError.set('No pudimos actualizar el ejercicio. Intenta nuevamente.');
        this.actualizando.set(null);
      },
    });
  }
}
