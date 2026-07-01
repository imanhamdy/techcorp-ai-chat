<template>
  <div class="absolute inset-0 overflow-hidden">
    <div class="blob b1" /><div class="blob b2" /><div class="blob b3" />
  </div>
</template>
<style scoped>
.blob { position:absolute; border-radius:50%; filter:blur(90px); animation:drift 16s ease-in-out infinite alternate; }
.b1 { width:60vw;height:60vw; background:radial-gradient(circle,#5a3ca840,transparent 70%); top:-20%;left:-10%; opacity:.25; animation-duration:18s; }
.b2 { width:45vw;height:45vw; background:radial-gradient(circle,#7c5cfc30,transparent 70%); bottom:-15%;right:-5%; opacity:.2; animation-duration:22s;animation-delay:-7s; }
.b3 { width:35vw;height:35vw; background:radial-gradient(circle,#4f8dff25,transparent 70%); top:35%;left:45%; opacity:.15; animation-duration:26s;animation-delay:-4s; }
@keyframes drift {
  0%{transform:translate(0,0) scale(1)} 33%{transform:translate(4%,6%) scale(1.08)} 66%{transform:translate(-3%,3%) scale(.95)} 100%{transform:translate(5%,-4%) scale(1.05)}
}
</style>
