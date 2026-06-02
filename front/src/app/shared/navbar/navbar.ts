import { Component, inject, signal, computed, viewChild, ElementRef, Renderer2, DestroyRef } from '@angular/core';
import { RouterLink, Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'app-navbar',
  imports: [RouterLink],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Navbar {
  private authService = inject(AuthService);
  private router = inject(Router);
  private renderer = inject(Renderer2);
  private destroyRef = inject(DestroyRef);

  usuario = this.authService.usuario;
  isLoggedIn = this.authService.isLoggedIn;
  rol = computed(() => this.usuario()?.id_rol?.nombre_rol ?? '');
  menuOpen = signal(false);
  userMenuOpen = signal(false);

  private userMenuWrapper = viewChild.required<ElementRef<HTMLElement>>('userMenu');

  avatarInitial = computed(() => {
    const nombre = this.usuario()?.nombre ?? '';
    return nombre.charAt(0).toUpperCase();
  });

  constructor() {
    const removeListener = this.renderer.listen('document', 'click', (event: Event) => {
      if (!this.userMenuOpen()) {
        return;
      }
      const wrapper = this.userMenuWrapper().nativeElement;
      const target = event.target as Node;
      if (!wrapper.contains(target)) {
        this.closeUserMenu();
      }
    });

    this.destroyRef.onDestroy(() => {
      removeListener();
    });
  }

  toggleMenu() {
    this.menuOpen.update(v => !v);
  }

  closeMenu() {
    this.menuOpen.set(false);
  }

  toggleUserMenu() {
    this.userMenuOpen.update(v => !v);
  }

  closeUserMenu() {
    this.userMenuOpen.set(false);
  }

  scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  logout() {
    this.authService.logout();
  }
}