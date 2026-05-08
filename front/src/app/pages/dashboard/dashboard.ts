import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-dashboard',
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class DashboardComponent {
  rol = localStorage.getItem('rol') || 'cliente';

  cliente = {
    nombre: 'Pablo Romero',
    objetivo: 'Aumentar masa muscular',
    planActual: 'Plan gratuito',
    rutina: 'Rutina de fuerza - Principiante',
    caloriasHoy: 1800,
    nutricionista: 'Lic. Mariana García'
  };

  nutricionista = {
    nombre: 'Lic. Mariana García',
    pacientesAsignados: 12,
    consultasPendientes: 3,
    registrosPorRevisar: 5
  };

  admin = {
    usuariosRegistrados: 120,
    nutricionistasActivos: 6,
    planesDisponibles: 3,
    rutinasCargadas: 18
  };

  opcionesCliente = [
    {
      titulo: 'Ver mi rutina',
      descripcion: 'Accedé a tu rutina personalizada según tu objetivo físico.'
    },
    {
      titulo: 'Registrar comida',
      descripcion: 'Cargá tus comidas diarias para llevar un control alimentario.'
    },
    {
      titulo: 'Ver plan alimenticio',
      descripcion: 'Consultá recomendaciones de comidas, calorías y proteínas.'
    },
    {
      titulo: 'Consultar nutricionista',
      descripcion: 'Enviá consultas o revisá indicaciones de tu profesional asignado.'
    },
    {
      titulo: 'Ver planes premium',
      descripcion: 'Conocé funciones avanzadas para mejorar tu seguimiento.'
    }
  ];

  opcionesNutricionista = [
    {
      titulo: 'Ver pacientes',
      descripcion: 'Consultar la lista de usuarios asignados para seguimiento.'
    },
    {
      titulo: 'Revisar registros alimentarios',
      descripcion: 'Analizar comidas cargadas, calorías y hábitos alimentarios.'
    },
    {
      titulo: 'Responder consultas',
      descripcion: 'Atender mensajes o dudas enviadas por los pacientes.'
    },
    {
      titulo: 'Cargar recomendación',
      descripcion: 'Crear indicaciones nutricionales personalizadas.'
    }
  ];

  opcionesAdmin = [
    {
      titulo: 'Gestionar usuarios',
      descripcion: 'Administrar clientes registrados y sus perfiles.'
    },
    {
      titulo: 'Gestionar nutricionistas',
      descripcion: 'Alta, edición o baja de profesionales dentro del sistema.'
    },
    {
      titulo: 'Gestionar rutinas',
      descripcion: 'Crear, editar o eliminar rutinas de entrenamiento.'
    },
    {
      titulo: 'Gestionar planes alimenticios',
      descripcion: 'Administrar recomendaciones nutricionales disponibles.'
    },
    {
      titulo: 'Gestionar planes de pago',
      descripcion: 'Actualizar planes gratuitos, premium y sus beneficios.'
    }
  ];

  cambiarRol() {
    if (this.rol === 'cliente') {
      this.rol = 'nutricionista';
    } else if (this.rol === 'nutricionista') {
      this.rol = 'admin';
    } else {
      this.rol = 'cliente';
    }

    localStorage.setItem('rol', this.rol);
  }
}
