<template>
  <div class="container">
    <div class="box">
      <div class="dropfile">
        <div class="dropfileinputlabel">
          <svg class="upload-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <!-- upload icon path -->
          </svg>
          <p>Drag & Drop your file here, or click to select file</p>
        </div>
        <input class="dropfileinput" type="file" @change="handleFile" required />
      </div>
      <div v-if="excelFile !== null" class="dropfilepreview">
        <p class="dropfilepreviewtitle">Ready to upload</p>
        <div class="dropfilepreviewitem">
          <img class="dropfilepreviewitemimg" :src="xlsxIcon" alt="" />
          <div class="dropfilepreviewiteminfo">
            <p class="dropfilepreviewiteminfoP">{{ fileName }}</p>
            <p>{{ fileSize }} B</p>
          </div>
          <span class="dropfilepreviewitemdel" @click="removeFile">x</span>
        </div>
        <div class="button-container">
          <button class="button" :disabled="loading" @click="handleButtonClick">
            <template v-if="!success">
              <svg class="article-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <!-- article icon path -->
              </svg>
            </template>
            <template v-else>
              <svg class="next-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <!-- next icon path -->
              </svg>
            </template>
            {{ success ? "Next" : "Read File" }}
          </button>
          <template v-if="loading">
            <div class="loading">
              <div class="loading-circle"></div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TestComponent",
  data() {
    return {
      excelFile: null,
      success: false,
      loading: false,
      fileName: "", // Initialize with appropriate value
      fileSize: "", // Initialize with appropriate value,
      xlsxIcon: "", // Initialize with appropriate value
    };
  },
  methods: {
    handleFile() {
      // Handle file selection logic
    },
    removeFile() {
      // Remove file logic
    },
    handleButtonClick() {
      // Handle button click logic
    },
  },
};
</script>

<style scoped>
:root {
  --body-bg: #f5f8ff;
  --box-bg: #d9e1ff;
  --input-bg: #d9e1ff;
  --txt-color: #2f2d2f;
  --txt-second-color: #2b365f;
  --border-color: #0c1430;
  --box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
}

.container {
  height: auto;
  display: flex !important;
  margin-top: 2rem;
  justify-content: center;
}

.box {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.dropfile {
  position: relative;
  width: 27rem;
  height: 200px;
  border: 2px dashed var(--border-color);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--input-bg);
}

.dropfileinput {
  opacity: 0;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.dropfileinputlabel {
  text-align: center;
  color: var(--txt-second-color);
  font-weight: 600;
  padding: 10px;
}

.dropfilepreview {
  margin-top: 30px;
}

.dropfilepreviewiteminfoP {
  font-weight: 500;
}

.dropfilepreviewtitle {
  margin-bottom: 20px;
}

.dropfilepreviewitem {
  position: relative;
  width: 27rem;
  display: flex;
  margin-bottom: 10px;
  background-color: var(--input-bg);
  padding: 15px;
  border-radius: 20px;
}

.dropfilepreviewitemimg {
  width: 50px;
  margin-right: 20px;
}

.dropfilepreviewiteminfo {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.dropfilepreviewitemdel {
  background-color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  box-shadow: var(--box-shadow);
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.dropfilepreviewitem:hover .dropfilepreviewitemdel {
  opacity: 1;
}

.button-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.button {
  background-color: var(--txt-second-color);
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

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.loading-circle {
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--txt-second-color);
  border-radius: 50%;
  width: 24px;
  height: 24px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
