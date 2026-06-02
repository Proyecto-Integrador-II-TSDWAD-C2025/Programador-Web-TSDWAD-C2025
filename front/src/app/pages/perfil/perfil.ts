import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-perfil',
  imports: [ReactiveFormsModule],
  templateUrl: './perfil.html',
  styleUrl: './perfil.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Perfil {
  private authService = inject(AuthService);

  usuario = this.authService.usuario;
  mensajeExito = signal(false);

  perfilForm = new FormGroup({
    edad: new FormControl<number | null>(null, [Validators.required, Validators.min(13), Validators.max(100)]),
    pesoActual: new FormControl<number | null>(null, [Validators.required, Validators.min(30), Validators.max(300)]),
    altura: new FormControl<number | null>(null, [Validators.required, Validators.min(100), Validators.max(250)]),
    pesoObjetivo: new FormControl<number | null>(null, [Validators.required, Validators.min(30), Validators.max(300)]),
    objetivo: new FormControl('', [Validators.required]),
    actividad: new FormControl('', [Validators.required]),
    preferencia: new FormControl('', [Validators.required]),
  });

  guardar() {
    if (this.perfilForm.invalid) {
      this.perfilForm.markAllAsTouched();
      return;
    }

    this.mensajeExito.set(true);
    setTimeout(() => this.mensajeExito.set(false), 3000);
  }

  campoInvalido(nombre: string): boolean {
    const campo = this.perfilForm.get(nombre);
    return !!campo && campo.invalid && campo.touched;
  }
}
