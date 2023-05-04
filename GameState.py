import copy


class GameState():
    def __init__(self):
        self.playerAi = {1: (0, 0), 2: (0, 2), 3: (6, 4), 4: (6, 6)}
        self.playerHuman = {1: (6, 0), 2: (6, 2), 3: (0, 4), 4: (0, 6)}
        self.komsular = {}
        for i in range(7):
            for j in range(7):
                self.komsular[(i, j)] = []
        for i in range(7):
            for j in range(7):
                if 0 <= i + 1 <= 6 and 0 <= j <= 6:
                    self.komsular[(i, j)].append((i + 1, j))
                if 0 <= i - 1 <= 6 and 0 <= j <= 6:
                    self.komsular[(i, j)].append((i - 1, j))
                if 0 <= i <= 6 and 0 <= j + 1 <= 6:
                    self.komsular[(i, j)].append((i, j + 1))
                if 0 <= i <= 6 and 0 <= j - 1 <= 6:
                    self.komsular[(i, j)].append((i, j - 1))

    def clear_dead_pieces(self):
        dead_pieces_ai = self.check_dead_pieces("ai")
        dead_pieces_human = self.check_dead_pieces("human")
        for piece in dead_pieces_ai:
            self.playerAi.pop(piece, None)
        for piece in dead_pieces_human:
            self.playerHuman.pop(piece, None)
        return dead_pieces_ai, dead_pieces_human

    def get_pieces(self, str):
        if str == "ai":
            return self.playerAi
        else:
            return self.playerHuman

    def check_dead_pieces(self, str):
        if str == "ai":
            player = "ai"
            other = "human"
        else:
            player = "human"
            other = "ai"

        dead_pieces = []
        for piece in self.get_pieces(player):
            x, y = self.get_pieces(player)[piece]
            horizontal_death = 0
            vertical_death = 0

            upx, upy = x, y - 1
            while True:
                if upy < 0:
                    vertical_death += 1
                    break
                elif (upx, upy) in self.get_pieces(other).values():
                    vertical_death += 1
                    break
                elif (upx, upy) in self.get_pieces(str).values():
                    upy = upy - 1
                else:
                    break

            downx, downy = x, y + 1
            while True:
                if downy >= 7:
                    vertical_death += 1
                    break
                elif (downx, downy) in self.get_pieces(other).values():
                    vertical_death += 1
                    break
                elif (downx, downy) in self.get_pieces(str).values():
                    downy = downy + 1
                else:
                    break

            leftx, lefty = x - 1, y
            while True:
                if leftx < 0:
                    horizontal_death += 1
                    break
                elif (leftx, lefty) in self.get_pieces(other).values():
                    horizontal_death += 1
                    break
                elif (leftx, lefty) in self.get_pieces(str).values():
                    leftx = leftx - 1
                else:
                    break

            rightx, righty = x + 1, y
            while True:
                if rightx >= 7:
                    horizontal_death += 1
                    break
                elif (rightx, righty) in self.get_pieces(other).values():
                    horizontal_death += 1
                    break
                elif (rightx, righty) in self.get_pieces(str).values():
                    rightx = rightx + 1
                else:
                    break

            if horizontal_death == 2 or vertical_death == 2:
                dead_pieces.append(piece)
        return dead_pieces

    def move_ai(self):
        move , state = findBestMove(self.playerAi, self.playerHuman, self.komsular)
        playerAi, playerHuman = state
        for m in move:
            self.playerAi[m[0]] = m[1]
        dead_pieces_ai, dead_pieces_human = self.clear_dead_pieces()

        return move, dead_pieces_ai, dead_pieces_human

    def ai_score(self):
        return scoreAi(self.playerAi, self.playerHuman)

    def human_score(self):
        return scoreHuman(self.playerAi, self.playerHuman)

    def game_winner(self):
        if len(self.playerAi) == 0 and len(self.playerHuman) > 0:
            return "Human"
        elif len(self.playerHuman) == 0 and len(self.playerAi) > 0:
            return "AI"
        elif len(self.playerHuman) == 0 and len(self.playerAi) == 0:
            return "tie"
        else:
            return "continue"

    def get_piece_choosen(self, x, y, str):
        if str == "human":
            player = self.playerHuman
        else:
            player = self.playerAi
        for p in player:
            if player[p] == (x, y):
                return p
        return None

    def get_moves_allowable(self, str):
        if str == "human":
            player = self.playerHuman
        else:
            player = self.playerAi
        if len(player) >= 2:
            return 2
        else:
            return len(player)

    def get_piece_values(self, str):
        if str == "human":
            return self.playerHuman.values()
        else:
            return self.playerAi.values()

    def possible_moves(self, piece, str):
        if str == "human":
            player = self.playerHuman
        else:
            player = self.playerAi

        x, y = player[piece]
        move_list = []
        upx, upy = x, y - 1

        if 0 <= upx < 7 and 0 <= upy < 7:
            if (upx, upy) not in self.get_all_pieces():
                move_list.append((upx, upy))

        downx, downy = x, y + 1
        if 0 <= downx < 7 and 0 <= downy < 7:
            if (downx, downy) not in self.get_all_pieces():
                move_list.append((downx, downy))

        leftx, lefty = x - 1, y
        if 0 <= leftx < 7 and 0 <= lefty < 7:
            if (leftx, lefty) not in self.get_all_pieces():
                move_list.append((leftx, lefty))

        rightx, righty = x + 1, y
        if 0 <= rightx < 7 and 0 <= righty < 7:
            if (rightx, righty) not in self.get_all_pieces():
                move_list.append((rightx, righty))

        return move_list

    def get_all_pieces(self):
        return list(self.playerHuman.values()) + list(self.playerAi.values())

