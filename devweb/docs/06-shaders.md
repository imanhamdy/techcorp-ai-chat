# 06 - Shaders WebGL

`ShaderCanvas.vue` encapsule cette animation. Utilisé pour le fond du bouton "New Chat" et la bordure de l'input au focus. **Utiliser les shaders tels quels.**

## Vertex shader
```glsl
attribute vec2 a_position;
attribute vec2 a_texCoord;
varying vec2 v_texCoord;
void main() {
 gl_Position = vec4(a_position, 0, 1);
 v_texCoord = a_texCoord;
}
```

## Fragment shader
```glsl
precision highp float;
varying vec2 v_texCoord;
uniform float u_time;
uniform vec2 u_resolution;
void main() {
 vec2 uv = v_texCoord;
 float t = u_time * 0.5;
 vec3 c1 = vec3(0.259, 0.522, 0.957);
 vec3 c2 = vec3(0.608, 0.447, 0.796);
 vec3 c3 = vec3(0.851, 0.396, 0.439);
 vec3 c4 = vec3(0.275, 0.824, 0.941);
 float w1 = sin(uv.x * 2.0 + t) * 0.5 + 0.5;
 float w2 = sin(uv.y * 3.0 - t * 1.2) * 0.5 + 0.5;
 float w3 = cos((uv.x + uv.y) * 1.5 + t * 0.8) * 0.5 + 0.5;
 vec3 col = mix(c1, c2, w1);
 col = mix(col, c3, w2);
 col = mix(col, c4, w3);
 gl_FragColor = vec4(col * 0.8, 1.0);
}
```
