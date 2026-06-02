import { ChangeDetectionStrategy, Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { PlanService } from '../../services/plan.service';
import { UsuarioPlanService } from '../../services/usuario-plan.service';
import { Plan, UsuarioPlan } from '../../models';

interface DashboardOption {
  titulo: string;
  descripcion: string;
  ruta?: string;
}

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DashboardComponent implements OnInit {
  private authService = inject(AuthService);
  private planService = inject(PlanService);
  private usuarioPlanService = inject(UsuarioPlanService);

  usuario = this.authService.usuario;
  rol = this.authService.getRole();

  planes = signal<Plan[]>([]);
  misPlanes = signal<UsuarioPlan[]>([]);
  cargando = signal(true);

  opcionesCliente: DashboardOption[] = [
    { titulo: 'Ver mi rutina', descripcion: 'Accedé a tu rutina personalizada según tu objetivo físico.', ruta: '/mi-rutina' },
    { titulo: 'Registrar comida', descripcion: 'Cargá tus comidas diarias para llevar un control alimentario.', ruta: '/mi-plan-alimenticio' },
    { titulo: 'Ver plan alimenticio', descripcion: 'Consultá recomendaciones de comidas, calorías y proteínas.', ruta: '/mi-plan-alimenticio' },
    { titulo: 'Consultar nutricionista', descripcion: 'Enviá consultas o revisá indicaciones de tu profesional asignado.' },
    { titulo: 'Ver planes premium', descripcion: 'Conocé funciones avanzadas para mejorar tu seguimiento.' },
  ];

  opcionesNutricionista = [
    { titulo: 'Gestionar planes alimenticios', descripcion: 'Crear, editar o eliminar planes nutricionales disponibles.', ruta: '/nutricionista/planes' },
    { titulo: 'Gestionar comidas', descripcion: 'Cargar alimentos y mantener sus valores nutricionales.', ruta: '/nutricionista/comidas' },
    { titulo: 'Ver pacientes', descripcion: 'Consultar la lista de usuarios asignados para seguimiento.' },
    { titulo: 'Revisar registros alimentarios', descripcion: 'Analizar comidas cargadas, calorías y hábitos alimentarios.' },
    { titulo: 'Responder consultas', descripcion: 'Atender mensajes o dudas enviadas por los pacientes.' },
  ];

  opcionesAdmin = [
    { titulo: 'Gestionar usuarios', descripcion: 'Administrar clientes registrados y sus perfiles.' },
    { titulo: 'Gestionar nutricionistas', descripcion: 'Alta, edición o baja de profesionales dentro del sistema.', ruta: '/administrador/nutricionistas' },
    { titulo: 'Gestionar rutinas', descripcion: 'Crear, editar o eliminar rutinas de entrenamiento.' },
    { titulo: 'Gestionar planes alimenticios', descripcion: 'Administrar recomendaciones nutricionales disponibles.' },
    { titulo: 'Gestionar planes de pago', descripcion: 'Actualizar planes gratuitos, premium y sus beneficios.' },
  ];

  firstName = signal('');

  nombrePlanActual(): string {
    const plan = this.misPlanes()[0]?.id_plan;
    return typeof plan === 'number' ? `Plan #${plan}` : plan?.nombre_plan ?? 'Sin plan asignado';
  }

  ngOnInit() {
    const user = this.usuario();
    if (user) {
      this.firstName.set(user.nombre.split(' ')[0]);
    }

    this.planService.getPlanes().subscribe({
      next: (planes) => {
        this.planes.set(planes);
        this.cargando.set(false);
      },
      error: () => this.cargando.set(false),
    });

    const userId = this.usuario()?.id_usuario;
    if (userId && this.rol === 'usuario') {
      this.usuarioPlanService.getPlanesByUsuario(userId).subscribe({
        next: (misPlanes) => this.misPlanes.set(misPlanes),
        error: () => {},
      });
    }
  }
}
