# -*- coding: utf-8 -*-

def get_splitting(nant_val, cm_val, cm_minus_lim, amount):
    """


    Dans tous les exemples suivants, la limite de crédit mutuel
    est -5. C'est a dire que ma balance en Crédit Mutuel peut-être
    de -5 à la fin de l'opération.

    Voici quelques scénarios:

    - Pas d'argent sur mes 2 comptes ?, je peux quand même payer 5 car
    j'ai le droit d'utiliser jusqu'à 5 unité en crédit mutuel.
    
    >>> get_splitting(0, 0, -5, 5)
    {'possible': True, 'nant': 0, 'cm': 5}

    - Pas d'argent sur mes 2 comptes ?, je peux pas payer 6 car je
    n'ai que le droit d'utiliser jusqu'à 5 unité en crédit mutuel or
    cela ne couvrira pas les 6 unités pour compléter la transaction.

    >>> get_splitting(0, 0, -5, 6)
    {'possible': False, 'nant': 0, 'cm': 0}

    - Si j'ai un solde positif suffisant d'unité de crédit mutuels, je
    peux tout payer en unité de crédit mutuel, par exemple si je dois
    payer une transaction de 5, et que j'ai 5 unité de crédit mutuel,
    je vais payer toute la transaction avec mes crédit mutuels en
    priorité : je vais me retrouver à 0 sur ma balance de crédit
    mutuel, et ma balance de crédit Nantie ne sera pas affectée.
    
    >>> get_splitting(5, 5, -5, 5)
    {'possible': True, 'nant': 0, 'cm': 5}

    - Si mon solde de crédit mutuel est positif mais n'est pas suffisant
    pour couvrir la transaction, le compte de crédit mutuel sera vidé, et
    le reste de la transaction sera imputée au compte de monnaie nantie, en
    éspérant que j'ai assez dessus pour couvrir la transaction.

    >>> get_splitting(5, 5, -5, 10)
    {'possible': True, 'nant': 5, 'cm': 5}

    - Si je n'ai pas assez de crédit mutuel positif et de monnaie nantie, alors
    je peux puiser en crédit mutuel négatif. Jusqu'à la limite autorisée.

    >>> get_splitting(5, 5, -5, 12)
    {'possible': True, 'nant': 5, 'cm': 7}


    >>> get_splitting(5, 0, -5, 5)
    {'possible': True, 'nant': 5, 'cm': 0}



    >>> get_splitting(0, 5, -5, 5)
    {'possible': True, 'nant': 0, 'cm': 5}
    >>> get_splitting(2, 2, -5, 5)
    {'possible': True, 'nant': 2, 'cm': 3}
    >>> get_splitting(3, 3, -5, 5)
    {'possible': True, 'nant': 2, 'cm': 3}
    >>> get_splitting(2, -1, -5, 5)
    {'possible': True, 'nant': 2, 'cm': 3}
    >>> get_splitting(2, 4, -5, 5)
    {'possible': True, 'nant': 1, 'cm': 4}
    >>> get_splitting(5, 1, -5, 5)
    {'possible': True, 'nant': 4, 'cm': 1}

    """

    nant = 0
    cm = 0

    res = amount
    if cm_val > 0:
        if cm_val >= res:
            cm = res
            res = 0
        else:
            cm = cm_val
            res = res - cm_val
            cm_val = 0

    if nant_val > 0:
        if nant_val >= res:
            nant = res
            res = 0
        else:
            nant = nant_val
            res = res - nant_val
            # nant_val = 0

    if res > 0 and cm_val - cm_minus_lim >= res:
        cm = cm + res
        res = 0

    possible = res == 0
    return {'possible': possible, 'nant': nant, 'cm': cm}





Dans tous les exemples suivants, la limite de crédit mutuel
est -5. C'est a dire que ma balance en Crédit Mutuel peut-être
de -5 à la fin de l'opération.

Voici quelques scénarios:

- Pas d'argent sur mes 2 comptes ?, je peux quand même payer 5 car
j'ai le droit d'utiliser jusqu'à 5 unité en crédit mutuel.

- Pas d'argent sur mes 2 comptes ?, je peux PAS payer 6 car je
n'ai que le droit d'utiliser jusqu'à 5 unité en crédit mutuel or
cela ne couvrira pas les 6 unités pour compléter la transaction.

- Si j'ai un solde positif suffisant d'unité de crédit mutuels, je
peux tout payer en unité de crédit mutuel, par exemple si je dois
payer une transaction de 5, et que j'ai 5 unité de crédit mutuel,
je vais payer toute la transaction avec mes crédit mutuels en
priorité : je vais me retrouver à 0 sur ma balance de crédit
mutuel, et ma balance de crédit Nantie ne sera pas affectée.

- Si mon solde de crédit mutuel est positif mais n'est pas suffisant
pour couvrir la transaction, le compte de crédit mutuel sera vidé, et
le reste de la transaction sera imputée au compte de monnaie nantie, en
éspérant que j'ai assez dessus pour couvrir la transaction.

- Si je n'ai pas assez de crédit mutuel positif et de monnaie nantie, alors
je peux puiser en crédit mutuel négatif. Jusqu'à la limite autorisée.

