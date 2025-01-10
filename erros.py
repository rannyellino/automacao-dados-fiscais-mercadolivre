
async def err(message, tipo):

    if tipo == 'Dados':
        msg = "Houve um erro na validação dos dados recebidos"
    if tipo == 'Token':
        msg = "Token de segurança do Google foi expirado"
    if tipo == 'Desconhecido':
        msg = "Houve um erro ainda não catalogado"

    err_msg = f"Erro: {tipo}, Menssagem: {msg}"

    return await message.channel.send(str(err_msg))