import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: '', loadComponent: () => import('./pages/home/home').then(m => m.Home) },
  { path: 'quienes-somos', loadComponent: () => import('./pages/quienes-somos/quienes-somos').then(m => m.QuienesSomosComponent) },
  { path: 'login', loadComponent: () => import('./pages/login/login').then(m => m.Login) },
  { path: 'registro', loadComponent: () => import('./pages/registro/registro').then(m => m.Registro) },
  { path: 'dashboard', loadComponent: () => import('./pages/dashboard/dashboard').then(m => m.DashboardComponent), canActivate: [authGuard] },
  { path: 'perfil', loadComponent: () => import('./pages/perfil/perfil').then(m => m.Perfil), canActivate: [authGuard] },
  { path: 'planes', loadComponent: () => import('./pages/planes/planes').then(m => m.Planes), canActivate: [authGuard] },
];