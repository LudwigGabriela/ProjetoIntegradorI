from .models import ConfiguracaoSistema

def configuracoes_globais(request):
    config = ConfiguracaoSistema.objects.first()
    return {
        'config_global': config
    }
