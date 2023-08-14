<template>
  <div>
    <div class="video-container">
      <VideoPlayer ref="videoPlayer" :videoSrc="videoSource" @timeupdate="handleTimeUpdate" />
    </div>
    <p v-if="currentSubtitle">{{ currentSubtitle }}</p>
    <button v-if="!showInput && !markingEnd" @click="markTimestamp">Mark Start Timestamp</button>
    <ul>
      <li v-for="(entry, index) in timestampSubtitles" :key="index">{{ entry.start_timestamp }} -{{ entry.subtitle }} - {{ entry.end_timestamp }}</li>
    </ul>
    <div>
      <input v-if="showInput" v-model="subtitleInput" placeholder="Enter Subtitle" />
      <button v-if="!markingEnd && showInput" @click="addStartTime">Add Subtitle</button>
      <button v-if="markingEnd" @click="addEndTime">Add End Time</button>
      <button v-if="showInput" @click="cancelSubtitle">Cancel</button>
    </div>
    <button @click="submitSubtitles">Submit</button>
  </div>
</template>

<script>
import axios from "axios";
import VideoPlayer from "./VideoPlayer.vue";

export default {
  name: "AddSubtitles",
  components: {
    VideoPlayer,
  },
  data() {
    return {
      // videoSource: null,
      videoSource: `http://127.0.0.1:5000/video/${this.$route.params.video_id}/stream`,
      timestampSubtitles: [],
      showInput: false,
      subtitleInput: "",
      markedStartTime: null,
      markedEndTime: null,
      markingEnd: false,
      currentSubtitle: null,
    };
  },
  mounted() {
    axios
      .get(`http://127.0.0.1:5000/video/${this.$route.params.video_id}`)
      .then((response) => {
        if (response.data.subtitles.length != 0) {
          this.timestampSubtitles = response.data.subtitles;
        }
        console.log(response);
      })
      .catch((e) => {
        console.log(e);
      });
  },
  methods: {
    markTimestamp() {
      const videoElement = this.$refs.videoPlayer;
      if (videoElement) {
        const currentTime = videoElement.currentTime;
        if (!this.timestampSubtitles.some((entry) => entry.startTime === currentTime)) {
          this.markedStartTime = currentTime;
          this.showInput = true;
          this.markingEnd = false;
          videoElement.pause();
        }
      }
    },
    handleTimeUpdate(currentTime) {
      const matchingSubtitle = this.timestampSubtitles.find((entry) => {
        return parseFloat(entry.start_timestamp) <= currentTime && parseFloat(entry.end_timestamp) >= currentTime;
      });

      if (matchingSubtitle) {
        this.currentSubtitle = matchingSubtitle.subtitle;
      } else {
        this.currentSubtitle = null;
      }
    },
    addStartTime() {
      this.showInput = false;
      this.markingEnd = true;
      this.markedEndTime = null;
    },
    addEndTime() {
      const videoElement = this.$refs.videoPlayer;
      if (videoElement) {
        const currentTime = videoElement.currentTime;
        if (!this.timestampSubtitles.some((entry) => entry.endTime === currentTime)) {
          this.markedEndTime = currentTime;
          videoElement.pause();
        }
      }
      if (this.subtitleInput && this.markedStartTime !== null && this.markedEndTime !== null) {
        this.timestampSubtitles.push({
          start_timestamp: this.markedStartTime.toFixed(2),
          end_timestamp: this.markedEndTime.toFixed(2),
          subtitle: this.subtitleInput,
        });
        this.showInput = false;
        this.markingEnd = false;
        this.markedStartTime = null;
        this.markedEndTime = null;
        this.subtitleInput = "";
      }
    },
    cancelSubtitle() {
      this.showInput = false;
      this.markingEnd = false;
      this.markedStartTime = null;
      this.markedEndTime = null;
      this.subtitleInput = "";
    },
    submitSubtitles() {
      const subtitles = this.timestampSubtitles.map((entry) => {
        return {
          start_timestamp: parseFloat(entry.startTime),
          end_timestamp: parseFloat(entry.endTime),
          subtitle: entry.subtitle,
        };
      });

      const videoId = this.$route.params.video_id;
      const url = `http://127.0.0.1:5000/subtitle/${videoId}`;

      const requestData = { subtitles };

      axios
        .post(url, requestData)
        .then((response) => {
          console.log("Subtitles added successfully:", response.data);
        })
        .catch((error) => {
          console.error("Error adding subtitles:", error);
        });
    },
  },
};
</script>

<style scoped></style>
