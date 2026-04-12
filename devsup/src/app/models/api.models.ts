export interface DnsResponse {
  dns: string;
  status: string[];
  error?: string;
}

export interface ComboResponse {
  ip: string;
  port_list: string[];
  status_list: string[];
  color_list: string[];
  resolved_ip: string;
  dns_routes: string[];
  error?: string;
}

export interface DiffLine {
  num: number | string;
  text: string;
  kind: 'removed' | 'added' | 'unchanged' | 'empty';
}

export interface DiffResponse {
  left: DiffLine[];
  right: DiffLine[];
}

export interface ConvertResponse {
  download_url?: string;
  filename?: string;
  error?: string;
}
