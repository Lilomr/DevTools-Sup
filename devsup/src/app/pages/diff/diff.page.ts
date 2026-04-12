import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { DiffLine, DiffResponse } from '../../models/api.models';

@Component({
  selector: 'app-diff',
  templateUrl: 'diff.page.html',
  styleUrls: ['diff.page.scss'],
  standalone: false,
})
export class DiffPage {
  input1 = '';
  input2 = '';
  result: DiffResponse | null = null;
  loading = false;
  errorMsg = '';
  activeTab: 'left' | 'right' = 'left';

  constructor(private api: ApiService) {}

  compare(): void {
    if (!this.input1.trim() && !this.input2.trim()) return;
    this.loading = true;
    this.result = null;
    this.errorMsg = '';

    this.api.diffTexts(this.input1, this.input2).subscribe({
      next: (res) => {
        this.result = res;
        this.activeTab = 'left';
        this.loading = false;
      },
      error: () => {
        this.errorMsg = 'Erro ao conectar com o servidor.';
        this.loading = false;
      },
    });
  }

  reset(): void {
    this.result = null;
    this.input1 = '';
    this.input2 = '';
  }

  compareAgain(): void {
    this.result = null;
  }

  lineClass(line: DiffLine): string {
    const map: Record<string, string> = {
      removed: 'diff-removed',
      added: 'diff-added',
      unchanged: 'diff-unchanged',
      empty: 'diff-empty',
    };
    return map[line.kind] ?? '';
  }
}
