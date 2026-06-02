import { ChangeDetectionStrategy, Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { MiPlanAlimenticioResponse, PlanComida } from '../../models';
import { PlanAlimenticioService } from '../../services/plan-alimenticio.service';

@Component({
  selector: 'app-mi-plan-alimenticio',
  imports: [RouterLink],
  templateUrl: './mi-plan-alimenticio.html',
  styleUrl: './mi-plan-alimenticio.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MiPlanAlimenticio implements OnInit {
  private planAlimenticioService = inject(PlanAlimenticioService);

  respuesta = signal<MiPlanAlimenticioResponse | null>(null);
  cargando = signal(true);
  error = signal('');
  actualizando = signal<number | null>(null);

  ngOnInit(): void {
    this.cargarPlan();
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
      },
      error: () => {
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
        this.error.set(
          error.status === 404
            ? 'Completa tu perfil para obtener una orientacion alimenticia.'
            : 'No pudimos cargar tu plan alimenticio.'
        );
        this.cargando.set(false);
      },
    });
  }
}
