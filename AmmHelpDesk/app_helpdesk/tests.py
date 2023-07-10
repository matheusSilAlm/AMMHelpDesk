from django.test import TestCase

if request.method == 'POST':
        cliente = Cliente.objects.get(idcliente=idcliente)
        resposta_usuario = request.POST.get('resposta_usuario')
        cliente.resposta_usuario = resposta_usuario

        # Renderizar o template do e-mail
        context = {
            'cliente': cliente,
            'resposta_usuario': resposta_usuario,
        }
        html_message = render_to_string('pageclienteX.html', context)
        text_message = strip_tags(html_message)

        # Anexar a imagem embutida ao e-mail
        image_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'AmmLOGO.webp')
        with open(image_path, 'rb') as f:
            image_data = f.read()
        image = MIMEImage(image_data)
        image.add_header('Content-ID', '<logo_image>')
        image.add_header('Content-Disposition', 'inline', filename='AmmLOGO.webp')

        # Atualizar o conteúdo do e-mail para incluir a imagem embutida
        html_message = html_message.replace('src="logo_image"', f'src="cid:logo_image"')

        # Enviar e-mail para o cliente
        subject = f'Resposta ao seu chamado: {cliente.assunto}' 
        from_email = 'teushiftz@gmail.com'  
        to_email = cliente.email_cliente  

        email = EmailMultiAlternatives(subject, text_message, from_email, [to_email])
        email.attach_alternative(html_message, "text/html")

        # Processar o anexo enviado pelo usuário, se existir
        anexo = request.FILES.get('anexo')
        if anexo:
            email.attach(anexo.name, anexo.read(), anexo.content_type)

        email.send()
        cliente.save()
        return redirect('/')
