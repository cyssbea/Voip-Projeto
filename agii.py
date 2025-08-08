#!/usr/bin/python3

from asterisk.agi import *
from func import pegar_bairro_cep, indicar_bairro_oferecer_plano

agi = AGI()
agi.answer()

# Mensagens de boas-vindas (corrigindo vírgulas)
agi.appexec('Agi',f'googletts.agi,"Seja bem vindo a Voip Net em que posso ajuda-lo?","pt-BR"')
agi.appexec('Agi',f'googletts.agi,"Para contratar um novo plano digite um","pt-BR"')
agi.appexec('Agi',f'googletts.agi,"Para cancelar seu contrato digite dois","pt-BR"')
agi.appexec('Agi',f'googletts.agi,"Para reclamar com a nossa atendente a troco de nada digite 3","pt-BR"')

digito = agi.get_data('beep', timeout=10000, max_digits=1)

if digito == "1":
    agi.appexec('Agi',f'googletts.agi,"Digite seu CEP","pt-BR"')
    cep = agi.get_data("beep", timeout=10000, max_digits=8)
    bairro = pegar_bairro_cep(cep)
    
    # Verifica se o CEP é válido
    if not bairro:
        agi.appexec('Agi',f'googletts.agi,"CEP não encontrado, desligando","pt-BR"')
        agi.hangup()
        exit()
    
    agi.verbose(f"CEP: {cep} | Região: {bairro}")
    
    plano = indicar_bairro_oferecer_plano(bairro)
    
    if "não temos" in plano.lower():
        agi.appexec('Agi',f'googletts.agi,"{plano}","pt-BR"')
        agi.hangup()
    else:
        agi.appexec('Agi',f'googletts.agi,"{plano}","pt-BR"')
        agi.appexec('Agi',f'googletts.agi,"Gostaria de contratar?","pt-BR"')
        agi.appexec('Agi',f'googletts.agi,"Se sim digite um","pt-BR"')
        agi.appexec('Agi',f'googletts.agi,"Se não digite dois","pt-BR"')
        
        resposta = agi.get_data('beep', timeout=10000, max_digits=1)
        
        if resposta == "1":
            agi.appexec('Agi',f'googletts.agi,"Estaremos enviando uma equipe para {bairro}","pt-BR"')
        else:
            agi.appexec('Agi',f'googletts.agi,"Tudo bem, estaremos desligando. Tenha uma boa noite!","pt-BR"')
        agi.hangup()

elif digito == "2":
    agi.appexec('Agi',f'googletts.agi,"Estaremos cancelando seu contrato","pt-BR"')
    agi.hangup()

elif digito == "3":
    agi.appexec('Agi',f'googletts.agi,"Isso foi rude, estarei desligando","pt-BR"')
    agi.hangup()

else:
    agi.appexec('Agi',f'googletts.agi,"Opção inválida, desligando","pt-BR"')
    agi.hangup()