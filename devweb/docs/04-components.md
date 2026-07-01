# 04 - Composants : comportement attendu

## `App.vue`

Racine de l'application. Monte le layout et démarre les services au `onMounted` :
1. `checkStatus()` - vérifie si Ollama est en ligne
2. `fetchModels()` - récupère la liste des modèles disponibles
3. `setInterval` toutes les 30s - re-vérifie le statut, re-fetch les modèles si en ligne

## `Sidebar.vue`

- Largeur fixe `280px`, hauteur `100vh`, fond `surface-container-lowest`, bordure droite.
- Titre "Synthetic Intelligence" + sous-titre "Pro Model 2.1".
- Bouton **New Chat** avec animation shader WebGL + icône qui tourne à 90° au hover.
- Deux sections pliables via `SidebarSection` : **Recent Chats** et **Archive**.
- Chaque item : titre tronqué + horodatage relatif. Au hover : boutons archive/désarchiver + supprimer.
- Section courante active en `bg-primary/10 text-primary`.

## `SidebarSection.vue`

- Header cliquable : icône + label + badge compteur + chevron animé.
- Contenu expandable animé par **JS hooks Vue Transition** (height 0 → scrollHeight, ease cubic-bezier).
- Items enfants reçoivent une animation `sidebar-item-enter` avec stagger de 25ms par index.

## `TopBar.vue`

- Fixed top, `w-[calc(100%-280px)]`, `h-16`, backdrop blur.
- Gauche : "TechCorp" + dot statut Ollama (vert animé / rouge fixe).
- Droite : bouton Settings + cloche notifications.
- **Cloche** : badge pop animé au compteur, dropdown `slide-down` avec liste des erreurs système.
 - Chaque erreur : icône colorée, label, détail, horodatage, bouton dismiss.
 - Bouton "Tout effacer" si erreurs présentes.
 - `TransitionGroup name="fade"` sur les items de la liste.
- Pas d'avatar (supprimé).

## `ChatViewport.vue`

- `flex-1`, `overflow-y-auto`, `pt-24 pb-32`, `max-w-[800px] mx-auto`.
- **Empty state** : icône `auto_awesome` avec `animate-float` (flottement doux).
- **Messages** : `TransitionGroup name="msg"` - chaque message slide-up + fade spring à l'apparition.
- Scroll automatique vers le bas à chaque changement de contenu.

## `MessageUser.vue`

- Aligné à droite, fond `surface-container-high`.
- Horodatage dessous : `text-[10px] uppercase tracking-widest`.

## `MessageAI.vue`

- Bordure gauche dégradée `.ai-message-border`.
- Icône IA : spark gradient + `auto_awesome`.
- Curseur clignotant `.cursor-blink` pendant le streaming.
- **Carte d'erreur** si `message.error && message.errorType` : fond `error/5`, bordure `error/20`, icône colorée, label, détail, code.

## `InputArea.vue`

- Fixed bottom, `.glass-input` rounded-full avec shader border focus.
- **Model picker pill** : dropdown `slide-up` qui liste `availableModels`, checkmark sur l'actif, chevron animé.
- **Mic button** : anneau `.mic-ring` pulsant vers l'extérieur quand `listening`, icône FILL 1 en rouge.
- Input texte : overlay transcript interim en `text-primary/60` pendant la dictée.
- **Send button** : animation `send-sent` (bounce) au clic, `animate-spin` pendant le loading.
- Chips de prompt rapide au-dessus.

## `SettingsPanel.vue`

- Slide-in depuis la droite, `w-[480px]`, avec backdrop overlay.
- Transition `panel` (translateX + opacity).
- **5 onglets** :
 - **Connexion** : URL Ollama éditable, bouton Test (→ ok/error), bouton Sauvegarder.
 - **Modèle** : slider température (0–2), slider maxTokens (256–8192).
 - **Voix** : select langue de reconnaissance vocale, warning si Speech API non supportée.
 - **Historique** : toggle autoSave, stats sessions, export JSON, bouton clear all.
 - **À propos** : tableau stack (Vue 3, Vite, Tailwind, Ollama).

## `ShaderCanvas.vue`

Canvas WebGL réutilisable. Utilisé dans :
- Fond du bouton New Chat
- Bordure animée de l'input au focus (via `.input-shader-border`)
