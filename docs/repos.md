# Les 18 dépôts

Source : post de @flxrnc (Florence), 21 nov. 2026, sur x.com/flxrnc/status/2124231511499026436.
Pipeline annoncé : **sujet → script → animation → musique → export**.

| # | Outil | Rôle | Dépôt | Statut |
|---|---|---|---|---|
| 1 | huashu-motion | Films de lancement qui composent leur propre musique | https://github.com/alchaincyf/huashu-motion | à vérifier |
| 2 | anything2explainer | Un sujet → une vidéo explicative narrée | https://github.com/Vincentwei1021/anything2explainer | à vérifier |
| 3 | OpenScreen | Enregistrements d'écran façon démo soignée | https://github.com/getopenscreen/openscreen | à vérifier |
| 4 | onetake | Toute la pièce en un seul mouvement de caméra | https://github.com/feitangyuan/onetake | à vérifier |
| 5 | Lemo-Opuscar | 99 looks de film reproductibles en code | https://github.com/lemomo-ai/lemo-opuscar | à vérifier |
| 6 | EffectCraft | Boîte à outils VFX gratuite | https://github.com/storytold/effectcraft | à vérifier |
| 7 | GSAP | Timelines d'animation | https://github.com/greensock/GSAP | connu |
| 8 | Three.js | 3D dans le navigateur | https://github.com/mrdoob/three.js | connu |
| 9 | Blender MCP (mcp-for-blender) | Claude pilote Blender | https://github.com/ahujasid/mcp-for-blender | connu, mettre `DISABLE_TELEMETRY=true` |
| 10 | ComfyUI | Génération d'images IA | https://github.com/Comfy-Org/ComfyUI | connu, GPU nécessaire |
| 11 | HyperFrames | HTML → vidéo, conçu pour les agents | https://github.com/heygen-com/hyperframes | connu |
| 12 | Remotion | Vidéo en React | https://github.com/remotion-dev/remotion | connu, licence payante au-delà de 3 personnes |
| 13 | Remotion Skills | Skills officiels Remotion pour agents | https://github.com/remotion-dev/skills | connu |
| 14 | Impeccable | Passe de finition design | https://github.com/pbakaus/impeccable | connu |
| 15 | Taste Skill | Sens du style pour l'agent | https://github.com/Leonxlnx/taste-skill | à vérifier |
| 16 | Hallmark | Éviter le « look IA » | https://github.com/Nutlope/hallmark | à vérifier |
| 17 | Open Design | Studio de design IA | https://github.com/nexu-io/open-design | à vérifier |
| 18 | FFmpeg | Export MP4 | https://github.com/FFmpeg/FFmpeg | connu, installé ici |

## Installation (commandes tirées du playbook)

```bash
# Remotion
npx skills add remotion-dev/skills
claude plugin marketplace add remotion-dev/claude-code-plugin
claude plugin install remotion@remotion

# HyperFrames
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes

# GSAP
npx skills add https://github.com/greensock/gsap-skills

# Blender
/plugin marketplace add EL4CTEO/blender-skills
/plugin install blender-agent-skills@blender-agent-skills
```

## Autres outils cités dans le playbook

motion2code (reconstruit un mouvement de référence en SVG + GSAP), chrome-devtools-mcp,
claude-video (`/watch`), Mediabunny, librosa (détection du tempo), faster-whisper (sous-titres),
ai-portals, blender-skills.
