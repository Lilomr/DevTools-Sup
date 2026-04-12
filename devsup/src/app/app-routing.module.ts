import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  {
    path: 'home',
    loadChildren: () => import('./pages/home/home.module').then(m => m.HomePageModule),
  },

  {
    path: 'combo',
    loadChildren: () => import('./pages/combo/combo.module').then(m => m.ComboPageModule),
  },
  {
    path: 'diff',
    loadChildren: () => import('./pages/diff/diff.module').then(m => m.DiffPageModule),
  },
  {
    path: 'convert',
    loadChildren: () => import('./pages/convert/convert.module').then(m => m.ConvertPageModule),
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })],
  exports: [RouterModule],
})
export class AppRoutingModule {}
