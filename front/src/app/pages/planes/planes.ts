import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlanService } from '../../services/plan.service';
import { Plan } from '../../models';
import { ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'app-planes',
  imports: [CommonModule],
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
}