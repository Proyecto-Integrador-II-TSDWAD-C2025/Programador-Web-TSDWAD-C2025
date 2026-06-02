import { ChangeDetectionStrategy, Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { PlanComida, PlanDetalle as PlanDetalleModel } from '../../models';
import { PlanService } from '../../services/plan.service';

@Component({
  selector: 'app-plan-detalle',
  imports: [RouterLink],
  templateUrl: './plan-detalle.html',
  styleUrls: ['../mi-plan-alimenticio/mi-plan-alimenticio.css'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PlanDetalle implements OnInit {
  private route = inject(ActivatedRoute);
  private planService = inject(PlanService);

  plan = signal<PlanDetalleModel | null>(null);
  cargando = signal(true);
  error = signal('');

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.planService.getPlan(id).subscribe({
      next: (plan) => {
        this.plan.set(plan);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No pudimos cargar el detalle de esta plantilla.');
        this.cargando.set(false);
      },
    });
  }

  dias(): number[] {
    return [...new Set((this.plan()?.comidas_plan ?? []).map((item) => item.dia))];
  }

  comidasDelDia(dia: number): PlanComida[] {
    return this.plan()?.comidas_plan.filter((item) => item.dia === dia) ?? [];
  }

  nombreComida(item: PlanComida): string {
    return typeof item.id_comida === 'number' ? `Comida #${item.id_comida}` : item.id_comida.nombre;
  }
}
