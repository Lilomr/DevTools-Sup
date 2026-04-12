import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { APP_PAGES, AppPage } from '../../models/pages';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: false,
})
export class HomePage {
  services = APP_PAGES
    .filter((p: AppPage) => p.url !== '/home')
    .map((p: AppPage) => ({
      ...p,
      icon: p.icon + '-outline',
      description: p.description,
    }));

  constructor(private router: Router) {}

  navigate(route: string): void {
    this.router.navigateByUrl(route);
  }
}
