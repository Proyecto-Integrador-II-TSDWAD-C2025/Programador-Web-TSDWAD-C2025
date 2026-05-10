import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_URL } from './api.config';
import { Comida } from '../models';

@Injectable({ providedIn: 'root' })
export class ComidaService {
  private http = inject(HttpClient);

  getComidas(): Observable<Comida[]> {
    return this.http.get<Comida[]>(`${API_URL}/comidas/`);
  }
}