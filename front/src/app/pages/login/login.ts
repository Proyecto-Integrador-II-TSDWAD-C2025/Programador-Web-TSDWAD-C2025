import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-login',
  imports: [RouterLink, FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  email = '';
  password = '';
  mensajeError = '';

  constructor(private router: Router) {}

  iniciarSesion() {
    if (this.email === 'cliente@nutriapp.com' && this.password === 'cliente123') {
      localStorage.setItem('rol', 'cliente');
      this.router.navigate(['/dashboard']);
      return;
    }

    if (this.email === 'nutricionista@nutriapp.com' && this.password === 'nutri123') {
      localStorage.setItem('rol', 'nutricionista');
      this.router.navigate(['/dashboard']);
      return;
    }

    if (this.email === 'admin@nutriapp.com' && this.password === 'admin123') {
      localStorage.setItem('rol', 'admin');
      this.router.navigate(['/dashboard']);
      return;
    }

    this.mensajeError = 'Correo o contraseña incorrectos.';
  }
}

