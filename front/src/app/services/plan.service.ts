import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_URL } from './api.config';
import { Plan } from '../models';

@Injectable({ providedIn: 'root' })
export class PlanService {
  private http = inject(HttpClient);

  getPlanes(): Observable<Plan[]> {
    return this.http.get<Plan[]>(`${API_URL}/planes/`);
  }

  getPlan(id: number): Observable<Plan> {
    return this.http.get<Plan>(`${API_URL}/planes/${id}/`);
  }
}