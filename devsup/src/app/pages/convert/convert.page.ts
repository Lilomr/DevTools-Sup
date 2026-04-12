import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { ConvertResponse } from '../../models/api.models';

const ACCEPTED_TYPES = [
  'text/csv',
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'text/plain',
  'image/png',
  'image/jpeg',
  'image/jpg',
];

@Component({
  selector: 'app-convert',
  templateUrl: 'convert.page.html',
  styleUrls: ['convert.page.scss'],
  standalone: false,
})
export class ConvertPage {
  selectedFile: File | null = null;
  result: ConvertResponse | null = null;
  loading = false;
  errorMsg = '';

  constructor(private api: ApiService) {}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0] ?? null;

    if (file && !ACCEPTED_TYPES.includes(file.type)) {
      this.errorMsg = 'Formato não suportado. Use CSV, XLS, XLSX, TXT, PNG ou JPG.';
      this.selectedFile = null;
      return;
    }

    this.selectedFile = file;
    this.errorMsg = '';
    this.result = null;
  }

  convert(): void {
    if (!this.selectedFile) return;
    this.loading = true;
    this.result = null;
    this.errorMsg = '';

    this.api.convertFile(this.selectedFile).subscribe({
      next: (res) => {
        if (res.error) {
          this.errorMsg = res.error;
        } else {
          this.result = res;
        }
        this.loading = false;
      },
      error: () => {
        this.errorMsg = 'Erro ao conectar com o servidor.';
        this.loading = false;
      },
    });
  }

  reset(): void {
    this.selectedFile = null;
    this.result = null;
    this.errorMsg = '';
  }
}
