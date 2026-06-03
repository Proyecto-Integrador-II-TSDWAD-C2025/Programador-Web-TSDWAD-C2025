import { ChangeDetectionStrategy, Component, inject, OnInit, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { NivelActividadPlan, ObjetivoPlan, Plan, PreferenciaCompatiblePlan } from '../../../models';
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

  objetivos: { value: ObjetivoPlan; label: string }[] = [
    { value: 'bajar_grasa', label: 'Bajar grasa corporal' },
    { value: 'mantener_peso', label: 'Mantener peso' },
    { value: 'aumentar_masa', label: 'Aumentar masa muscular' },
    { value: 'mejorar_habitos', label: 'Mejorar habitos saludables' },
  ];
  nivelesActividad: { value: NivelActividadPlan; label: string }[] = [
    { value: 'bajo', label: 'Bajo' },
    { value: 'moderado', label: 'Moderado' },
    { value: 'alto', label: 'Alto' },
  ];
  preferencias: { value: PreferenciaCompatiblePlan; label: string }[] = [
    { value: 'todas', label: 'Todas las preferencias' },
    { value: 'vegetariana', label: 'Vegetariana' },
    { value: 'alta_proteina', label: 'Alta en proteinas' },
    { value: 'baja_calorias', label: 'Baja en calorias' },
  ];

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
    objetivo: new FormControl<ObjetivoPlan | ''>('', [Validators.required]),
    nivel_actividad: new FormControl<NivelActividadPlan | ''>('', [Validators.required]),
    preferencia_compatible: new FormControl<PreferenciaCompatiblePlan>('todas', [Validators.required]),
    observaciones: new FormControl('', [Validators.maxLength(1000)]),
    activo: new FormControl(true, { nonNullable: true }),
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
      objetivo: value.objetivo as ObjetivoPlan,
      nivel_actividad: value.nivel_actividad as NivelActividadPlan,
      preferencia_compatible: value.preferencia_compatible as PreferenciaCompatiblePlan,
      observaciones: value.observaciones ?? '',
      activo: value.activo,
    };
    const id = this.planEditando();
    const request = id ? this.planService.updatePlan(id, payload) : this.planService.createPlan(payload);

    this.guardando.set(true);
    this.error.set('');
    request.subscribe({
      next: () => {
        this.mensaje.set(id ? 'Plantilla actualizada correctamente.' : 'Plantilla creada correctamente.');
        this.cancelarEdicion();
        this.cargarPlanes();
      },
      error: () => {
        this.error.set('No se pudo guardar la plantilla. Revisá los datos e intentá nuevamente.');
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
      objetivo: plan.objetivo,
      nivel_actividad: plan.nivel_actividad,
      preferencia_compatible: plan.preferencia_compatible,
      observaciones: plan.observaciones,
      activo: plan.activo,
    });
  }

  eliminar(plan: Plan) {
    if (!confirm(`¿Eliminar la plantilla "${plan.nombre_plan}"?`)) {
      return;
    }

    this.planService.deletePlan(plan.id_plan).subscribe({
      next: () => {
        this.mensaje.set('Plantilla eliminada correctamente.');
        this.cargarPlanes();
      },
      error: () => this.error.set('No se pudo eliminar la plantilla. Puede estar asignada a un usuario.'),
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

  etiquetaObjetivo(objetivo: ObjetivoPlan): string {
    return this.objetivos.find(opcion => opcion.value === objetivo)?.label ?? objetivo;
  }

  etiquetaActividad(nivel: NivelActividadPlan): string {
    return this.nivelesActividad.find(opcion => opcion.value === nivel)?.label ?? nivel;
  }

  etiquetaPreferencia(preferencia: PreferenciaCompatiblePlan): string {
    return this.preferencias.find(opcion => opcion.value === preferencia)?.label ?? preferencia;
  }

  private cargarPlanes() {
    this.cargando.set(true);
    this.planService.getPlanes().subscribe({
      next: (planes) => {
        this.planes.set(planes);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudieron cargar las plantillas.');
        this.cargando.set(false);
        this.guardando.set(false);
      },
    });
  }
}