def SuccessorMovesAi(playerAi, playerHuman, komsular):
    suc_moves = []
    if len(playerAi) == 1:
        for piece in playerAi:
            suc_moves += nextMoveAi(piece,playerAi, playerHuman, komsular)
        return suc_moves
    suc_moves = []
    suc_moves_set = set()
    for piece in playerAi:
        move_list = nextMoveAi(piece,playerAi, playerHuman, komsular)
        for move_state in move_list:
            for piece2 in playerAi:
                if piece != piece2:
                    move, state = move_state
                    playerAi2, playerHuman2 = state
                    if piece2 not in playerAi2:
                        continue
                    move_list2 = nextMoveAi(piece2, playerAi2, playerHuman2, komsular)
                    for move_state2 in move_list2:
                        move2, state2 = move_state2

                        if tuple(move2 + move) not in suc_moves_set:
                            suc_moves_set.add( tuple(move + move2))
                            suc_moves.append( ( move + move2, state2 )  )
    return suc_moves

def SuccessorMovesHuman(playerAi, playerHuman, komsular):
    suc_moves = []
    if len(playerHuman) == 1:
        for piece in playerHuman:
            suc_moves += nextMoveHuman(piece,playerAi, playerHuman, komsular)
        return suc_moves
    suc_moves = []
    suc_moves_set = set()
    for piece in playerHuman:
        move_list = nextMoveHuman(piece,playerAi, playerHuman, komsular)
        for move_state in move_list:
            for piece2 in playerHuman:
                if piece != piece2 :
                    move, state = move_state
                    playerAi2, playerHuman2 = state
                    if piece2 not in playerHuman2:
                        continue
                    move_list2 = nextMoveHuman(piece2, playerAi2, playerHuman2, komsular)
                    for move_state2 in move_list2:
                        move2, state2 = move_state2
                        if tuple(move2 + move) not in suc_moves_set:
                            suc_moves_set.add(tuple(move + move2))
                            suc_moves.append((move + move2, state2))
    return suc_moves

