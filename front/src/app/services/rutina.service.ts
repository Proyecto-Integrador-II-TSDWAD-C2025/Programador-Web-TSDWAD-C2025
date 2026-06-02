import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { CompletarEjercicioResponse, MiRutinaResponse } from '../models';
import { API_URL } from './api.config';

@Injectable({ providedIn: 'root' })
export class RutinaService {
  private http = inject(HttpClient);

  getMiRutina(): Observable<MiRutinaResponse> {
    return this.http.get<MiRutinaResponse>(`${API_URL}/mi-rutina/`);
  }

  alternarEjercicio(ejercicioId: number): Observable<CompletarEjercicioResponse> {
    return this.http.post<CompletarEjercicioResponse>(`${API_URL}/mi-rutina/completar-ejercicio/`, {
      ejercicio_id: ejercicioId,
    });
  }
}
