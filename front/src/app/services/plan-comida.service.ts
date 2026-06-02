import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { PlanComida } from '../models';
import { API_URL } from './api.config';

export type PlanComidaPayload = Omit<PlanComida, 'id_plan_comida' | 'completada_hoy'>;

@Injectable({ providedIn: 'root' })
export class PlanComidaService {
  private http = inject(HttpClient);

  getComidasPorPlan(planId: number): Observable<PlanComida[]> {
    return this.http.get<PlanComida[]>(`${API_URL}/plan-comidas/por-plan/${planId}/`);
  }

  createPlanComida(comida: PlanComidaPayload): Observable<PlanComida> {
    return this.http.post<PlanComida>(`${API_URL}/plan-comidas/`, comida);
  }

  deletePlanComida(id: number): Observable<void> {
    return this.http.delete<void>(`${API_URL}/plan-comidas/${id}/`);
  }
}
