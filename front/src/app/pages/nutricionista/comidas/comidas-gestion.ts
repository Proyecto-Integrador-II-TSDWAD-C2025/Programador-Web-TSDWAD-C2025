import { ChangeDetectionStrategy, Component, inject, OnInit, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CategoriaComida, Comida } from '../../../models';
import { ComidaService } from '../../../services/comida.service';

@Component({
  selector: 'app-comidas-gestion',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './comidas-gestion.html',
  styleUrl: '../gestion-nutricionista.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ComidasGestion implements OnInit {
  private comidaService = inject(ComidaService);

  comidas = signal<Comida[]>([]);
  cargando = signal(true);
  guardando = signal(false);
  mensaje = signal('');
  error = signal('');
  comidaEditando = signal<number | null>(null);
  categorias: { value: CategoriaComida; label: string }[] = [
    { value: 'preparacion', label: 'Preparacion completa' },
    { value: 'frutas_verduras', label: 'Frutas y verduras' },
    { value: 'cereales_legumbres', label: 'Cereales y legumbres' },
    { value: 'proteinas', label: 'Proteinas' },
    { value: 'lacteos', label: 'Lacteos' },
    { value: 'grasas_saludables', label: 'Grasas saludables' },
  ];

  comidaForm = new FormGroup({
    nombre: new FormControl('', [Validators.required, Validators.maxLength(100)]),
    categoria: new FormControl<CategoriaComida>('preparacion', [Validators.required]),
    porcion_referencia: new FormControl('', [Validators.required, Validators.maxLength(100)]),
    calorias: new FormControl<number | null>(null, [Validators.required, Validators.min(0), Validators.max(5000)]),
    proteinas: new FormControl<number | null>(null, [Validators.required, Validators.min(0), Validators.max(500)]),
    carbohidratos: new FormControl<number | null>(null, [Validators.required, Validators.min(0), Validators.max(1000)]),
    grasas: new FormControl<number | null>(null, [Validators.required, Validators.min(0), Validators.max(500)]),
  });

  ngOnInit() {
    this.cargarComidas();
  }

  guardar() {
    if (this.comidaForm.invalid) {
      this.comidaForm.markAllAsTouched();
      return;
    }

    const value = this.comidaForm.getRawValue();
    const payload = {
      nombre: value.nombre!,
      categoria: value.categoria as CategoriaComida,
      porcion_referencia: value.porcion_referencia!,
      calorias: String(value.calorias),
      proteinas: String(value.proteinas),
      carbohidratos: String(value.carbohidratos),
      grasas: String(value.grasas),
    };
    const id = this.comidaEditando();
    const request = id ? this.comidaService.updateComida(id, payload) : this.comidaService.createComida(payload);

    this.guardando.set(true);
    this.error.set('');
    request.subscribe({
      next: () => {
        this.mensaje.set(id ? 'Comida actualizada correctamente.' : 'Comida creada correctamente.');
        this.cancelarEdicion();
        this.cargarComidas();
      },
      error: () => {
        this.error.set('No se pudo guardar la comida. Revisá los datos e intentá nuevamente.');
        this.guardando.set(false);
      },
    });
  }

  editar(comida: Comida) {
    this.comidaEditando.set(comida.id_comida);
    this.mensaje.set('');
    this.error.set('');
    this.comidaForm.setValue({
      nombre: comida.nombre,
      categoria: comida.categoria,
      porcion_referencia: comida.porcion_referencia,
      calorias: Number(comida.calorias),
      proteinas: Number(comida.proteinas),
      carbohidratos: Number(comida.carbohidratos),
      grasas: Number(comida.grasas),
    });
  }

  eliminar(comida: Comida) {
    if (!confirm(`¿Eliminar la comida "${comida.nombre}"?`)) {
      return;
    }

    this.comidaService.deleteComida(comida.id_comida).subscribe({
      next: () => {
        this.mensaje.set('Comida eliminada correctamente.');
        this.cargarComidas();
      },
      error: () => this.error.set('No se pudo eliminar la comida. Puede estar asociada a un plan.'),
    });
  }

  cancelarEdicion() {
    this.comidaEditando.set(null);
    this.guardando.set(false);
    this.comidaForm.reset();
  }

  campoInvalido(nombre: string): boolean {
    const campo = this.comidaForm.get(nombre);
    return !!campo && campo.invalid && campo.touched;
  }

  etiquetaCategoria(categoria: CategoriaComida): string {
    return this.categorias.find(opcion => opcion.value === categoria)?.label ?? categoria;
  }

  private cargarComidas() {
    this.cargando.set(true);
    this.comidaService.getComidas().subscribe({
      next: (comidas) => {
        this.comidas.set(comidas);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudieron cargar las comidas.');
        this.cargando.set(false);
        this.guardando.set(false);
      },
    });
  }
}
