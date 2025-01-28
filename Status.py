from TenhouLog import get_log

def batida_ver(list):
    #Verifica se a batida foi por Ron ou Tsumo
    neg = 0
    pos = 0
    for score in list:
        if score >= 0:
            pos += 1
        else: neg += 1
    if neg == 3:
        return "tsumo"
    else:
        return "ron"

# Classe com as informações de cada jogador
class Player:
    name = ''
    sc = 0
    riichis = 0
    wins = 0
    wins_riichi = 0
    tsumos = 0
    empates = 0
    deal_in = 0
    maos_abertas = 0
    kans = 0
    uras = 0
    ganho = 0
    perdas = 0
    colocacao = 0

# Classe com as informações totais do log
class Status:
    p0 = Player()
    p1 = Player()
    p2 = Player()
    p3 = Player()
    players = [p0, p1, p2, p3]
    rodadas = 0
    empates = 0

def stats(log):
    # Pega as informações da partida pelo Tenhou
    j = get_log(log)
    partida = j['log']

    status = Status()  

    for rodada in partida:

        status.rodadas += 1

        fim_da_rodada = rodada[16]

        # Fim da rodada foi uma batida
        if fim_da_rodada[0] == "和了":
            e = 0
            #Verifica quem ganhou
            for pontuação in fim_da_rodada[1]:
                if pontuação > 0:
                    break
                else: e += 1
            #Vertifica se foi tsumo
            if batida_ver(fim_da_rodada[1]) == "tsumo":
                status.players[e].tsumos += 1
            for yaku in fim_da_rodada[2]:
                yaku = str(yaku)
                #Verifica se teve ura dora
                if yaku.startswith("裏ドラ"):
                    status.players[e].uras += 1
                if yaku.startswith("立直"):
                    status.players[e].wins_riichi += 1
            status.players[e].wins += 1
        elif fim_da_rodada[0] == "流局" or fim_da_rodada[0] == "全員不聴" or fim_da_rodada[0] == '全員聴牌':
            status.empates += 1

        #loop para verificar info dos 4 jogadores
        for i in range(4):
            #Ignora empates com ganho 0 (Todas em tenpai e todos sem tenpai)
            if fim_da_rodada[0] != '全員不聴' and fim_da_rodada[0] != '全員聴牌':
                if fim_da_rodada[1][i] >= 0:
                    status.players[i].ganho += fim_da_rodada[1][i]
                # Nos status de mahjong, desconsideram perdas, por tsumo e empate. Só Deus sabe o porque.
                elif fim_da_rodada[1][i] < 0 and batida_ver(fim_da_rodada[1]) == 'ron' and fim_da_rodada[0] == "和了": 
                    p = fim_da_rodada[1][i] * -1
                    status.players[i].perdas +=p

            #Booleans de verificação
            v_riichi = False
            v_aberto = False
            # Uma matemática que pula os descartes para a de um jogador para o outro.
            index = 6 + (3 * i)
            #Descarte do jogador
            descarte = rodada[index]
            for peca in descarte:
                if str(peca).startswith('r') and v_riichi == False:
                    status.players[i].riichis +=1
                    v_riichi = True
                if 'k' in str(peca) or 'a' in str(peca):
                    status.players[i].kans +=1

            #Compra do jogador
            index = (5 + (3 * i))
            compra = rodada[index]
            for peca in compra:
                if 'c' in str(peca) or 'p' in str(peca) or 'm' in str(peca):
                    if v_aberto == False:
                        status.players[i].maos_abertas +=1
                        v_aberto = True
                if 'm' in str(peca):
                    status.players[i].kans += 1
            #conta as vitorias com riichi
            if v_riichi == True and fim_da_rodada[0] == "和了" and fim_da_rodada[1][i] > 0:
                status.players[i].wins_riichi += 1
            #Quantidade de empates ganhos
            if fim_da_rodada[0] == '全員聴牌': status.players[i].empates += 1
            if fim_da_rodada[0] == "流局" and fim_da_rodada[1][i] > 0: status.players[i].empates += 1
            if fim_da_rodada[0] == "和了" and fim_da_rodada[1][i] < 0 and batida_ver(fim_da_rodada[1]) == "ron": status.players[i].deal_in += 1
    #Lista temporaria com a pontuação
    aux = []
    for i in range(4):
        idx = 1 + (i * 2)
        aux.append(j['sc'][idx])

    aux.sort(reverse=True)
    #Adiciona nome, pontuação e colocação
    for i in range(4):
        idx = 1 + (i * 2)

        status.players[i].name = j['name'][i]
        status.players[i].sc = j['sc'][idx-1] 

        if j['sc'][idx] == aux[0]:
            status.players[i].colocacao = 1
        elif j['sc'][idx] == aux[1]:
            status.players[i].colocacao = 2
        elif j['sc'][idx] == aux[2]:
            status.players[i].colocacao = 3
        elif j['sc'][idx] == aux[3]:
            status.players[i].colocacao = 4

    return status

if __name__ == '__main__':
    j = stats("2025012808gm-0089-0000-196735cc")
    for i in range(4):
        print(j.players[i].name, j.players[i].sc, j.players[i].colocacao)
            