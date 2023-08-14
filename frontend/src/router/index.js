import { createRouter, createWebHistory } from "vue-router";

import UploadVideo from "../components/UploadVideo.vue";
import AddSubtitles from "../components/AddSubtitles.vue";
import VideoPlayer from "../components/VideoPlayer.vue";

const routes = [
  {
    path: "/upload-video",
    name: "UploadVideo",
    component: UploadVideo,
  },
  {
    path: "/video-player",
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
