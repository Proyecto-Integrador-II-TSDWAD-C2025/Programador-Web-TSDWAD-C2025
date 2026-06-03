import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {
  private authService = inject(AuthService);
  isLoggedIn = this.authService.isLoggedIn;

  // Hero
  badge = '✦ Nutrición inteligente';
  tituloLinea1 = 'Transformá tu';
  tituloDestacado = 'salud';
  tituloLinea2 = 'con un plan a tu medida';
  descripcion = 'NutriApp combina nutrición personalizada y rutinas de entrenamiento adaptadas a tu perfil para que alcances tus objetivos reales.';
  heroImg = 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=700&auto=format&fit=crop&q=80';
  heroImgAlt = 'Nutrición saludable';

  // Estadísticas
  stats = [
    { numero: '+500', label: 'Usuarios activos' },
    { numero: '98%',  label: 'Satisfacción' },
    { numero: '30+',  label: 'Planes disponibles' }
  ];

  // Features
  sectionTag = 'Funcionalidades';
  sectionTitulo = 'Todo lo que necesitás en un solo lugar';
  features = [
    { icono: '🥗', titulo: 'Planes Alimenticios',   descripcion: 'Recomendaciones personalizadas con control de calorías y proteínas según tus objetivos.' },
    { icono: '🏋️', titulo: 'Rutinas de Ejercicio',  descripcion: 'Entrenamientos adaptados a tu nivel y metas, ya sea ganar músculo o perder peso.' },
    { icono: '👤', titulo: 'Perfil Personalizado',  descripcion: 'Planes ajustados a tu perfil único: edad, peso, altura y objetivos específicos.' },
    { icono: '💎', titulo: 'Planes Premium',         descripcion: 'Accedé a funciones avanzadas con nuestros planes diseñados para resultados óptimos.' },
    { icono: '🔒', titulo: 'Seguridad y Privacidad', descripcion: 'Tus datos de salud protegidos con los más altos estándares de seguridad.' },
    { icono: '📱', titulo: 'Responsive',             descripcion: 'Accedé a tu plan desde cualquier dispositivo, en cualquier momento y lugar.' }
  ];

  // About
  aboutTag = 'Sobre nosotros';
  aboutTitulo = 'Una app pensada para tu bienestar';
  aboutTexto1 = 'NutriApp nació para democratizar el acceso a planes de nutrición y entrenamiento de calidad.';
  aboutTexto2 = 'Combinamos tecnología moderna con conocimiento nutricional para ofrecerte una experiencia personalizada y accesible.';
  aboutImg = 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&auto=format&fit=crop&q=80';
  aboutImgAlt = 'Entrenamiento físico';
  aboutChips = ['✓ Planes personalizados', '✓ Seguimiento de progreso', '✓ Soporte dedicado', '✓ Actualización continua'];

  // CTA
  ctaTag = 'Empezá hoy';
  ctaTitulo = '¿Listo para transformar tu salud?';
  ctaDescripcion = 'Comenzá con un plan personalizado de nutrición y entrenamiento diseñado para vos.';
}