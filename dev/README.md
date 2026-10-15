# GRIMLOOM — état du projet (15 oct. 2026)

Jeu mobile idle RPG dark fantasy en pixel art, inspiré de Legend of Mushroom.
Jeu en ligne : https://kristofkmaa.github.io/Grimloom/ (PWA installable).

## Fichiers
- `../index.html` (racine) = version publiée (générée, ne pas éditer à la main).
- `dev/src.html` = SOURCE du jeu (HTML/CSS/JS, images en base64). C'est ce fichier qu'on modifie.
- `dev/assemble.py` = assemble `src.html` + polices + `assets_*.js` → `dev/out/grimloom.html` (chemins relatifs au dossier `dev/`).
- `dev/build_pwa.py` = fabrique `dev/out/pwa/` (index.html + manifest + sw.js + icônes) ; avec `--publish`, copie aussi à la racine du dépôt.
- `dev/build/patch_vNN.py` = ancien historique des modifications de `src.html` (avant la vue de côté).
- `dev/build/vue_cote/p01…p08_*.py` = modifications depuis la vue de côté, à appliquer dans l'ordre (`dev/build/vue_cote/rebuild.sh` reconstruit `src.html` à partir du commit eb32ca7). Ajouter les suivantes en p09, p10…
- `dev/build/build_side.py` = découpe des planches de héros → `dev/assets_side.js`.
- `dev/build_enemy.py` = découpe une planche ChatGPT fond vert 4×3 en sprite d'ennemi.
- `dev/maquette/` = maquette de la NOUVELLE direction (vue de côté) + essai jouable + sprites découpés.

## Publication
`python3 dev/assemble.py && python3 dev/build_pwa.py --publish`, puis commit + push sur `main` → GitHub Pages se met à jour.

## Fonctionnalités en place (v18, vue de côté façon Mushroom)
- **Combat de côté** : héros fixe à gauche, familier derrière lui, démons qui arrivent de la droite sur 3 rangées ; vague finie → courte avance rapide, le décor (cimetière à la lune rouge, `tile2`) défile. Biomes 2-7 : même décor teinté.
- **Boss** : à l'étape X-10, le héros farme la dernière vague jusqu'à ce qu'on touche « Défier le boss ». Mort → repli + bouton « Défier X-Y ».
- **Disposition** : combat ~44 % avec HUD, bandeau d'étape, hubs (Invocation/Roue/Passe à gauche, Coffre de temps/7 jours à droite) et quête en surimpression ; barre de sorts ronde (AUTO = ultime automatique ON/OFF, 3 pouvoirs, ultime) ; grille 12 équipements (Arme, Casque, Épaulettes, Plastron / Gants, Ceinture, Jambières, Bottes / Anneau, Amulette, Bracelet, 12e verrouillée 5-1) + 6 artefacts (Ailes, Familier, Reliques, Pouvoirs, Monture et ??? verrouillés).
- **Coffre à clés** à la place de la forge (`chest.png`, 6 images) : cadenas sans clé, clé qui tourne, ouverture, lumière à la couleur de la rareté, tremblement dès Légendaire ; en auto l'objet file vers sa case. Marteaux → **clés**, clés de donjon de set → **tickets**, niveau de forge → **niveau du coffre** (textes, quêtes, succès, tutoriel).
- Sprites de profil intégrés : Écuyer (attente/attaque/coup + marche 8 images), Diablotin d'os, **Sorcier complet (8 formes)**, **Chevalier complet (Écuyer refait + 7 évolutions)**, **Chasseur à l'arc complet (8 formes)**. Héros de profil affichés à ×1,25 (`HSC`). Les autres formes/ennemis gardent leurs anciennes planches en attendant.
- Ajouter un héros de profil : planche ChatGPT fond vert 4×3 (marche ×4 · sort/attaque ×4 · touché ×2 + mort ×2, regard vers la droite) → `python3 dev/build/build_side.py planche.png <clé de forme>` (ex. `chev`, `h_novice`) → il apparaît tout seul en combat (`dev/assets_side.js`). `--keep-green` seulement pour une aura vraiment verte ; `--ws` quand les images se touchent (grosses auras), avec `--claim=rang,col,x0,y0,x1,y1` pour rendre une épée tendue à la bonne image (voir sfeu) ; `--aura=violet|feu|glace|sang|sacre|foudre|vert` sépare l'aura du corps : en jeu le dessin reste intact : l'aura scintille, des flammèches s'échappent de ses bords, halo et lumière au sol, liseré pulsé et cercle runique pour les formes ultimes, embrasement à chaque attaque.
- Toujours là : 3 classes et évolutions, ailes, familiers, reliques, pouvoirs, ultime, talents, donjons + raid, quêtes, succès, hub illustré, déblocages progressifs, tutoriel.

## À faire / en attente
- Plus d'amélioration d'objet (p12) : on progresse en trouvant mieux dans le coffre. Ailes de profil HD (p13-p14) : planche 4 images en ligne, fond vert, racine au bord droit → `python3 dev/build/build_wings.py planche.png corbeau|os|enfer|givre|dechu` (→ `dev/assets_wings.js`).
- Plusieurs familiers équipés (p15) : 1 emplacement, +1 aux étapes 3-1, 4-1, 5-1, 6-1 (5 max) ; chacun tire et donne son bonus.
- Chevalier au corps à corps (p16) : coup d'épée sans projectile, entaille les démons collés à la cible ; contre lui, même les démons à distance viennent au contact.
- Éclats supprimés (p11) : recycler donne de l'or, améliorer coûte seulement de l'or.
- **Retirer le mode test p09** (choix direct de n'importe quelle forme dans « Choisis ton héros ») : supprimer `dev/build/vue_cote/p09_test_formes.py` puis `rebuild.sh`.
- Icônes des 3 nouvelles pièces (épaulettes, ceinture, bracelet), 5 raretés chacune — prompt donné.
- Redessiner de profil : autres ennemis/élites/boss, ailes vues de côté.
- Icônes définitives des Épaulettes, Ceinture, Bracelet (provisoirement celles du plastron, des jambières et de l'anneau).
- Décors extérieurs des biomes 2-7. Contenu de la 12e case et de la Monture.
- Remplacer tous les assets de packs achetés (priorité), vérifier licences (icônes, audio, UI zLizard), page Crédits.
- Événement temporaire, sauvegarde en ligne, puis Android (Capacitor).

## Méthode
- Chris génère les images dans ChatGPT à partir de prompts complets ; fond vert #00FF00 pour sprites/icônes ; pixel art net, palette sombre (noir, rouge sang, or vieilli), pas trop « brillant/IA ».
- Toujours joindre une image de référence pour garder le style ; pour changer d'angle, demander une MODIFICATION d'une image existante.
- Réponses en français, concises. Pas d'idées liées au travail de Chris.
