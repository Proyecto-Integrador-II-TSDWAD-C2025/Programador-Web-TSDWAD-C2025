import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { API_URL } from './api.config';
import { UsuarioRead } from '../models';

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

@Injectable({ providedIn: 'root' })
export class UsuarioService {
  private http = inject(HttpClient);

  getUsuarios(): Observable<UsuarioRead[]> {
    return this.http.get<UsuarioRead[] | PaginatedResponse<UsuarioRead>>(`${API_URL}/usuarios/`).pipe(
      map(res => Array.isArray(res) ? res : res.results)
    );
  }

  getUsuario(id: number): Observable<UsuarioRead> {
    return this.http.get<UsuarioRead>(`${API_URL}/usuarios/${id}/`);
  }
}
