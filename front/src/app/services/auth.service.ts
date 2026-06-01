import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { finalize, map, Observable, tap } from 'rxjs';
import { API_URL } from './api.config';
import { UsuarioRead, LoginRequest, LoginResponse, RegistroRequest } from '../models';

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
    const token = localStorage.getItem('auth_token');
    if (stored && token) {
      try {
        const user: UsuarioRead = JSON.parse(stored);
        this.currentUser.set(user);
        this.isAuthenticated_.set(true);
      } catch {
        localStorage.removeItem('usuario');
        localStorage.removeItem('auth_token');
      }
    } else {
      localStorage.removeItem('usuario');
      localStorage.removeItem('auth_token');
    }
  }

  login(credentials: LoginRequest): Observable<UsuarioRead> {
    return this.http.post<LoginResponse>(`${API_URL}/login/`, credentials).pipe(
      tap((response) => this.guardarSesion(response)),
      map((response) => response.usuario)
    );
  }

  registro(data: RegistroRequest): Observable<UsuarioRead> {
    return this.http.post<LoginResponse>(`${API_URL}/register/`, data).pipe(
      tap((response) => this.guardarSesion(response)),
      map((response) => response.usuario)
    );
  }

  logout(): void {
    this.http.post(`${API_URL}/logout/`, {}).pipe(
      finalize(() => this.limpiarSesion())
    ).subscribe({ error: () => {} });
  }

  private guardarSesion(response: LoginResponse): void {
    this.currentUser.set(response.usuario);
    this.isAuthenticated_.set(true);
    localStorage.setItem('usuario', JSON.stringify(response.usuario));
    localStorage.setItem('auth_token', response.token);
  }

  private limpiarSesion(): void {
    this.currentUser.set(null);
    this.isAuthenticated_.set(false);
    localStorage.removeItem('usuario');
    localStorage.removeItem('auth_token');
    this.router.navigate(['/login']);
  }

  getRole(): string {
    return this.currentUser()?.id_rol?.nombre_rol ?? '';
  }
}
