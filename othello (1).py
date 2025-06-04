# Définition de la taille du plateau (8x8 pour Othello)
TAILLE = 8

# Les 8 directions possibles autour d'une case (horizontal, vertical, diagonales)
# Ces directions sont utilisées pour vérifier les captures de pions dans toutes les directions
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1), (0, 1),
              (1, -1), (1, 0), (1, 1)]


# Fonction pour créer et initialiser le plateau de jeu
def initialiser_plateau():
   
    plateau = [[' ' for _ in range(TAILLE)] for _ in range(TAILLE)]
    plateau[3][3], plateau[4][4] = 'O', 'O'
    plateau[3][4], plateau[4][3] = 'X', 'X'
    return plateau


# Retourne la liste des coups valides pour un joueur donné
def coups_valides(plateau, joueur):
  
    adversaire = 'O' if joueur == 'X' else 'X'
    valides = []
    for x in range(TAILLE):
        for y in range(TAILLE):
            # On ne peut jouer que sur une case vide
            if plateau[x][y] != ' ':
                continue
            # Vérifier dans chaque direction si on peut capturer des pions
            for dx, dy in DIRECTIONS:
                i, j = x + dx, y + dy
                trouvé = False
                # Tant qu'on trouve des pions adverses dans cette direction
                while 0 <= i < TAILLE and 0 <= j < TAILLE and plateau[i][j] == adversaire:
                    i += dx
                    j += dy
                    trouvé = True
                # Si on a trouvé des pions adverses et qu'ils sont suivis par un pion du joueur
                if trouvé and 0 <= i < TAILLE and 0 <= j < TAILLE and plateau[i][j] == joueur:
                    valides.append((x, y))
                    break
    return valides


# Applique un coup en retournant les pions nécessaires
def appliquer_coup(plateau, x, y, joueur):
    """
    Place un pion du joueur à la position (x,y) et retourne tous les pions
    adverses qui sont encadrés par ce coup selon les règles d'Othello.

    Args:
        plateau: État actuel du plateau de jeu
        x, y: Coordonnées où placer le pion
        joueur: Symbole du joueur qui fait le coup ('X' ou 'O')

    Modifie directement le plateau de jeu sans retourner de valeur.
    """
    adversaire = 'O' if joueur == 'X' else 'X'
    plateau[x][y] = joueur
    # Vérifier chaque direction pour les retournements
    for dx, dy in DIRECTIONS:
        i, j = x + dx, y + dy
        pions_à_retourner = []
        # Collecter tous les pions adverses consécutifs dans cette direction
        while 0 <= i < TAILLE and 0 <= j < TAILLE and plateau[i][j] == adversaire:
            pions_à_retourner.append((i, j))
            i += dx
            j += dy
        # Si on termine sur un pion du joueur, on peut retourner les pions collectés
        if 0 <= i < TAILLE and 0 <= j < TAILLE and plateau[i][j] == joueur:
            for (ix, iy) in pions_à_retourner:
                plateau[ix][iy] = joueur


# Vérifie si la partie est terminée
def est_fin_partie(plateau):
    """
    Détermine si la partie est terminée.
    La partie est terminée quand aucun des deux joueurs ne peut plus faire de coup valide.

    Args:
        plateau: État actuel du plateau de jeu

    Retourne:
        True si la partie est terminée, False sinon
    """
    return not coups_valides(plateau, 'X') and not coups_valides(plateau, 'O')


# Fonction d'évaluation
def evaluer(plateau, joueur):
    """
    Évalue la position du plateau du point de vue du joueur spécifié.
    Cette fonction simple compte la différence entre le nombre de pions
    du joueur et ceux de l'adversaire.

    Cette heuristique favorise les positions où le joueur a plus de pions que l'adversaire.
    Dans une version plus avancée, on pourrait ajouter d'autres facteurs comme
    le contrôle des coins et des bords qui ont une valeur stratégique plus importante.

    Args:
        plateau: État actuel du plateau de jeu
        joueur: Symbole du joueur pour lequel on évalue ('X' ou 'O')

    Retourne:
        Un score numérique où une valeur positive indique un avantage pour le joueur
    """
    compteur = sum(row.count(joueur) for row in plateau)
    adversaire = 'O' if joueur == 'X' else 'X'
    return compteur - sum(row.count(adversaire) for row in plateau)


