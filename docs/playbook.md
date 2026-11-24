# Playbook motion — l'essentiel

Résumé de « The Fable 5.2 Motion Playbook: One Prompt, One Film » (@flxrnc, 10 nov. 2026).
Les blocs de prompt sont gardés en anglais, comme dans l'original.

## Les 9 leçons

1. **Effort : High, pas Max.** Max coûte environ 3 fois plus et n'est pas plus fiable. On itère en Medium, on construit en High.
2. **Des nombres, pas des adjectifs.** « premium » devient `roughness 0.38, clearcoat 0.35`, et « smooth » devient `cubic-bezier(0.16, 1, 0.3, 1)`.
3. **Ressorts : le taux d'amortissement décide de l'atterrissage.** 1.0 pour le texte et l'UI, 0.8 pour les produits et logos, 0.5 pour les personnages.
4. **QA du mouvement.** Un modèle qui ne regarde que des images fixes laisse passer un film figé. Il faut mesurer le mouvement (freezedetect, courbe de mouvement).
5. **Finition.** Écrire le timing d'abord (`timing.json` = horloge maître), puis définir ce que « terminé » veut dire.
6. **Prompts : moins de règles, mais meilleures.** Pas de MAJUSCULES ni de « NEVER ». On nomme précisément ce qui est autorisé.
7. **Blender en script** : `blender -b --factory-startup -P script.py`, export en GLB, chargement dans three.js.
8. **Équipes d'agents** : celui qui relit ne doit pas être celui qui a construit. Les limites s'écrivent en chiffres.
9. **Coûts** : corriger sur les images fixes avant tout rendu complet, garder le cache chaud, fixer `--model` dans les scripts.

## L'idée clé : la partition est l'horloge

Une seule liste d'événements (notes, temps) pilote tout : sauts, coupes, sons.
L'image et la musique ne peuvent donc pas se décaler. Chaque son tombe **1 image après** l'événement visuel qui lui correspond.

## Le contrat (chaque film l'expose)

```js
window.renderAt = (t) => {             // draw exactly time t, in seconds
  updateEverythingFrom(t);             // no clocks, no Math.random, no accumulated state
  renderer.render(scene, camera);
};
const live = !new URLSearchParams(location.search).has("render");
if (live) renderer.setAnimationLoop(ms => renderAt((ms / 1000) % DURATION));
window.__ready = true;                 // only after fonts, models and textures load
```

## Gabarit de brief (les 10 cailloux)

```
SUBJECT   one idea per shot
TIME      8 s loop, 60 fps = 480 frames, 1920x1080
PALETTE   exact hex: background FBFAF6, ink 0E0E10, one accent D97757
TYPE      face, weight, size, tracking: Archivo 800, 96 px, -0.04 em
SHOTS     what moves, from which frame to which frame
EASING    a curve, not an adjective: cubic-bezier(0.16, 1, 0.3, 1)
HOLDS     still while it is read: 0.3 s per word + 0.5 s
BANS      glow orbs, purple gradients, fade-in on everything
QA        the stills to check before done: 0.5, 1.8, 3.0, 4.6 s
LOOP      frame 479 flows into frame 0
```

## Liste de plans

```
LENSES    35 mm room, 50 mm action, 85 mm face. Shallow depth of field.
FOCUS     follows the hero's real depth on every frame.
HERO      at least 170 px wide at 1080p in every main shot. Measure it.
CUTS      energy from cuts on the beat, never zooms or whip pans.
HOLDS     a beautiful angle lasts a whole beat.
TEXT      fully in frame or fully out. Never half cut.
ENDING    the last frame is the image. No end line under it.
```

## Valeurs de mouvement

- Entrée : `cubic-bezier(0.16, 1, 0.3, 1)`. Sortie : `cubic-bezier(0.7, 0, 0.84, 0)`, 40 à 50 % plus courte. Pop : `cubic-bezier(0.34, 1.56, 0.64, 1)`
- Retour UI : 100 à 200 ms. Révélation du héros : 600 à 900 ms
- Décalage : 1 image par lettre, 60 à 120 ms par mot, 40 à 80 ms par élément de liste
- Chevauchement : le mouvement suivant démarre à 30–50 % du précédent
- Squash & stretch : accroupi 1.2x0.75, envol 0.85x1.28, atterrissage 1.25x0.75
- Follow-through : les bras suivent avec 4 images de retard, queues et cravates avec 6
- Grille de tempo : images par temps = fps × 60 / BPM (120 BPM à 60 fps = 30 images)
- Ressorts **en forme fermée** de t, sans état accumulé d'une image à l'autre

## Bloc QA (à coller à la fin de tout prompt motion)

```
QA before you say done:
- Stills at the listed times AND a contact sheet every 0.25 s; check pose, spacing, contact.
- Measure the hero's width in pixels per shot. Under the minimum is a bug.
- Run freezedetect on a 30 fps draft. Any freeze you did not ask for is a bug.
- Plot frame-to-frame change per second; every planned move must show up as a bump.
- Seam check: frame N-1 and frame 0 must differ by less than one normal frame step.
- Seek check: render frame 300 cold and after frame 299; they must match.
Report each check with its number, not "looks good".
```

## Bloc « finishing work »

```
Finishing work: this film is done only when the full-length MP4 renders, every QA check passes
with its number, and NOTES.md lists what changed. Until then, keep going: a failed render, a
timeout, a missing font or a locked file is an ordinary obstacle, fix it and continue. Stop only
for a real blocker you can't fix, and then say exactly what you need.
```

## Export pour X

- Vidéo : H.264 High, yuv420p, 60 fps maximum, audio AAC, faststart
- Son : -14 LUFS intégré, true peak à -2 dBTP ou moins, mesuré **après** l'encodage AAC
- GIF : 15 Mo, 1280x1080 et 350 images au maximum
- Boucles : on rend les images 0 à N-1, jamais l'image N

Voir `tools/` pour le rendu, la QA et l'export.

## En cas de problème (phrase à recoller)

| Symptôme | Correction |
|---|---|
| Il s'arrête et propose de continuer | « Finishing work: done means the MP4 renders and every QA check passes with its number. Keep going. » |
| Le héros n'est qu'un point | « He is at least 170 px wide at 1080p in every main shot. Measure it per shot. » |
| Graphismes figés | « Run freezedetect on a 30 fps draft and plot change per second. Fix every freeze I did not ask for. » |
| Son en avance ou en retard | « Every sound hit is read from timing.json and lands 1 frame after its picture event. » |
| La boucle saccade | « Render frames 0 to N-1. Frame N-1 must flow into frame 0. » |
| Aperçu et rendu différents | « Every spring and motion is a closed-form function of t. » |
| Look IA par défaut | Les nommer dans une ligne `Banned:` |
