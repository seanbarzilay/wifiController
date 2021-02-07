import Vue from 'vue'
import Router from 'vue-router';
import App from './App'
import FileList from './components/FileList'
import CodeMirror from './components/CodeMirror'

import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'


Vue.use(VueMaterial);

Vue.use(Router);

const routes = [
    {path: '/', component: FileList},
    {path: '/file/:file', component: CodeMirror}
];


const router = new Router({
    mode: 'history',
    routes: routes,
});

new Vue({
    render: h => h(App),
    router
}).$mount('#app');