# Algorithme Minimax pour choisir le meilleur coup
def minmax(plateau, profondeur, joueur, max_):
    """
    Implémentation de l'algorithme Minimax pour déterminer le meilleur coup.
    Minimax est un algorithme récursif qui simule tous les coups possibles jusqu'à
    une certaine profondeur pour choisir le coup optimal.

    En mode maximisant (max_=True), l'algorithme cherche à maximiser le score.
    En mode minimisant (max_=False), il cherche à minimiser le score.

    Args:
        plateau: État actuel du plateau de jeu
        profondeur: Nombre de coups à anticiper (plus c'est élevé, plus l'IA est forte mais lente)
        joueur: Symbole du joueur dont c'est le tour ('X' ou 'O')
        max_: Boolean indiquant si on cherche à maximiser (True) ou minimiser (False) le score

    Retourne:
        Un tuple (score, coup) où score est la valeur de la position et coup est le meilleur mouvement
    """
    # Si on atteint la profondeur 0 ou que le jeu est fini, on évalue le plateau
    if profondeur == 0 or est_fin_partie(plateau):
        return evaluer(plateau, joueur), None

    # Liste des coups possibles pour ce joueur
    coups = coups_valides(plateau, joueur)
    # Si aucun coup possible, passer au tour de l'adversaire
    if not coups:
        score, _ = minmax(plateau, profondeur-1, 'O' if joueur == 'X' else 'X', not max_)
        return score, None

    # Initialisation du meilleur score
    meilleur_score = float('-inf') if max_ else float('inf')
    meilleur_coup = None

    # On teste tous les coups possibles
    for coup in coups:
        # Copier le plateau pour ne pas modifier l'original
        copie = [ligne[:] for ligne in plateau]
        # Appliquer le coup sur la copie
        appliquer_coup(copie, coup[0], coup[1], joueur)
        # Appel récursif sur le nouveau plateau avec changement de joueur et inversion du max_
        score, _ = minmax(copie, profondeur-1, 'O' if joueur == 'X' else 'X', not max_)

        # Mise à jour du meilleur score et coup selon qu'on cherche à maximiser ou minimiser
        if (max_ and score > meilleur_score) or (not max_ and score < meilleur_score):
            meilleur_score = score
            meilleur_coup = coup

    # Retourner le meilleur score et le meilleur coup trouvé
    return meilleur_score, meilleur_coup


# Algorithme Alpha-Beta pour choisir le meilleur coup
def alpha_beta(plateau, profondeur, joueur, alpha, beta, maximisant):
    """
    Implémentation de l'algorithme Alpha-Beta, une optimisation de Minimax.
    Alpha-Beta permet d'éliminer des branches de recherche qui ne peuvent pas
    influencer la décision finale, ce qui rend l'algorithme beaucoup plus rapide.

    Args:
        plateau: État actuel du plateau de jeu
        profondeur: Nombre de coups à anticiper
        joueur: Symbole du joueur dont c'est le tour ('X' ou 'O')
        alpha: Meilleur score que le maximisant peut garantir
        beta: Meilleur score que le minimisant peut garantir
        maximisant: Boolean indiquant si on cherche à maximiser (True) ou minimiser (False)

    Retourne:
        Un tuple (score, coup) où score est la valeur de la position et coup est le meilleur mouvement
    """
    if profondeur == 0 or est_fin_partie(plateau):
        return evaluer(plateau, joueur), None

    coups = coups_valides(plateau, joueur)
    if not coups:
        score, _ = alpha_beta(plateau, profondeur - 1, 'O' if joueur == 'X' else 'X', alpha, beta, not maximisant)
        return score, None

    meilleur_coup = None

    for coup in coups:
        copie = [row[:] for row in plateau]
        appliquer_coup(copie, coup[0], coup[1], joueur)
        score, _ = alpha_beta(copie, profondeur - 1, 'O' if joueur == 'X' else 'X', alpha, beta, not maximisant)

        if maximisant:
            if score > alpha:
                alpha, meilleur_coup = score, coup
            if alpha >= beta:
                break  # Coupe alpha: cette branche ne peut pas produire un meilleur résultat
        else:
            if score < beta:
                beta, meilleur_coup = score, coup
            if beta <= alpha:
                break  # Coupe beta: cette branche ne peut pas produire un meilleur résultat

    return (alpha if maximisant else beta), meilleur_coup


