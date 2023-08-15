<template>
  <div class="cards">
    <div v-for="item in obj.list" v-bind:key="item.video_id" class="card">
      <router-link class="svg" :to="`/video-player/${item.video_id}`">
        <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 1024 1024">
          <path
            fill="currentColor"
            d="M512 64a448 448 0 1 1 0 896a448 448 0 0 1 0-896zm0 832a384 384 0 0 0 0-768a384 384 0 0 0 0 768zm-48-247.616L668.608 512L464 375.616v272.768zm10.624-342.656l249.472 166.336a48 48 0 0 1 0 79.872L474.624 718.272A48 48 0 0 1 400 678.336V345.6a48 48 0 0 1 74.624-39.936z"
          />
        </svg>
      </router-link>

      <router-link class="link" :to="`/video-player/${item.video_id}`">
        <p>{{ item.video_name }}</p>
      </router-link>

      <div class="btncontainer">
        <!-- <button class="editButton deletebutton" @click="deleteVideo(item.video_id)">Delete</button> -->
        <router-link class="link" :to="`/add-subtitles/${item.video_id}`">
          <button class="editButton">Edit Subtitle</button>
        </router-link>
      </div>
    </div>
  </div>
  <div v-if="obj.empty" class="empty">
    <router-link class="link" to="/upload-video">
      <p class="pempty">No Video Found!</p>
      <button class="editButton">Upload Video</button>
    </router-link>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "HomePage",
  data() {
    return {
      obj: {
        list: null,
        empty: false,
        API_URI: process.env.VUE_APP_API_URI,
      },
    };
  },
  methods: {
    getList() {
      axios.get(this.obj.API_URI).then((response) => {
        this.obj.list = response.data;
        if (this.obj.list.length === 0) {
          this.obj.empty = true;
        } else {
          this.obj.empty = false;
        }
      });
    },
    deleteVideo(video_id) {
      axios
        .delete(`${this.obj.API_URI}/video/${video_id}`)
        .then((response) => {
          console.log(response.data);
          this.getList();
        })
        .catch((e) => {
          console.log(e);
        });
    },
  },
  mounted() {
    this.getList();
  },
};
</script>

<style scoped>
.pempty {
  color: #2b365f;
}

.empty {
  width: 100%;
}

.empty .editButton:hover,
.empty .editButton:active {
  color: #2b365f;
}

.link {
  text-decoration: none;
  color: white;
}
.card {
  background-color: #2b365f;
  color: white;
  padding: 1rem;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.link p {
  margin: 5px 0;
}

.cards {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-gap: 1rem;
}

.svg {
  background-color: #d9e1ff;
  border-radius: 20px;
  width: 90%;
  padding: 20px;
  color: #2b365f;
  font-size: 30px;
}

.btncontainer {
  width: 100%;
  padding: 0 5px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.editButton {
  background: #2343bc;
  border: 1px solid #2343bc;
  border-radius: 6px;
  box-shadow: rgba(0, 0, 0, 0.1) 1px 2px 4px;
  box-sizing: border-box;
  color: #fff;
  cursor: pointer;
  display: inline-block;
  font-family: nunito, roboto, proxima-nova, "proxima nova", sans-serif;
  font-size: 16px;
  font-weight: 800;
  line-height: 16px;
  min-height: 40px;
  outline: 0;
  padding: 12px 14px;
  text-align: center;
  text-rendering: geometricprecision;
  text-transform: none;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  vertical-align: middle;
}

.editButton:hover,
.editButton:active {
  background-color: initial;
  background-position: 0 0;
  color: white;
}

.editButton:active {
  opacity: 0.5;
}

.editButton.deletebutton {
  background: red;
  border: 1px solid red;
  color: white;
}

.editButton.deletebutton:hover,
.editButton.deletebutton:active {
  background-color: initial;
  background-position: 0 0;
  color: #fff;
}

@media (min-width: 600px) {
  .cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 900px) {
  .cards {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1000px) {
  .cards {
    padding: 10px;
  }
}
</style>
