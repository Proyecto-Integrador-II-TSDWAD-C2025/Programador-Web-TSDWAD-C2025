import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap, switchMap } from 'rxjs';
import { API_URL } from './api.config';
import { UsuarioRead, LoginRequest, RegistroRequest } from '../models';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);

  private currentUser = signal<UsuarioRead | null>(null);
  private isAuthenticated_ = signal<boolean>(false);

  readonly usuario = this.currentUser.asReadonly();
  readonly isLoggedIn = this.isAuthenticated_.asReadonly();

  constructor() {
    const stored = localStorage.getItem('usuario');
    if (stored) {
      try {
        const user: UsuarioRead = JSON.parse(stored);
        this.currentUser.set(user);
        this.isAuthenticated_.set(true);
      } catch {
        localStorage.removeItem('usuario');
      }
    }
  }

  login(credentials: LoginRequest): Observable<UsuarioRead> {
    return this.http.post<UsuarioRead>(`${API_URL}/login/`, credentials).pipe(
      tap((user) => {
        this.currentUser.set(user);
        this.isAuthenticated_.set(true);
        localStorage.setItem('usuario', JSON.stringify(user));
      })
    );
  }

  registro(data: RegistroRequest): Observable<UsuarioRead> {
    return this.http.post(`${API_URL}/usuarios/`, data).pipe(
      switchMap(() => this.login({ email: data.email, contrasena: data.contrasena }))
    );
  }

  logout(): void {
    this.currentUser.set(null);
    this.isAuthenticated_.set(false);
    localStorage.removeItem('usuario');
    this.router.navigate(['/login']);
  }

  getRole(): string {
    return this.currentUser()?.id_rol?.nombre_rol ?? '';
  }
}