# Fonction pour afficher le plateau de jeu de manière lisible
def afficher_plateau(plateau):
    """
    Affiche le plateau de jeu dans la console de manière lisible.

    Args:
        plateau: État actuel du plateau de jeu
    """
    print("  0 1 2 3 4 5 6 7")
    print(" +-+-+-+-+-+-+-+-+")
    for i in range(TAILLE):
        print(f"{i}|", end="")
        for j in range(TAILLE):
            print(f"{plateau[i][j]}|", end="")
        print("\n +-+-+-+-+-+-+-+-+")

    # Affiche le nombre de pions par joueur
    x_count = sum(row.count('X') for row in plateau)
    o_count = sum(row.count('O') for row in plateau)
    print(f"Score: X: {x_count}, O: {o_count}")


# Boucle principale du jeu
def jouer_jeu():
    """
    Fonction principale qui gère le déroulement du jeu.
    Alterne entre les tours du joueur humain et de l'IA jusqu'à la fin de la partie.
    Affiche le résultat final une fois la partie terminée.
    """
    plateau = initialiser_plateau()
    joueur_humain = 'X'  # Le joueur humain utilise les 'X'
    joueur_ia = 'O'     # L'IA utilise les 'O'
    courant = 'X'       # Le joueur X commence toujours dans Othello

    # Boucle principale du jeu
    while not est_fin_partie(plateau):
        # Afficher le plateau et les scores actuels
        afficher_plateau(plateau)
        print(f"Tour du joueur: {courant}")

        if courant == joueur_humain:
            # Tour du joueur humain
            coups = coups_valides(plateau, courant)
            if not coups:
                print("Pas de coup possible pour vous. Passage de tour.")
                courant = 'O' if courant == 'X' else 'X'
                continue

            # Afficher les coups valides
            print("Coups valides:", coups)

            # Demander au joueur de choisir un coup
            try:
                x, y = map(int, input("Entrez x y (ligne colonne): ").split())
            except ValueError:
                print("Entrée invalide. Veuillez entrer deux nombres séparés par un espace.")
                continue

            # Vérifier si le coup est valide
            if (x, y) in coups:
                appliquer_coup(plateau, x, y, courant)
            else:
                print("Coup invalide. Veuillez choisir parmi les coups disponibles.")
                continue
        else:
            # Tour de l'IA
            coups = coups_valides(plateau, courant)
            if not coups:
                print("L'IA passe son tour.")
                courant = 'O' if courant == 'X' else 'X'
                continue

            # L'IA utilise l'algorithme Alpha-Beta pour choisir son coup
            print("L'IA réfléchit...")
            # Utiliser Alpha-Beta pour de meilleures performances
            _, coup = alpha_beta(plateau, 3, courant, float('-inf'), float('inf'), True)

            if coup:
                print(f"L'IA joue en {coup}")
                appliquer_coup(plateau, coup[0], coup[1], courant)
            else:
                print("Erreur: L'IA n'a pas pu choisir de coup.")

        # Passage au joueur suivant
        courant = 'O' if courant == 'X' else 'X'

    # Fin de la partie - calculer et afficher les scores
    afficher_plateau(plateau)
    score_x = sum(row.count('X') for row in plateau)
    score_o = sum(row.count('O') for row in plateau)
    
    print(f"Fin de la partie! Score final: Vous (X): {score_x}, IA (O): {score_o}")
    
    if score_x > score_o:
        print("Vous avez gagné !")
    elif score_o > score_x:
        print("L'IA a gagné.")
    else:
        print("Égalité.")


if __name__ == '__main__':
    jouer_jeu()
