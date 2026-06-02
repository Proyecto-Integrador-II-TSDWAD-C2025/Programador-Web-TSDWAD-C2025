import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { API_URL } from './api.config';
import { NutricionistaRequest, UsuarioRead } from '../models';

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

  getNutricionistas(): Observable<UsuarioRead[]> {
    return this.http.get<UsuarioRead[]>(`${API_URL}/usuarios/nutricionistas/`);
  }

  createNutricionista(data: NutricionistaRequest): Observable<UsuarioRead> {
    return this.http.post<UsuarioRead>(`${API_URL}/usuarios/crear-nutricionista/`, data);
  }

  updateNutricionista(id: number, data: NutricionistaRequest): Observable<UsuarioRead> {
    return this.http.patch<UsuarioRead>(`${API_URL}/usuarios/${id}/`, data);
  }

  deleteNutricionista(id: number): Observable<void> {
    return this.http.delete<void>(`${API_URL}/usuarios/${id}/`);
  }
}
