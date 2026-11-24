# Motion-Design

Atelier de films motion faits en code : **sujet → script → animation → musique → export**.

- `docs/repos.md` : les 18 outils de référence, avec leurs liens complets
- `docs/playbook.md` : les règles qui font un bon film (nombres, ressorts, QA, export)
- `tools/render.js` : rendu image par image d'un `film.html` (contrat `renderAt(t)`) vers MP4
- `tools/qa.sh` : détection des freezes et mesure de la loudness
- `tools/export_x.sh` : export compatible X

```bash
node tools/render.js films/demo/film.html 8 60
tools/qa.sh film.mp4
tools/export_x.sh film.mp4
```
