# Booking box Beds24 — La Villa du Pré du Cerf

Les calendriers de disponibilités sont déjà sur les quatre pages de chambres. Ce fichier décrit la booking box, le formulaire arrivée, départ, personnes et bouton.

Chemin dans Beds24 : Settings → Booking Engine → Booking Widgets. Type : Booking Box. Une seule boîte, pour toute la maison.

Après Refresh, Get Code donne le code à intégrer sur le site. Le coller dans Beds24 ne change pas le site.

## Valeurs

| Champ | Valeur |
| --- | --- |
| Type | Booking Box |
| Propriété | La Villa du Pré du Cerf, identifiant 368230 |
| Chambre | vide, pour montrer les quatre chambres |
| Langue | Français (`fr`) |
| Premier jour | Lundi |
| Dates | Arrivée et départ |
| Format de date | `jj/mm/aaaa` |
| Jours | Di, Lu, Ma, Me, Je, Ve, Sa |
| Personnes | Adultes et enfants |
| Adultes par défaut | 2 |
| Enfants par défaut | 0 |
| Premier jour proposé | Aujourd’hui |
| Nuits par défaut | 1 |
| Minimum de nuits | 1 |
| Maximum de nuits | vide |
| Libellés | affichés |
| Titre | vide |
| Bouton | Réserver |
| Alignement | gauche |
| Largeur | 100 % |
| Cible du formulaire | nouvel onglet |
| Adresse du formulaire | `https://beds24.com/booking2.php` |
| Referer | `site` |
| Polices externes | non |
| Ombre | non |
| Fond | `#1a1814` |
| Bordure | `#cda45e` |
| Texte | `#ffffff` |
| button background-color | `#cda45e` |
| button-color | `#cda45e` |
| button text | `#0c0b09` |
| past background color | `#1a1814` |
| past color | `#6a6966` |
| available background color | `#cda45e` |
| available color | `#0c0b09` |
| unavailable background color | `#1a1814` |
| unavailable color | `#6a6966` |
| request background color | `#cda45e` |
| request color | `#0c0b09` |
| search label | vide |
| redirect URL | vide |

Laisser vides le groupe, l’identifiant propriétaire et le paramètre personnalisé. Ne pas créer de boîte pour l’Atelier du Peintre.

Les dates passées et les dates prises ont le fond brun `#1a1814` et un texte gris `#6a6966`. Les dates libres et les dates en demande ont le fond or `#cda45e` et le texte `#0c0b09` : une nuit libre se demande à la maison, les deux états se lisent pareil.

`search label` est le texte d’un lien de recherche entre plusieurs propriétés. La villa n’en a qu’une : laisser vide.

`redirect URL` est une adresse vers laquelle Beds24 renvoie l’hôte juste après le clic, une fois les dates enregistrées. Laisser vide : le formulaire ouvre déjà `https://beds24.com/booking2.php`.

## Chambres, si le formulaire demande un identifiant

| Chambre | Identifiant |
| --- | --- |
| Albert Einstein | 758046 |
| Golf Club | 758047 |
| Sous le Tilleul | 758048 |
| Café Cramique | 758049 |

Tant que l’essai Beds24 est actif, le bouton ouvre encore la page « Poser une question ».

Ce fichier est dans `assets/seo/`, exclu par `robots.txt`.
