import { Component, inject, signal, OnInit } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { RolService } from '../../services/rol.service';
import { Rol } from '../../models';
import { ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'app-registro',
  imports: [RouterLink, ReactiveFormsModule],
  templateUrl: './registro.html',
  styleUrl: './registro.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Registro implements OnInit {
  private authService = inject(AuthService);
  private router = inject(Router);
  private rolService = inject(RolService);

  roles = signal<Rol[]>([]);
  mensajeError = signal('');
  cargando = signal(false);

  registroForm = new FormGroup({
    nombre: new FormControl('', [Validators.required]),
    apellido: new FormControl('', [Validators.required]),
    email: new FormControl('', [Validators.required, Validators.email]),
    contrasena: new FormControl('', [Validators.required, Validators.minLength(8)]),
    id_rol: new FormControl<number | null>(null, [Validators.required]),
  });

  ngOnInit() {
    this.rolService.getRoles().subscribe({
      next: (roles) => this.roles.set(roles),
      error: () => this.mensajeError.set('Error al cargar los roles. Intentá de nuevo.'),
    });
  }

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
      id_rol: formValue.id_rol!,
    }).subscribe({
      next: () => {
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.cargando.set(false);
        const errorMsg = err.error;
        if (typeof errorMsg === 'object' && errorMsg.email) {
          this.mensajeError.set('Ya existe un usuario con ese correo electrónico.');
        } else {
          this.mensajeError.set('Error al registrarse. Intentá de nuevo.');
        }
      }
    });
  }
}
