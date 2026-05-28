import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { API_URL } from './api.config';
import { Comida } from '../models';

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

@Injectable({ providedIn: 'root' })
export class ComidaService {
  private http = inject(HttpClient);

  getComidas(): Observable<Comida[]> {
    return this.http.get<Comida[] | PaginatedResponse<Comida>>(`${API_URL}/comidas/`).pipe(
      map(res => Array.isArray(res) ? res : res.results)
    );
  }
}
