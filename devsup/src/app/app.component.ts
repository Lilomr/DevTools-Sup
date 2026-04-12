import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { APP_PAGES, AppPage } from './models/pages';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
  standalone: false,
})
export class AppComponent {
  public appPages: AppPage[] = APP_PAGES;

  constructor(public router: Router) {}

  get visiblePages(): AppPage[] {
    return this.appPages.filter(p => !this.router.url.startsWith(p.url));
  }
}
