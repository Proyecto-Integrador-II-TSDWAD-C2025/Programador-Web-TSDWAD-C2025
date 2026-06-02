import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { PlanService } from '../../services/plan.service';
import { NivelActividadPlan, ObjetivoPlan, Plan } from '../../models';
import { ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'app-planes',
  imports: [CommonModule, RouterLink],
  templateUrl: './planes.html',
  styleUrl: './planes.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Planes implements OnInit {
  private planService = inject(PlanService);

  planes = signal<Plan[]>([]);
  cargando = signal(true);
  error = signal('');

  ngOnInit() {
    this.planService.getPlanes().subscribe({
      next: (planes) => {
        this.planes.set(planes);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('Error al cargar los planes. Intentá de nuevo.');
        this.cargando.set(false);
      }
    });
  }

  etiquetaObjetivo(objetivo: ObjetivoPlan): string {
    const etiquetas: Record<ObjetivoPlan, string> = {
      bajar_grasa: 'Bajar grasa corporal',
      mantener_peso: 'Mantener peso',
      aumentar_masa: 'Aumentar masa muscular',
      mejorar_habitos: 'Mejorar habitos saludables',
    };
    return etiquetas[objetivo];
  }

  etiquetaActividad(nivel: NivelActividadPlan): string {
    const etiquetas: Record<NivelActividadPlan, string> = {
      bajo: 'Actividad baja',
      moderado: 'Actividad moderada',
      alto: 'Actividad alta',
    };
    return etiquetas[nivel];
  }
}
