import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { ComboPageRoutingModule } from './combo-routing.module';
import { ComboPage } from './combo.page';

@NgModule({
  imports: [CommonModule, FormsModule, IonicModule, ComboPageRoutingModule],
  declarations: [ComboPage],
})
export class ComboPageModule {}
