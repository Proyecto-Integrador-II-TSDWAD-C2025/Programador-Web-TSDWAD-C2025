import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ReactiveFormsModule, FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { ChangeDetectionStrategy } from '@angular/core';

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
    edad: new FormControl<number | null>(null),
    pesoActual: new FormControl<number | null>(null),
    altura: new FormControl<number | null>(null),
    pesoObjetivo: new FormControl<number | null>(null),
    objetivo: new FormControl(''),
    actividad: new FormControl(''),
    preferencia: new FormControl(''),
  });

  guardar() {
    this.mensajeExito.set(true);
    setTimeout(() => this.mensajeExito.set(false), 3000);
  }
}