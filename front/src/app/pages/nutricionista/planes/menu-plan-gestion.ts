import { ChangeDetectionStrategy, Component, OnInit, inject, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import { Comida, PlanComida, PlanDetalle } from '../../../models';
import { ComidaService } from '../../../services/comida.service';
import { PlanComidaService } from '../../../services/plan-comida.service';
import { PlanService } from '../../../services/plan.service';

@Component({
  selector: 'app-menu-plan-gestion',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './menu-plan-gestion.html',
  styleUrls: ['../gestion-nutricionista.css', './menu-plan-gestion.css'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MenuPlanGestion implements OnInit {
  private route = inject(ActivatedRoute);
  private planService = inject(PlanService);
  private comidaService = inject(ComidaService);
  private planComidaService = inject(PlanComidaService);

  planId = Number(this.route.snapshot.paramMap.get('id'));
  plan = signal<PlanDetalle | null>(null);
  comidas = signal<Comida[]>([]);
  menu = signal<PlanComida[]>([]);
  cargando = signal(true);
  guardando = signal(false);
  mensaje = signal('');
  error = signal('');

  menuForm = new FormGroup({
    dia: new FormControl<number | null>(1, [Validators.required, Validators.min(1), Validators.max(7)]),
    orden: new FormControl<number | null>(1, [Validators.required, Validators.min(1), Validators.max(10)]),
    tipo_comida: new FormControl('desayuno', [Validators.required]),
    id_comida: new FormControl<number | null>(null, [Validators.required]),
    porcion: new FormControl('', [Validators.required, Validators.maxLength(100)]),
    alternativa: new FormControl('', [Validators.maxLength(255)]),
  });

  ngOnInit(): void {
    this.cargarDatos();
  }

  dias(): number[] {
    return [...new Set(this.menu().map((item) => item.dia))];
  }

  comidasDelDia(dia: number): PlanComida[] {
    return this.menu().filter((item) => item.dia === dia);
  }

  nombreComida(item: PlanComida): string {
    return typeof item.id_comida === 'number' ? `Comida #${item.id_comida}` : item.id_comida.nombre;
  }

  guardar(): void {
    if (this.menuForm.invalid) {
      this.menuForm.markAllAsTouched();
      return;
    }

    const value = this.menuForm.getRawValue();
    this.guardando.set(true);
    this.error.set('');
    this.planComidaService.createPlanComida({
      id_plan: this.planId,
      id_comida: Number(value.id_comida),
      dia: value.dia!,
      orden: value.orden!,
      tipo_comida: value.tipo_comida!,
      porcion: value.porcion!,
      alternativa: value.alternativa ?? '',
    }).subscribe({
      next: () => {
        this.mensaje.set('Comida agregada al menu.');
        this.menuForm.reset({ dia: 1, orden: 1, tipo_comida: 'desayuno' });
        this.cargarMenu();
      },
      error: () => {
        this.error.set('No se pudo agregar la comida. Revisa los datos.');
        this.guardando.set(false);
      },
    });
  }

  eliminar(item: PlanComida): void {
    if (!confirm(`Eliminar "${this.nombreComida(item)}" del dia ${item.dia}?`)) {
      return;
    }

    this.planComidaService.deletePlanComida(item.id_plan_comida).subscribe({
      next: () => {
        this.mensaje.set('Comida eliminada del menu.');
        this.cargarMenu();
      },
      error: () => this.error.set('No se pudo eliminar la comida del menu.'),
    });
  }

  campoInvalido(nombre: string): boolean {
    const campo = this.menuForm.get(nombre);
    return !!campo && campo.invalid && campo.touched;
  }

  private cargarDatos(): void {
    forkJoin({
      plan: this.planService.getPlan(this.planId),
      comidas: this.comidaService.getComidas(),
      menu: this.planComidaService.getComidasPorPlan(this.planId),
    }).subscribe({
      next: ({ plan, comidas, menu }) => {
        this.plan.set(plan);
        this.comidas.set(comidas);
        this.menu.set(menu);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudo cargar el menu de la plantilla.');
        this.cargando.set(false);
      },
    });
  }

  private cargarMenu(): void {
    this.planComidaService.getComidasPorPlan(this.planId).subscribe({
      next: (menu) => {
        this.menu.set(menu);
        this.guardando.set(false);
      },
      error: () => {
        this.error.set('No se pudo actualizar el menu.');
        this.guardando.set(false);
      },
    });
  }
}
