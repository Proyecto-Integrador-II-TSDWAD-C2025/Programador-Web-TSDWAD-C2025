import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_URL } from './api.config';
import { UsuarioRead } from '../models';

@Injectable({ providedIn: 'root' })
export class UsuarioService {
  private http = inject(HttpClient);

  getUsuarios(): Observable<UsuarioRead[]> {
    return this.http.get<UsuarioRead[]>(`${API_URL}/usuarios/`);
  }

  getUsuario(id: number): Observable<UsuarioRead> {
    return this.http.get<UsuarioRead>(`${API_URL}/usuarios/${id}/`);
  }
}