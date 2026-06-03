import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { API_URL } from './api.config';
import { UsuarioPlan } from '../models';

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

@Injectable({ providedIn: 'root' })
export class UsuarioPlanService {
  private http = inject(HttpClient);

  getPlanesByUsuario(usuarioId: number): Observable<UsuarioPlan[]> {
    return this.http.get<UsuarioPlan[] | PaginatedResponse<UsuarioPlan>>(`${API_URL}/usuario-planes/por-usuario/${usuarioId}/`).pipe(
      map(res => Array.isArray(res) ? res : res.results)
    );
  }
}
