import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { API_URL } from './api.config';
import { Plan, PlanDetalle } from '../models';

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

  getPlan(id: number): Observable<PlanDetalle> {
    return this.http.get<PlanDetalle>(`${API_URL}/planes/${id}/`);
  }

  createPlan(plan: Omit<Plan, 'id_plan' | 'codigo'> & { codigo?: string | null }): Observable<Plan> {
    return this.http.post<Plan>(`${API_URL}/planes/`, plan);
  }

  updatePlan(id: number, plan: Omit<Plan, 'id_plan' | 'codigo'> & { codigo?: string | null }): Observable<Plan> {
    return this.http.put<Plan>(`${API_URL}/planes/${id}/`, plan);
  }

  deletePlan(id: number): Observable<void> {
    return this.http.delete<void>(`${API_URL}/planes/${id}/`);
  }
}
