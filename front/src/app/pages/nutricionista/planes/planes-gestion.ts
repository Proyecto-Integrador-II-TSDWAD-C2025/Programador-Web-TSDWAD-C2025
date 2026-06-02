import { ChangeDetectionStrategy, Component, inject, OnInit, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { Plan } from '../../../models';
import { PlanService } from '../../../services/plan.service';

@Component({
  selector: 'app-planes-gestion',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './planes-gestion.html',
  styleUrl: '../gestion-nutricionista.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PlanesGestion implements OnInit {
  private planService = inject(PlanService);

  planes = signal<Plan[]>([]);
  cargando = signal(true);
  guardando = signal(false);
  mensaje = signal('');
  error = signal('');
  planEditando = signal<number | null>(null);

  planForm = new FormGroup({
    nombre_plan: new FormControl('', [Validators.required, Validators.maxLength(100)]),
    descripcion: new FormControl('', [Validators.required, Validators.maxLength(800)]),
    duracion_dias: new FormControl<number | null>(null, [Validators.required, Validators.min(1), Validators.max(365)]),
    calorias_objetivo: new FormControl<number | null>(null, [Validators.required, Validators.min(500), Validators.max(6000)]),
  });

  ngOnInit() {
    this.cargarPlanes();
  }

  guardar() {
    if (this.planForm.invalid) {
      this.planForm.markAllAsTouched();
      return;
    }

    const value = this.planForm.getRawValue();
    const payload = {
      nombre_plan: value.nombre_plan!,
      descripcion: value.descripcion!,
      duracion_dias: value.duracion_dias!,
      calorias_objetivo: String(value.calorias_objetivo),
    };
    const id = this.planEditando();
    const request = id ? this.planService.updatePlan(id, payload) : this.planService.createPlan(payload);

    this.guardando.set(true);
    this.error.set('');
    request.subscribe({
      next: () => {
        this.mensaje.set(id ? 'Plan actualizado correctamente.' : 'Plan creado correctamente.');
        this.cancelarEdicion();
        this.cargarPlanes();
      },
      error: () => {
        this.error.set('No se pudo guardar el plan. Revisá los datos e intentá nuevamente.');
        this.guardando.set(false);
      },
    });
  }

  editar(plan: Plan) {
    this.planEditando.set(plan.id_plan);
    this.mensaje.set('');
    this.error.set('');
    this.planForm.setValue({
      nombre_plan: plan.nombre_plan,
      descripcion: plan.descripcion,
      duracion_dias: plan.duracion_dias,
      calorias_objetivo: Number(plan.calorias_objetivo),
    });
  }

  eliminar(plan: Plan) {
    if (!confirm(`¿Eliminar el plan "${plan.nombre_plan}"?`)) {
      return;
    }

    this.planService.deletePlan(plan.id_plan).subscribe({
      next: () => {
        this.mensaje.set('Plan eliminado correctamente.');
        this.cargarPlanes();
      },
      error: () => this.error.set('No se pudo eliminar el plan. Puede estar asignado a un usuario.'),
    });
  }

  cancelarEdicion() {
    this.planEditando.set(null);
    this.guardando.set(false);
    this.planForm.reset();
  }

  campoInvalido(nombre: string): boolean {
    const campo = this.planForm.get(nombre);
    return !!campo && campo.invalid && campo.touched;
  }

  private cargarPlanes() {
    this.cargando.set(true);
    this.planService.getPlanes().subscribe({
      next: (planes) => {
        this.planes.set(planes);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudieron cargar los planes.');
        this.cargando.set(false);
        this.guardando.set(false);
      },
    });
  }
}