def scoreHuman(playerAi, playerHuman):
    score = 0
    if len(playerAi) == 0:
        score += 2
    if len(playerHuman) == 0:
        score -= 2
    capture_opponet_piece = 4 - len(playerAi)
    score += capture_opponet_piece * 0.5
    capture_own_piece = 4 - len(playerHuman)
    score -= capture_own_piece * 0.5
    return score

def scoreAi(playerAi, playerHuman):
    score = 0
    if len(playerHuman) == 0:
        score += 2
    if len(playerAi) == 0:
        score -= 2
    capture_opponet_piece = 4 - len(playerHuman)
    score += capture_opponet_piece * 0.5
    capture_own_piece = 4 - len(playerAi)
    score -= capture_own_piece * 0.5
    return score

def clear_dead_pieces(playerAI, playerHuman):
    dead_pieces_ai = check_dead_pieces(playerAI, playerHuman,"ai")
    dead_pieces_human = check_dead_pieces(playerAI, playerHuman,"human")
    for piece in dead_pieces_ai:
        playerAI.pop(piece, None)
    for piece in dead_pieces_human:
        playerHuman.pop(piece, None)
    return dead_pieces_ai, dead_pieces_human

def check_dead_pieces(playerAI, playerHuman, str):
    if str == "ai":
        player = playerAI
        other = playerHuman
    else:
        player = playerHuman
        other = playerAI

    dead_pieces = []
    for piece in player:
        x, y = player[piece]
        horizontal_death = 0
        vertical_death = 0

        upx, upy = x, y - 1
        while True:
            if upy < 0:
                vertical_death += 1
                break
            elif (upx, upy) in other.values():
                vertical_death += 1
                break
            elif (upx, upy) in player.values():
                upy = upy - 1
            else:
                break

        downx, downy = x, y + 1
        while True:
            if downy >= 7:
                vertical_death += 1
                break
            elif (downx, downy) in other.values():
                vertical_death += 1
                break
            elif (downx, downy) in player.values():
                downy = downy + 1
            else:
                break

        leftx, lefty = x - 1, y
        while True:
            if leftx < 0:
                horizontal_death += 1
                break
            elif (leftx, lefty) in other.values():
                horizontal_death += 1
                break
            elif (leftx, lefty) in player.values():
                leftx = leftx - 1
            else:
                break

        rightx, righty = x + 1, y
        while True:
            if rightx >= 7:
                horizontal_death += 1
                break
            elif (rightx, righty) in other.values():
                horizontal_death += 1
                break
            elif (rightx, righty) in player.values():
                rightx = rightx + 1
            else:
                break

        if horizontal_death == 2 or vertical_death == 2:
            dead_pieces.append(piece)
    return dead_pieces

def nextMoveAi(piece, playerAi, playerHuman, komsular):
    allPieces = list(playerAi.values()) + list(playerHuman.values())
    moves = []
    for komsu in komsular[playerAi[piece]]:
        if komsu not in allPieces:
            playerAi2 = dict(playerAi)
            playerHuman2 = dict(playerHuman)
            playerAi2[piece] = komsu
            for yeni_komsu in komsular[komsu]:
                if yeni_komsu in allPieces:
                    clear_dead_pieces(playerAi2,playerHuman2)
                    moves.append(( [(piece, komsu)], (playerAi2, playerHuman2)))
                    break
    return moves

def nextMoveHuman(piece, playerAi, playerHuman, komsular):
    allPieces = list(playerAi.values()) + list(playerHuman.values())
    moves = []
    for komsu in komsular[playerHuman[piece]]:
        if komsu not in allPieces:
            playerAi2 = dict(playerAi)
            playerHuman2 = dict(playerHuman)
            playerHuman2[piece] = komsu
            for yeni_komsu in komsular[komsu]:
                if yeni_komsu in allPieces:
                    clear_dead_pieces(playerAi2,playerHuman2)
                    moves.append(([(piece, komsu)], (playerAi2, playerHuman2)))
                    break
    return moves

