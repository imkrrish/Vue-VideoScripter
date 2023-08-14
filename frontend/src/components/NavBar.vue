<template>
  <div>
    <nav>
      <div class="logo"><router-link to="/">VideoScripter</router-link></div>
      <ul>
        <li><router-link :class="{ active: $route.path === '/' }" to="/">Home</router-link></li>
        <li><router-link :class="{ active: $route.path === '/upload-video' }" to="/upload-video">UploadVideo</router-link></li>
      </ul>
    </nav>
  </div>
</template>

<script>
export default {
  name: "NavBar",
};
</script>

<style scoped>
nav {
  display: flex;
  height: 80px;
  width: 100%;
  background: #2b365f;
  align-items: center;
  justify-content: space-between;
  padding: 0 100px 0 150px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}
nav .logo {
  color: #e3f2fd;
  font-size: 18px;
  font-weight: 500;
}
nav .logo a {
  text-decoration: none;
  color: #e3f2fd;
}
nav ul {
  display: flex;
  flex-wrap: wrap;
  list-style: none;
}
nav ul li {
  margin: 0 5px;
}
nav ul li a {
  color: #e3f2fd;
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  padding: 8px 15px;
  border-radius: 5px;
  letter-spacing: 1px;
  transition: all 0.3s ease;
}
nav ul li a.active,
nav ul li a:hover {
  color: #2b365f;
  background: #e3f2fd;
}
nav .menu-btn i {
  color: #e3f2fd;
  font-size: 22px;
  cursor: pointer;
  display: none;
}
input[type="checkbox"] {
  display: none;
}
@media (max-width: 1000px) {
  nav {
    padding: 0 40px 0 50px;
  }
}
@media (max-width: 920px) {
  nav {
    padding: 0 5px 0 10px;
  }
  nav .logo {
    font-size: 15px;
  }
  nav ul li a {
    font-size: 13px;
  }
}
</style>
