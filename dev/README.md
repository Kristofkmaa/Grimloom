# GRIMLOOM — état du projet (15 oct. 2026)

Jeu mobile idle RPG dark fantasy en pixel art, inspiré de Legend of Mushroom.
Jeu en ligne : https://kristofkmaa.github.io/Grimloom/ (PWA installable).

## Fichiers
- `../index.html` (racine) = version publiée (générée, ne pas éditer à la main).
- `dev/src.html` = SOURCE du jeu (HTML/CSS/JS, images en base64). C'est ce fichier qu'on modifie.
- `dev/assemble.py` = assemble `src.html` + polices + `assets_*.js` → jeu complet.
  Chemins codés en dur à adapter : `/home/claude/grimloom/…`, `/home/claude/lune/assets2.js` (= `dev/lune_assets2.js`), `/home/claude/crypte/assets_cata.js` (= `dev/crypte_assets_cata.js`).
- `dev/build_pwa.py` = fabrique le dossier publiable (index.html + manifest + sw.js + icônes).
- `dev/build_enemy.py` = découpe une planche ChatGPT fond vert 4×3 en sprite d'ennemi.
- `dev/maquette/` = maquette de la NOUVELLE direction (vue de côté) + essai jouable + sprites découpés.

## Publication
Copier la sortie de `build_pwa.py` à la racine du dépôt, commit, push sur `main` → GitHub Pages se met à jour.

## Fonctionnalités en place (jeu actuel, vue de face 3/4)
- Forge (marteaux) + auto-forge (propose les objets meilleurs), 8 emplacements d'équipement.
- 3 classes (Chevalier, Chasseur, Sorcier) avec évolutions, ailes, familiers (gacha), reliques (gacha + autel), pouvoirs/sorts (gacha Grimoire), ultime à recharge (20 s, accélérée par les kills).
- Talents (arbre façon PoE), donjons de ressources + raid, quêtes, succès.
- Hub : Invocation, Roue, Passe de saison (100 paliers, horizontal), Coffre de temps, Connexion 7 jours — interfaces illustrées.
- Déblocages progressifs par étape avec pop-up d'explication (coffre 1-4, talents 1-6, auto 2-1, invocation+familiers 2-3, donjons 2-5, grimoire 2-8, roue 3-1, passe 3-3, reliques 3-6, ailes 4-1).
- Mise à l'échelle téléphone, panneau d'équipement rétractable (glissement + balayage), caméra resserrée quand le panneau est ouvert.
- Biome 1 (Catacombes) : ennemis, élites, boss et décor entièrement faits maison (ChatGPT). Biomes 2-7 encore sur les packs achetés.

## Direction validée pour la suite (pas encore intégrée)
Voir `dev/maquette/maquette_vue_cote.html`.
1. **Combat en vue de côté façon Mushroom** : héros fixe à gauche (petit, écran dézoomé), familier à côté, ennemis arrivent de la droite ; vague finie → le héros avance rapidement (défilement) → s'arrête → vague suivante. Boss avec bouton « Défier ».
2. **Décors extérieurs** en bande horizontale raccordable (premier : cimetière à la lune rouge, `tile2.png`).
3. **Disposition Mushroom** : combat ~44 % en haut avec hub en surimpression, barre de sorts ronde (AUTO + sorts + ultime), panneau équipement : grille 12 emplacements à gauche (Arme, Casque, Épaulettes, Plastron / Gants, Ceinture, Jambières, Bottes / Anneau, Amulette, Bracelet, 12e verrouillée étape 5-1) + 6 artefacts à droite (Ailes, Familier, Reliques, Pouvoirs, Monture à venir, ???).
4. **Coffre à la place de la forge** (6 images, `chest.png`) : fermé à cadenas sans clé, animation d'ouverture, lumière selon rareté. Marteaux → **clés** ; les anciennes « clés » de donjon à renommer (sceaux/tickets) ; niveau de forge → niveau du coffre.
5. Tout redessiner **de profil** : héros + évolutions, ennemis, effets. Faits : Écuyer (attaque/attente + marche 8 images), Diablotin d'os. La marche du héros ne plaît pas (boite) → en vue Mushroom on limite la marche (avance courte et rapide).

## À faire / en attente
- Icônes des 3 nouvelles pièces (épaulettes, ceinture, bracelet), 5 raretés chacune — prompt donné.
- Intégrer la nouvelle disposition + moteur de combat de côté dans le vrai jeu.
- Remplacer tous les assets de packs achetés (priorité), vérifier licences (icônes, audio, UI zLizard), page Crédits.
- Événement temporaire, archère à arbalète, sauvegarde en ligne, puis Android (Capacitor).

## Méthode
- Chris génère les images dans ChatGPT à partir de prompts complets ; fond vert #00FF00 pour sprites/icônes ; pixel art net, palette sombre (noir, rouge sang, or vieilli), pas trop « brillant/IA ».
- Toujours joindre une image de référence pour garder le style ; pour changer d'angle, demander une MODIFICATION d'une image existante.
- Réponses en français, concises. Pas d'idées liées au travail de Chris.
