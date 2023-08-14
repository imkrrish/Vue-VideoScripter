<template>
  <div class="container">
    <!-- Input Box -->
    <div class="dropfile">
      <div class="dropfileinputlabel">
        <svg class="upload-icon" xmlns="http://www.w3.org/2000/svg" width="35" height="35" viewBox="0 0 24 24">
          <path
            fill="currentColor"
            d="M19.35 10.04A7.49 7.49 0 0 0 12 4C9.11 4 6.6 5.64 5.35 8.04A5.994 5.994 0 0 0 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5c0-2.64-2.05-4.78-4.65-4.96zM14 13v4h-4v-4H7l5-5l5 5h-3z"
          />
        </svg>
        <p>Drag & Drop your video here, or click to select video</p>
      </div>
      <input class="dropfileinput" accept=".mp4, .webm, .ogg, .mkv" type="file" @change="handleFileUpload" required />
    </div>

    <!-- Preview Box -->
    <div v-if="videoFile !== null" class="dropfilepreview">
      <p class="dropfilepreviewtitle">Ready to upload</p>
      <div class="dropfilepreviewitem">
        <div class="dropfilepreviewiteminfo">
          <p class="dropfilepreviewiteminfoP">{{ videoFile.name }}</p>
          <!-- <p>{{ videoFile.size }} B</p> -->
        </div>
        <span class="dropfilepreviewitemdel" @click="removeFile">x</span>
      </div>

      <!-- Buttons -->
      <div class="button-container">
        <!-- upload video Button -->
        <button v-if="!uploaded" class="button" :disabled="uploading" @click="handleUploadButtonClick">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
            <path
              fill="currentColor"
              d="M16 4a1 1 0 0 1 1 1v4.2l5.213-3.65a.5.5 0 0 1 .787.41v12.08a.5.5 0 0 1-.787.41L17 14.8V19a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h14ZM9 8l-4 4h3v4h2v-4h3L9 8Z"
            />
          </svg>
          Upload Video
        </button>

        <!-- Next Page Button -->
        <router-link v-if="uploaded" :to="{ name: 'AddSubtitles', params: { video_id: video_id } }">
          <button class="button">
            <svg class="next-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
              <path fill="currentColor" d="M9.31 6.71a.996.996 0 0 0 0 1.41L13.19 12l-3.88 3.88a.996.996 0 1 0 1.41 1.41l4.59-4.59a.996.996 0 0 0 0-1.41L10.72 6.7c-.38-.38-1.02-.38-1.41.01z" />
            </svg>
            Next
          </button>
        </router-link>

        <template v-if="uploading">
          <div class="loading">
            <div class="loading-circle"></div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UploadVideo",
  data() {
    return {
      videoFile: null,
      uploading: false,
      uploaded: false,
      video_id: null,
    };
  },
  methods: {
    handleFileUpload(event) {
      if (event.target.files[0] !== undefined) {
        const selectedFile = event.target.files[0];
        if (selectedFile && selectedFile.type.startsWith("video/")) {
          this.videoFile = selectedFile;
        } else {
          alert("Please select a valid video file.");
          event.target.value = "";
        }
      }
    },
    removeFile() {
      this.videoFile = null;
      this.uploading = false;
      this.uploaded = false;
    },

    handleUploadButtonClick() {
      this.uploading = true;
      const formData = new FormData();
      formData.append("video", this.videoFile);
      formData.append("title", this.videoFile.name);
      axios
        .post("http://127.0.0.1:5000/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log("File uploaded successfully:", response.data);
          this.video_id = response.data.video_id;
          console.log(this.video_id);
          this.uploading = false;
          this.uploaded = true;
        })
        .catch((error) => {
          console.error("Error uploading file:", error);
        });
    },
  },
};
</script>

<style scoped>
@import "../styles/UploadVideoStyle.css";
</style>
