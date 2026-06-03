import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, inject, OnInit, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { NutricionistaRequest, UsuarioRead } from '../../../models';
import { UsuarioService } from '../../../services/usuario.service';

@Component({
  selector: 'app-nutricionistas-gestion',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './nutricionistas-gestion.html',
  styleUrls: ['../../nutricionista/gestion-nutricionista.css', './nutricionistas-gestion.css'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class NutricionistasGestion implements OnInit {
  private usuarioService = inject(UsuarioService);

  nutricionistas = signal<UsuarioRead[]>([]);
  cargando = signal(true);
  guardando = signal(false);
  mensaje = signal('');
  error = signal('');
  nutricionistaEditando = signal<number | null>(null);

  nutricionistaForm = new FormGroup({
    nombre: new FormControl('', [Validators.required, Validators.maxLength(100)]),
    apellido: new FormControl('', [Validators.required, Validators.maxLength(100)]),
    email: new FormControl('', [Validators.required, Validators.email, Validators.maxLength(255)]),
    contrasena: new FormControl('', [Validators.required, Validators.minLength(8)]),
  });

  ngOnInit() {
    this.cargarNutricionistas();
  }

  guardar() {
    if (this.nutricionistaForm.invalid) {
      this.nutricionistaForm.markAllAsTouched();
      return;
    }

    const value = this.nutricionistaForm.getRawValue();
    const payload: NutricionistaRequest = {
      nombre: value.nombre!,
      apellido: value.apellido!,
      email: value.email!,
    };
    if (value.contrasena) {
      payload.contrasena = value.contrasena;
    }

    const id = this.nutricionistaEditando();
    const request = id
      ? this.usuarioService.updateNutricionista(id, payload)
      : this.usuarioService.createNutricionista(payload);

    this.guardando.set(true);
    this.error.set('');
    request.subscribe({
      next: () => {
        this.mensaje.set(id ? 'Nutricionista actualizado correctamente.' : 'Nutricionista creado correctamente.');
        this.cancelarEdicion();
        this.cargarNutricionistas();
      },
      error: (response: HttpErrorResponse) => {
        this.error.set(this.obtenerMensajeError(response));
        this.guardando.set(false);
      },
    });
  }

  editar(nutricionista: UsuarioRead) {
    this.nutricionistaEditando.set(nutricionista.id_usuario);
    this.mensaje.set('');
    this.error.set('');
    this.nutricionistaForm.setValue({
      nombre: nutricionista.nombre,
      apellido: nutricionista.apellido,
      email: nutricionista.email,
      contrasena: '',
    });
    this.nutricionistaForm.controls.contrasena.setValidators([Validators.minLength(8)]);
    this.nutricionistaForm.controls.contrasena.updateValueAndValidity();
  }

  eliminar(nutricionista: UsuarioRead) {
    if (!confirm(`¿Eliminar la cuenta profesional de ${nutricionista.nombre} ${nutricionista.apellido}?`)) {
      return;
    }

    this.usuarioService.deleteNutricionista(nutricionista.id_usuario).subscribe({
      next: () => {
        this.mensaje.set('Nutricionista eliminado correctamente.');
        if (this.nutricionistaEditando() === nutricionista.id_usuario) {
          this.cancelarEdicion();
        }
        this.cargarNutricionistas();
      },
      error: () => this.error.set('No se pudo eliminar la cuenta profesional.'),
    });
  }

  cancelarEdicion() {
    this.nutricionistaEditando.set(null);
    this.guardando.set(false);
    this.nutricionistaForm.reset();
    this.nutricionistaForm.controls.contrasena.setValidators([Validators.required, Validators.minLength(8)]);
    this.nutricionistaForm.controls.contrasena.updateValueAndValidity();
  }

  campoInvalido(nombre: string): boolean {
    const campo = this.nutricionistaForm.get(nombre);
    return !!campo && campo.invalid && campo.touched;
  }

  private cargarNutricionistas() {
    this.cargando.set(true);
    this.usuarioService.getNutricionistas().subscribe({
      next: (nutricionistas) => {
        this.nutricionistas.set(nutricionistas);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudo cargar la lista de nutricionistas.');
        this.cargando.set(false);
        this.guardando.set(false);
      },
    });
  }

  private obtenerMensajeError(response: HttpErrorResponse): string {
    const errores = response.error;
    if (errores?.email?.length) {
      return `Correo electrónico: ${errores.email.join(' ')}`;
    }
    if (errores?.contrasena?.length) {
      return `Contraseña: ${errores.contrasena.join(' ')}`;
    }
    return 'No se pudo guardar la cuenta profesional. Revisá los datos e intentá nuevamente.';
  }
}
