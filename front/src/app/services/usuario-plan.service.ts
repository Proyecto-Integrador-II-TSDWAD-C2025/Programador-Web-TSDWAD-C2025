import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_URL } from './api.config';
import { UsuarioPlan } from '../models';

@Injectable({ providedIn: 'root' })
export class UsuarioPlanService {
  private http = inject(HttpClient);

  getPlanesByUsuario(usuarioId: number): Observable<UsuarioPlan[]> {
    return this.http.get<UsuarioPlan[]>(`${API_URL}/usuario-planes/por-usuario/${usuarioId}/`);
  }
}