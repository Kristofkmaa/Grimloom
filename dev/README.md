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
- `dev/build_enemy.py` = ancienne découpe d'ennemi (petites cases pixel).
- `dev/build/build_enemy_hd.py planche.png <clé> [--h=hauteur] [--bg=magenta]` = ennemi de profil HD (regard à GAUCHE ; marche ×4 · attaque ×4 · touché + mort ×3) → `dev/assets_enemy.js` (ASSETS.DEMHD, fusionné par p21, dessiné lissé ; même taille affichée que l'ancienne planche).
- `dev/maquette/` = maquette de la NOUVELLE direction (vue de côté) + essai jouable + sprites découpés.

## Chargement
- `build_pwa.py` sort toutes les images du HTML en fichiers `a/<hash>.<ext>` (HTML ~3 Mo au lieu de 47). p25 : `lazyImg(url)` = image téléchargée au premier `.complete`/`.naturalWidth` (monstres, héros de profil, ailes, décors) ; `warmBiome` précharge le biome courant + suivant ; le démarrage n'attend plus que 2,5 s max. Tester la version PWA via `python3 -m http.server` dans `dev/out/pwa` (pas en file://).

## Publication
`python3 dev/assemble.py && python3 dev/build_pwa.py --publish`, puis commit + push sur `main` → GitHub Pages se met à jour.

## Fonctionnalités en place (v18, vue de côté façon Mushroom)
- **Combat de côté** : héros fixe à gauche, familier derrière lui, démons qui arrivent de la droite sur 3 rangées ; vague finie → courte avance rapide, le décor (cimetière à la lune rouge, `tile2`) défile. Biomes 2-7 : chacun son décor (p23, `dev/assets_biomes.js`, bords fondus pour la boucle).
- **Boss** : à l'étape X-10, le héros farme la dernière vague jusqu'à ce qu'on touche « Défier le boss ». Mort → repli + bouton « Défier X-Y ».
- **Disposition** : combat ~44 % avec HUD, bandeau d'étape, hubs (Invocation/Roue/Passe à gauche, Coffre de temps/7 jours à droite) et quête en surimpression ; barre de sorts ronde (AUTO = ultime automatique ON/OFF, 3 pouvoirs, ultime) ; grille 12 équipements (Arme, Casque, Épaulettes, Plastron / Gants, Ceinture, Jambières, Bottes / Anneau, Amulette, Bracelet, 12e verrouillée 5-1) + 6 artefacts (Ailes, Familier, Reliques, Pouvoirs, Monture et ??? verrouillés).
- **Coffre à clés** à la place de la forge (`chest.png`, 6 images) : cadenas sans clé, clé qui tourne, ouverture, lumière à la couleur de la rareté, tremblement dès Légendaire ; en auto l'objet file vers sa case. Marteaux → **clés**, clés de donjon de set → **tickets**, niveau de forge → **niveau du coffre** (textes, quêtes, succès, tutoriel).
- Sprites de profil intégrés : Écuyer (attente/attaque/coup + marche 8 images), Diablotin d'os, **Sorcier complet (8 formes)**, **Chevalier complet (Écuyer refait + 7 évolutions)**, **Chasseur à l'arc complet (8 formes)**. Héros de profil affichés à ×1,25 (`HSC`). Les autres formes/ennemis gardent leurs anciennes planches en attendant.
- Ajouter un héros de profil : planche ChatGPT fond vert 4×3 (marche ×4 · sort/attaque ×4 · touché ×2 + mort ×2, regard vers la droite) → `python3 dev/build/build_side.py planche.png <clé de forme>` (ex. `chev`, `h_novice`) → il apparaît tout seul en combat (`dev/assets_side.js`). `--keep-green` seulement pour une aura vraiment verte ; `--ws` quand les images se touchent (grosses auras), avec `--claim=rang,col,x0,y0,x1,y1` pour rendre une épée tendue à la bonne image (voir sfeu) ; `--aura=violet|feu|glace|sang|sacre|foudre|vert` sépare l'aura du corps : en jeu le dessin reste intact : l'aura scintille, des flammèches s'échappent de ses bords, halo et lumière au sol, liseré pulsé et cercle runique pour les formes ultimes, embrasement à chaque attaque.
- Toujours là : 3 classes et évolutions, ailes, familiers, reliques, pouvoirs, ultime, talents, donjons + raid, quêtes, succès, hub illustré, déblocages progressifs, tutoriel.

- p26 sensations : intro de boss (`bossIntro`), barre de vie + nom au-dessus du boss, micro-pause sur critique (`B.hs`), chiffres qui sautent, onde + âmes à la mort (`deathFx`), pièces vers `#goldD` (`coinFly`), flash blanc adouci pour les monstres HD.
- p27 donjons : boss nommé par donjon (`DBOSS`, boss HD du biome si dispo) avec intro, halo de couleur propre (`DCOL`) sur le décor.
- p28 : écran « Bon retour ! » (coffre de temps récolté d'un geste, via `dunScreen` + `o.btn`) ; lancement de pouvoir = onde + éclair de couleur.
- p29 : boss chronométré (`BOSS_T` = 60 s) : temps écoulé → repli et farm.
- p30 équilibrage : +3 % atk/PV par niveau ; en farm, 1 démon sur 3 donne une clé. Simulation bot : `sim.py` (scratchpad) — ×8, coffres auto, équipe, défie le boss après 90 s de farm.

## À faire / en attente
- Plus d'amélioration d'objet (p12) : on progresse en trouvant mieux dans le coffre. Ailes de profil HD (p13-p14) : planche 4 images en ligne, fond vert, racine au bord droit → `python3 dev/build/build_wings.py planche.png corbeau|os|enfer|givre|dechu` (→ `dev/assets_wings.js`).
- Plusieurs familiers équipés (p15) : 1 emplacement, +1 aux étapes 3-1, 4-1, 5-1, 6-1 (5 max) ; chacun tire et donne son bonus.
- Chevalier au corps à corps (p16) : coup d'épée sans projectile, entaille les démons collés à la cible ; contre lui, même les démons à distance viennent au contact.
- Familiers (p19) : chaque espèce a son sort (`FSPL` : Nuée de corbeaux, Morsure vampirique, Rapine, Poudre d'oubli, Vague d'ossements, Regard du vide, Spores, Toile, Éclaboussure, Feux follets, Rempart, Hurlement) ; puissance 55 % + 20 %/rareté, +20 %/étoile.
- Écran de fin de donjon / raid (p20) et messages « équipé / meilleur objet / recyclé » supprimés.
- Éclats supprimés (p11) : recycler donne de l'or, améliorer coûte seulement de l'or.
- **Retirer le mode test p09** (choix direct de n'importe quelle forme dans « Choisis ton héros ») : supprimer `dev/build/vue_cote/p09_test_formes.py` puis `rebuild.sh`.
- Icônes des 3 nouvelles pièces (épaulettes, ceinture, bracelet), 5 raretés chacune — prompt donné.
- Biome 1 complet en HD (p21) : goule, chauve-souris, crâne de feu, acolyte, garde d'os, prêtresse de sang, Démon écarlate, Bête ailée (+ diablotin d'os déjà fait). Biomes 2-7 : nouveaux monstres HD branchés par p24 (table `BHD` : pool/élites/boss/à distance, clés `bN_*`) ; un biome bascule quand toutes ses planches sont découpées. Fait : biome 2 (Ossuaire). Planches sans rangée de mort → `--anims` avec die_S:[0,1] (fondu). Fond magenta : fumées roses nettoyées automatiquement.
- Raid refait (p22) : Archidémon HD (`raid_arch`, planche fond magenta, 4e rangée « rage » via `--row4`), salle du trône (`dev/assets_raid.js` : décor + illustration de la carte), rage + bandeau à chaque palier franchi, le Chevalier peut le frapper au corps à corps.
- Icônes définitives des Épaulettes, Ceinture, Bracelet (provisoirement celles du plastron, des jambières et de l'anneau).
- Contenu de la 12e case et de la Monture.
- Remplacer tous les assets de packs achetés (priorité), vérifier licences (icônes, audio, UI zLizard), page Crédits.
- Événement temporaire, sauvegarde en ligne, puis Android (Capacitor).

## Méthode
- Chris génère les images dans ChatGPT à partir de prompts complets ; fond vert #00FF00 pour sprites/icônes ; pixel art net, palette sombre (noir, rouge sang, or vieilli), pas trop « brillant/IA ».
- Toujours joindre une image de référence pour garder le style ; pour changer d'angle, demander une MODIFICATION d'une image existante.
- Réponses en français, concises. Pas d'idées liées au travail de Chris.
