import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { DiffPageRoutingModule } from './diff-routing.module';
import { DiffPage } from './diff.page';

@NgModule({
  imports: [CommonModule, FormsModule, IonicModule, DiffPageRoutingModule],
  declarations: [DiffPage],
})
export class DiffPageModule {}
