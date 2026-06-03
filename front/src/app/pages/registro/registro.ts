import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-registro',
  imports: [RouterLink, ReactiveFormsModule],
  templateUrl: './registro.html',
  styleUrl: './registro.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Registro {
  private authService = inject(AuthService);
  private router = inject(Router);

  mensajeError = signal('');
  cargando = signal(false);

  registroForm = new FormGroup({
    nombre: new FormControl('', [Validators.required]),
    apellido: new FormControl('', [Validators.required]),
    email: new FormControl('', [Validators.required, Validators.email]),
    contrasena: new FormControl('', [Validators.required, Validators.minLength(8)]),
  });

  registrarse() {
    if (this.registroForm.invalid) {
      this.registroForm.markAllAsTouched();
      return;
    }

    this.cargando.set(true);
    this.mensajeError.set('');

    const formValue = this.registroForm.value;

    this.authService.registro({
      nombre: formValue.nombre!,
      apellido: formValue.apellido!,
      email: formValue.email!,
      contrasena: formValue.contrasena!,
    }).subscribe({
      next: () => {
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.cargando.set(false);
        this.mensajeError.set(this.obtenerMensajeError(err.error));
      }
    });
  }

  private obtenerMensajeError(error: unknown): string {
    if (!error || typeof error !== 'object') {
      return 'Error al registrarse. Intentá de nuevo.';
    }

    const detalle = error as Record<string, string | string[]>;
    if (detalle['email']) {
      return 'Ya existe un usuario con ese correo electrónico.';
    }

    const mensajeContrasena = detalle['contrasena'];
    if (Array.isArray(mensajeContrasena)) {
      return mensajeContrasena.join(' ');
    }
    if (typeof mensajeContrasena === 'string') {
      return mensajeContrasena;
    }

    return 'Error al registrarse. Intentá de nuevo.';
  }
}
