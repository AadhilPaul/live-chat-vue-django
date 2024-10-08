import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import WaveUI from "wave-ui";
import "wave-ui/dist/wave-ui.css";

const app = createApp(App).use(router);
new WaveUI(app, {});

app.mount("#app");
