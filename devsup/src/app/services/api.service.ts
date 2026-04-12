import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { ComboResponse, ConvertResponse, DiffResponse, DnsResponse } from '../models/api.models';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly base = environment.apiUrl;

  constructor(private http: HttpClient) {}

  lookupDns(hostname: string): Observable<DnsResponse> {
    const body = new FormData();
    body.append('dns', hostname);
    return this.http.post<DnsResponse>(`${this.base}/api/dns`, body);
  }

  checkPorts(ip: string, ports: string): Observable<ComboResponse> {
    const body = new FormData();
    body.append('ip', ip);
    body.append('portas', ports);
    return this.http.post<ComboResponse>(`${this.base}/api/combo`, body);
  }

  diffTexts(input1: string, input2: string): Observable<DiffResponse> {
    const body = new FormData();
    body.append('input1', input1);
    body.append('input2', input2);
    return this.http.post<DiffResponse>(`${this.base}/api/diff`, body);
  }

  convertFile(file: File): Observable<ConvertResponse> {
    const body = new FormData();
    body.append('file', file);
    return this.http.post<ConvertResponse>(`${this.base}/api/convert`, body);
  }
}
