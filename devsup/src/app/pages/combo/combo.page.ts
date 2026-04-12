import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ApiService } from '../../services/api.service';
import { ComboResponse, DnsResponse } from '../../models/api.models';

@Component({
  selector: 'app-combo',
  templateUrl: 'combo.page.html',
  styleUrls: ['combo.page.scss'],
  standalone: false,
})
export class ComboPage implements OnInit {
  ip = '';
  ports = '8181,5432';
  result: ComboResponse | null = null;
  loading = false;
  errorMsg = '';

  hostname = '';
  dnsResult: DnsResponse | null = null;
  dnsLoading = false;
  dnsErrorMsg = '';

  constructor(private api: ApiService, private http: HttpClient) {}

  ngOnInit(): void {
    this.http.get<{ ip: string }>('https://api.ipify.org?format=json').subscribe({
      next: (res) => { this.ip = res.ip; },
      error: () => {},
    });
  }

  check(): void {
    if (!this.ip.trim() || !this.ports.trim()) return;
    this.loading = true;
    this.result = null;
    this.errorMsg = '';

    this.api.checkPorts(this.ip.trim(), this.ports.trim()).subscribe({
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

  lookup(): void {
    if (!this.hostname.trim()) return;
    this.dnsLoading = true;
    this.dnsResult = null;
    this.dnsErrorMsg = '';

    this.api.lookupDns(this.hostname.trim()).subscribe({
      next: (res) => {
        this.dnsResult = res;
        this.dnsLoading = false;
      },
      error: () => {
        this.dnsErrorMsg = 'Erro ao conectar com o servidor.';
        this.dnsLoading = false;
      },
    });
  }

  statusColor(color: string): string {
    const map: Record<string, string> = {
      resultColorOpen: 'success',
      resultColorClose: 'danger',
      resultColorInvalid: 'warning',
    };
    return map[color] ?? 'medium';
  }

  statusIcon(color: string): string {
    const map: Record<string, string> = {
      resultColorOpen: 'checkmark-circle-outline',
      resultColorClose: 'close-circle-outline',
      resultColorInvalid: 'warning-outline',
    };
    return map[color] ?? 'help-circle-outline';
  }
}
