import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { PerfilPayload, PerfilResponse } from '../models';
import { API_URL } from './api.config';

@Injectable({ providedIn: 'root' })
export class PerfilService {
  private http = inject(HttpClient);

  getPerfil(): Observable<PerfilResponse> {
    return this.http.get<PerfilResponse>(`${API_URL}/perfil/`);
  }

  guardarPerfil(perfil: PerfilPayload): Observable<PerfilResponse> {
    return this.http.put<PerfilResponse>(`${API_URL}/perfil/`, perfil);
  }

  getHistorialPeso(): Observable<any> {
    return this.http.get<any>(`${API_URL}/historial-peso/`);
  }
}