def game_score(playerAi, playerHuman, komsular):  # evaluation function

    if len(playerHuman) == 0:
        return 9999
    if len(playerAi) == 0:
        return -9999
    #return scoreAi(playerAi, playerHuman)
    player_ai_score = scoreAi(playerAi, playerHuman)*100

    human_target_pieces = []
    all_pieces = list(playerHuman.values()) + list(playerAi.values())
    for piece in playerHuman:
        possible_moves = len(komsular[playerHuman[piece]])
        for komsu in komsular[playerHuman[piece]]:
            if komsu in all_pieces:
                possible_moves -= 1
        human_target_pieces.append((piece, possible_moves))
    human_target_pieces = sorted(human_target_pieces, key=lambda x: x[1])
    target_piece = human_target_pieces[0][0]
    ai_distance_pieces = []
    tx, ty = playerHuman[target_piece]
    for piece in playerAi:
        x, y = playerAi[piece]
        distance = abs(x - tx) + abs(y - ty)
        ai_distance_pieces.append((piece, distance))
    ai_distance_pieces = sorted(ai_distance_pieces, key=lambda x: x[1])
    min_distance = ai_distance_pieces[0][1]
    player_ai_score -= min_distance
    return player_ai_score



# def minimax(state, depth, maximizer, alpha, beta, komsular):
#     playerAi, playerHuman = state

#     if len(playerAi) == 0:
#         return -9999

#     if len(playerHuman) == 0:
#         return 9999

#     if depth == 0:
#         return game_score(playerAi, playerHuman,komsular)

#     # If this maximizer's move
#     if maximizer:
#         value = -float("inf")
#         for move_state in SuccessorMovesAi(playerAi, playerHuman, komsular):
#             move, state = move_state
#             score = minimax(state, depth - 1, False, alpha, beta, komsular)
#             value = max(value, score)
#             if value > beta:
#                 break
#             alpha = max(alpha, value)
#         return value
#     else:
#         value = float("inf")
#         for move_state in SuccessorMovesHuman(playerAi, playerHuman, komsular):
#             move, state = move_state
#             score = minimax(state, depth - 1, True, alpha, beta, komsular)
#             value = min(value,score)
#             if value < alpha:
#                 break
#             beta = min(beta, value)
#         return value


# def findBestMove(playerAi, playerHuman, komsular):
#     bestVal = -100000
#     for move_state in SuccessorMovesAi(playerAi, playerHuman, komsular):
#         move, state = move_state
#         a, h = state
#         if len(h) == 0 and len(a)>0:
#             return move_state
#         score = minimax(state, 2, False, -float("inf"), float("inf"), komsular)
#         if score > bestVal:
#             bestMove = move_state
#             bestVal = score

#     return bestMove


def minimax(state, depth, maximizer, alpha, beta, komsular):
    playerAi, playerHuman = state

    if len(playerAi) == 0:
        return -9999

    if len(playerHuman) == 0:
        return 9999

    if depth == 0:
        return game_score(playerAi, playerHuman,komsular)

    # If this maximizer's move
    if maximizer:
        value = -float("inf")
        for move_state in SuccessorMovesAi(playerAi, playerHuman, komsular):
            move, state = move_state
            score = minimax(state, depth - 1, False, alpha, beta, komsular)
            value = max(value, score)
            if value > beta:
                break
            alpha = max(alpha, value)
        return value
    else:
        value = float("inf")
        for move_state in SuccessorMovesHuman(playerAi, playerHuman, komsular):
            move, state = move_state
            score = minimax(state, depth - 1, True, alpha, beta, komsular)
            value = min(value,score)
            if value < alpha:
                break
            beta = min(beta, value)
        return value


def findBestMove(playerAi, playerHuman, komsular):
    bestVal = -100000
    for move_state in SuccessorMovesAi(playerAi, playerHuman, komsular):
        move, state = move_state
        a, h = state
        if len(h) == 0 and len(a)>0:
            return move_state
        score = minimax(state, 3, False, -float("inf"), float("inf"), komsular)
        if score > bestVal:
            bestMove = move_state
            bestVal = score

    return bestMove



