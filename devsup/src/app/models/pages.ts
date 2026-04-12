export interface AppPage {
  title: string;
  description: string;
  url: string;
  icon: string;
  color: string;
}

export const APP_PAGES: AppPage[] = [
  {
    title: 'Home',
    description: '',
    url: '/home',
    icon: 'home',
    color: 'light',
  },
  {
    title: 'Teste Porta',
    description: 'Verificar se portas estão abertas ou fechadas',
    url: '/combo',
    icon: 'server',
    color: 'tertiary',
  },
  {
    title: 'Diff',
    description: 'Comparar diferenças entre dois textos',
    url: '/diff',
    icon: 'git-compare',
    color: 'secondary',
  },
  {
    title: 'Converter',
    description: 'Converter arquivos para PDF',
    url: '/convert',
    icon: 'document',
    color: 'danger',
  },
];
