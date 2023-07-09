from django.test import TestCase

# Create your tests here.
if request.method == 'POST':
        cliente = Cliente.objects.get(idcliente=idcliente)
        cliente.resposta_usuario = resposta_usuario
        cliente.save()
        
        if resposta_usuario == True:
            resposta_usuario = form.cleaned_data['resposta_usuario']
            
            soup = BeautifulSoup(resposta_usuario, 'html.parser')
            resposta_texto = strip_tags(str(soup))


            subject = f'Resposta ao seu chamado: {cliente.assunto}'
            message = f'Olá {cliente.nomecliente},\n\nSua solicitação foi respondida.\n\nSua descrição do chamado: {cliente.descricao}\n\n\n\nResposta: {resposta_texto}\n\nAtenciosamente,\nEquipe de suporte'
            email = EmailMultiAlternatives(subject, message, from_email, [to_email])
            email.send()
    
        
        return redirect('/')