import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { DashboardComponent } from './pages/dashboard/dashboard';
import { QuienesSomosComponent } from './pages/quienes-somos/quienes-somos';
import { Login } from './pages/login/login';
import { Registro } from './pages/registro/registro';
import { Perfil } from './pages/perfil/perfil';
import { Planes } from './pages/planes/planes';

export const routes: Routes = [
  { path: '', component: Home },
  {path: 'dashboard', component: DashboardComponent },
  { path: 'quienes-somos', component: QuienesSomosComponent },
  { path: 'login', component: Login },
  { path: 'registro', component: Registro },
  { path: 'perfil', component: Perfil },
  { path: 'planes', component: Planes },
];

