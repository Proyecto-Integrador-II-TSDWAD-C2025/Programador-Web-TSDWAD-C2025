import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const staffRoleGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const rol = authService.getRole();

  if (rol === 'nutricionista' || rol === 'administrador') {
    return true;
  }

  router.navigate(['/dashboard']);
  return false;
};
