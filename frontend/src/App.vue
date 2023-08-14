<template>
  <!-- <router-link to="/upload-video">UploadVideo</router-link> -->
  <!-- <router-link to="/add-subtitles">AddSubtitles</router-link> -->
  <router-view></router-view>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
body {
  background-color: #f5f8ff;
}
</style>
