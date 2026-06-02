import { ChangeDetectionStrategy, Component, OnInit, inject, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { finalize } from 'rxjs';
import { DatePipe } from '@angular/common';
import {
  ActividadPerfil,
  ObjetivoPerfil,
  PerfilPayload,
  PreferenciaPerfil,
} from '../../models';
import { AuthService } from '../../services/auth.service';
import { PerfilService } from '../../services/perfil.service';

@Component({
  selector: 'app-perfil',
  imports: [ReactiveFormsModule, DatePipe],
  templateUrl: './perfil.html',
  styleUrl: './perfil.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Perfil implements OnInit {
  private authService = inject(AuthService);
  private perfilService = inject(PerfilService);
  private router = inject(Router);

  usuario = this.authService.usuario;
  cargando = signal(true);
  guardando = signal(false);
  mensajeExito = signal('');
  mensajeError = signal('');
  historialPeso = signal<any[]>([]);

  perfilForm = new FormGroup({
    edad: new FormControl<number | null>(null, [Validators.required, Validators.min(13), Validators.max(100)]),
    peso_actual: new FormControl<number | null>(null, [Validators.required, Validators.min(30), Validators.max(300)]),
    altura_cm: new FormControl<number | null>(null, [Validators.required, Validators.min(100), Validators.max(250)]),
    peso_objetivo: new FormControl<number | null>(null, [Validators.required, Validators.min(30), Validators.max(300)]),
    objetivo: new FormControl<ObjetivoPerfil | ''>('', [Validators.required]),
    actividad: new FormControl<ActividadPerfil | ''>('', [Validators.required]),
    preferencia: new FormControl<PreferenciaPerfil | ''>('', [Validators.required]),
    dias_entrenamiento: new FormControl<number | null>(3, [Validators.required, Validators.min(1), Validators.max(6)]),
    limitaciones: new FormControl('', [Validators.maxLength(500)]),
    consideraciones_alimentarias: new FormControl('', [Validators.maxLength(500)]),
    sexo: new FormControl<'m' | 'f' | ''>('', [Validators.required]),
  });

  ngOnInit(): void {
    this.perfilService.getPerfil().pipe(
      finalize(() => this.cargando.set(false))
    ).subscribe({
      next: ({ perfil }) => {
        this.perfilForm.patchValue({
          edad: perfil.edad,
          peso_actual: Number(perfil.peso_actual),
          altura_cm: perfil.altura_cm,
          peso_objetivo: Number(perfil.peso_objetivo),
          objetivo: perfil.objetivo,
          actividad: perfil.actividad,
          preferencia: perfil.preferencia,
          dias_entrenamiento: perfil.dias_entrenamiento,
          limitaciones: perfil.limitaciones,
          consideraciones_alimentarias: perfil.consideraciones_alimentarias,
          sexo: perfil.sexo,
        });
      },
      error: (error) => {
        if (error.status !== 404) {
          this.mensajeError.set('No pudimos cargar tu perfil. Intenta nuevamente.');
        }
      },
    });

    this.cargarHistorialPeso();
  }

  cargarHistorialPeso(): void {
    this.perfilService.getHistorialPeso().subscribe({
      next: (res) => {
        this.historialPeso.set(res.results || res);
      },
      error: () => {}
    });
  }

  guardar(): void {
    if (this.perfilForm.invalid) {
      this.perfilForm.markAllAsTouched();
      return;
    }

    const datos = this.perfilForm.getRawValue();
    const perfil: PerfilPayload = {
      edad: datos.edad!,
      peso_actual: datos.peso_actual!,
      altura_cm: datos.altura_cm!,
      peso_objetivo: datos.peso_objetivo!,
      objetivo: datos.objetivo as ObjetivoPerfil,
      actividad: datos.actividad as ActividadPerfil,
      preferencia: datos.preferencia as PreferenciaPerfil,
      dias_entrenamiento: datos.dias_entrenamiento!,
      limitaciones: datos.limitaciones ?? '',
      consideraciones_alimentarias: datos.consideraciones_alimentarias ?? '',
      sexo: datos.sexo as 'm' | 'f',
    };

    this.guardando.set(true);
    this.mensajeError.set('');
    this.perfilService.guardarPerfil(perfil).pipe(
      finalize(() => this.guardando.set(false))
    ).subscribe({
      next: ({ mensaje }) => {
        this.mensajeExito.set(mensaje);
        setTimeout(() => this.router.navigate(['/mi-rutina']), 650);
      },
      error: (error) => {
        console.error('Error al guardar el perfil:', error);
        if (error.error && typeof error.error === 'object') {
          const mensajes = Object.entries(error.error)
            .map(([campo, errores]) => `${campo}: ${Array.isArray(errores) ? errores.join(', ') : errores}`)
            .join(' | ');
          this.mensajeError.set(mensajes || 'Revisa los datos ingresados e intenta nuevamente.');
        } else {
          this.mensajeError.set(error.error?.detail || 'Revisa los datos ingresados e intenta nuevamente.');
        }
      },
    });
  }

  campoInvalido(nombre: string): boolean {
    const campo = this.perfilForm.get(nombre);
    return !!campo && campo.invalid && campo.touched;
  }
}
