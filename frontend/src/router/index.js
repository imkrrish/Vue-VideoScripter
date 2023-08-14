import { createRouter, createWebHistory } from "vue-router";

import UploadVideo from "../components/UploadVideo.vue";
import AddSubtitles from "../components/AddSubtitles.vue";
import VideoPlayer from "../components/VideoPlayer.vue";
import HomePage from "../components/HomePage.vue";

const routes = [
  {
    path: "/",
    name: "HomePage",
    component: HomePage,
  },
  {
    path: "/upload-video",
    name: "UploadVideo",
    component: UploadVideo,
  },
  {
    path: "/video-player/:video_id",
    name: "VideoPlayer",
    component: VideoPlayer,
  },
  {
    path: "/add-subtitles/:video_id",
    name: "AddSubtitles",
    component: AddSubtitles,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
