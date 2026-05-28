import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { API_URL } from './api.config';
import { Plan } from '../models';

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

@Injectable({ providedIn: 'root' })
export class PlanService {
  private http = inject(HttpClient);

  getPlanes(): Observable<Plan[]> {
    return this.http.get<Plan[] | PaginatedResponse<Plan>>(`${API_URL}/planes/`).pipe(
      map(res => Array.isArray(res) ? res : res.results)
    );
  }

  getPlan(id: number): Observable<Plan> {
    return this.http.get<Plan>(`${API_URL}/planes/${id}/`);
  }
}
