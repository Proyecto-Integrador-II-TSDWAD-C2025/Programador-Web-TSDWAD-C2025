import { Routes } from '@angular/router';
import { adminRoleGuard } from './guards/admin-role.guard';
import { authGuard } from './guards/auth.guard';
import { staffRoleGuard } from './guards/staff-role.guard';

export const routes: Routes = [
  { path: '', loadComponent: () => import('./pages/home/home').then(m => m.Home) },
  { path: 'quienes-somos', loadComponent: () => import('./pages/quienes-somos/quienes-somos').then(m => m.QuienesSomosComponent) },
  { path: 'login', loadComponent: () => import('./pages/login/login').then(m => m.Login) },
  { path: 'registro', loadComponent: () => import('./pages/registro/registro').then(m => m.Registro) },
  { path: 'dashboard', loadComponent: () => import('./pages/dashboard/dashboard').then(m => m.DashboardComponent), canActivate: [authGuard] },
  { path: 'perfil', loadComponent: () => import('./pages/perfil/perfil').then(m => m.Perfil), canActivate: [authGuard] },
  { path: 'planes', loadComponent: () => import('./pages/planes/planes').then(m => m.Planes), canActivate: [authGuard] },
  { path: 'nutricionista/planes', loadComponent: () => import('./pages/nutricionista/planes/planes-gestion').then(m => m.PlanesGestion), canActivate: [authGuard, staffRoleGuard] },
  { path: 'nutricionista/comidas', loadComponent: () => import('./pages/nutricionista/comidas/comidas-gestion').then(m => m.ComidasGestion), canActivate: [authGuard, staffRoleGuard] },
  { path: 'administrador/nutricionistas', loadComponent: () => import('./pages/administrador/nutricionistas/nutricionistas-gestion').then(m => m.NutricionistasGestion), canActivate: [authGuard, adminRoleGuard] },
];
