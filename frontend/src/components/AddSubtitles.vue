<template>
  <div class="subtitlecontainer">
    <textarea
      v-model="subtitle_text"
      placeholder="Write subtitles for your video"
      rows="40"
      name="subtitle_text"
      id="subtitle_text"
      cols="50"
      class="ui-autocomplete-input"
      autocomplete="off"
      role="textbox"
      aria-autocomplete="list"
      aria-haspopup="true"
      required
    ></textarea>
    <p v-if="isTextArea" class="error-message">Please enter a subtitle before submitting.</p>
    <!-- <button class="button" @click="submitSubtitles">Submit</button> -->

    <div class="button-container">
      <!-- upload video Button -->
      <button v-if="!submited" class="button" :disabled="submiting" @click="submitSubtitles">
        <svg xmlns="http://www.w3.org/2000/svg" width="15" height="16" viewBox="0 0 15 16">
          <path fill="currentColor" d="M12.49 7.14L3.44 2.27c-.76-.41-1.64.3-1.4 1.13l1.24 4.34c.05.18.05.36 0 .54l-1.24 4.34c-.24.83.64 1.54 1.4 1.13l9.05-4.87a.98.98 0 0 0 0-1.72Z" />
        </svg>
        Submit Subtitles
      </button>

      <!-- Next Page Button -->
      <router-link v-if="submited" :to="{ name: 'VideoPlayer', params: { video_id: video_id } }">
        <button class="button">
          <svg class="next-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
            <path fill="currentColor" d="M9.31 6.71a.996.996 0 0 0 0 1.41L13.19 12l-3.88 3.88a.996.996 0 1 0 1.41 1.41l4.59-4.59a.996.996 0 0 0 0-1.41L10.72 6.7c-.38-.38-1.02-.38-1.41.01z" />
          </svg>
          Next
        </button>
      </router-link>

      <template v-if="submiting">
        <div class="loading">
          <div class="loading-circle"></div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AddSubtitles",
  data() {
    return {
      subtitle_text: "",
      video_id: null,
      isTextArea: null,
      submiting: false,
      submited: false,
    };
  },
  mounted() {
    axios
      .get(`http://127.0.0.1:5000/video/${this.$route.params.video_id}`)
      .then((response) => {
        if (response.data) {
          this.subtitle_text = response.data;
        }
      })
      .catch((e) => {
        console.log(e);
      });
  },
  methods: {
    submitSubtitles() {
      if (this.subtitle_text.trim() === "") {
        this.isTextArea = true;
        return;
      } else {
        this.submiting = true;
        this.isTextArea = false;
        this.video_id = this.$route.params.video_id;
        const url = `http://127.0.0.1:5000/subtitle/${this.video_id}`;

        axios
          .post(url, { subtitle_text: this.subtitle_text })
          .then((response) => {
            this.submiting = false;
            this.submited = true;
            console.log("Subtitles added successfully:", response.data);
          })
          .catch((error) => {
            console.error("Error adding subtitles:", error);
          });
      }
    },
  },
};
</script>

<style scoped>
.subtitlecontainer {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.error-message {
  color: red;
  font-size: 12px;
  margin-top: 5px;
  margin-bottom: 5px;
}

textarea {
  margin-top: 10px;
  margin-bottom: 25px;
  width: 500px;
  height: 300px;
  background: none repeat scroll 0 0 #d9e1ff;
  border: 2px dashed #0c1430;
  border-radius: 6px 6px 6px 6px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.12) inset;
  font-size: 1em;
  line-height: 1.4em;
  color: #2b365f;
  font-weight: 400;
  padding: 10px;
  transition: background-color 0.2s ease 0s;
}

textarea:focus {
  background: none repeat scroll 0 0 #ffffff;
  color: #0c1430;
  outline-width: 0;
}

.button {
  background-color: #2b365f;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.button svg {
  width: 24px;
  height: 24px;
  margin-right: 10px;
}

@media (max-width: 1000px) {
  textarea {
    width: 100%;
  }
  .subtitlecontainer {
    padding: 10px;
  }
}
</style>
