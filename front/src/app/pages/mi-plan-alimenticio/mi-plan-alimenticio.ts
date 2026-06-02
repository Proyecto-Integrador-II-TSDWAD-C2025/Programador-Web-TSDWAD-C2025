import { ChangeDetectionStrategy, Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { MiPlanAlimenticioResponse, PlanComida, PerfilUsuario } from '../../models';
import { PlanAlimenticioService } from '../../services/plan-alimenticio.service';
import { PerfilService } from '../../services/perfil.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-mi-plan-alimenticio',
  imports: [RouterLink],
  templateUrl: './mi-plan-alimenticio.html',
  styleUrl: './mi-plan-alimenticio.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MiPlanAlimenticio implements OnInit {
  private planAlimenticioService = inject(PlanAlimenticioService);
  private perfilService = inject(PerfilService);

  respuesta = signal<MiPlanAlimenticioResponse | null>(null);
  perfil = signal<PerfilUsuario | null>(null);
  cargando = signal(true);
  error = signal('');
  actualizando = signal<number | null>(null);

  ngOnInit(): void {
    this.cargarPlan();
    this.cargarPerfil();
  }

  dias(): number[] {
    return [...new Set((this.respuesta()?.asignacion?.plan.comidas_plan ?? []).map((item) => item.dia))];
  }

  comidasDelDia(dia: number): PlanComida[] {
    return this.respuesta()?.asignacion?.plan.comidas_plan.filter((item) => item.dia === dia) ?? [];
  }

  nombreComida(item: PlanComida): string {
    return typeof item.id_comida === 'number' ? `Comida #${item.id_comida}` : item.id_comida.nombre;
  }

  totalComidas(): number {
    return this.respuesta()?.asignacion?.plan.comidas_plan.length ?? 0;
  }

  comidasCompletadas(): number {
    return this.respuesta()?.asignacion?.plan.comidas_plan.filter((item) => item.completada_hoy).length ?? 0;
  }

  alternarComida(planComidaId: number): void {
    this.actualizando.set(planComidaId);
    this.planAlimenticioService.alternarComida(planComidaId).subscribe({
      next: ({ completada_hoy }) => {
        this.respuesta.update((respuesta) => {
          const asignacion = respuesta?.asignacion;
          if (!respuesta || !asignacion) {
            return respuesta;
          }

          return {
            ...respuesta,
            asignacion: {
              ...asignacion,
              plan: {
                ...asignacion.plan,
                comidas_plan: asignacion.plan.comidas_plan.map((item) =>
                  item.id_plan_comida === planComidaId ? { ...item, completada_hoy } : item
                ),
              },
            },
          };
        });
        this.actualizando.set(null);
        
        const Toast = Swal.mixin({
          toast: true,
          position: "top-end",
          showConfirmButton: false,
          timer: 3000,
          timerProgressBar: true
        });
        Toast.fire({
          icon: completada_hoy ? 'success' : 'info',
          title: completada_hoy ? '¡Comida registrada!' : 'Registro deshecho'
        });
      },
      error: () => {
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'No pudimos actualizar la comida. Intenta nuevamente.',
          confirmButtonColor: '#2d7a3a'
        });
        this.error.set('No pudimos actualizar la comida. Intenta nuevamente.');
        this.actualizando.set(null);
      },
    });
  }

  private cargarPlan(): void {
    this.planAlimenticioService.getMiPlan().subscribe({
      next: (respuesta) => {
        this.respuesta.set(respuesta);
        this.cargando.set(false);
      },
      error: (error) => {
        const msg = error.status === 404
            ? 'Completa tu perfil para obtener una orientacion alimenticia.'
            : 'No pudimos cargar tu plan alimenticio.';
        this.error.set(msg);
        this.cargando.set(false);
        
        if (error.status === 404) {
          Swal.fire({
            icon: 'warning',
            title: 'Perfil Incompleto',
            text: msg,
            confirmButtonColor: '#2d7a3a'
          });
        }
      },
    });
  }

  private cargarPerfil(): void {
    this.perfilService.getPerfil().subscribe({
      next: ({ perfil }) => {
        this.perfil.set(perfil);
      },
      error: () => {}
    });
  }
}
