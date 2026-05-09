import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { API_URL } from './api.config';
import { Rol } from '../models';

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

@Injectable({ providedIn: 'root' })
export class RolService {
  private http = inject(HttpClient);

  getRoles(): Observable<Rol[]> {
    return this.http.get<PaginatedResponse<Rol>>(`${API_URL}/roles/`).pipe(
      map(res => res.results)
    );
  }
}