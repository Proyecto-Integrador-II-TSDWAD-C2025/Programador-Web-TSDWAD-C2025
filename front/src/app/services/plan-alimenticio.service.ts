import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { CompletarComidaPlanResponse, MiPlanAlimenticioResponse } from '../models';
import { API_URL } from './api.config';

@Injectable({ providedIn: 'root' })
export class PlanAlimenticioService {
  private http = inject(HttpClient);

  getMiPlan(): Observable<MiPlanAlimenticioResponse> {
    return this.http.get<MiPlanAlimenticioResponse>(`${API_URL}/mi-plan-alimenticio/`);
  }

  alternarComida(planComidaId: number): Observable<CompletarComidaPlanResponse> {
    return this.http.post<CompletarComidaPlanResponse>(`${API_URL}/mi-plan-alimenticio/completar-comida/`, {
      plan_comida_id: planComidaId,
    });
  }
}
