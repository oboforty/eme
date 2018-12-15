import {template} from "/js/vue/components/file-bar.vue.js"
import {store} from "/js/viewer/store.js";



export let component = Vue.component('file-bar', {
  template: template,
  data: function() {
    return {
      fs: store.fs_model,
    }
  },
  methods: {
    onClicked: function(path) {
      store.openPath(path);
    }
  },
  computed: {
    path_parts: function() {
      let parts = this.fs.vpath.split('/');

      // build up paths from parts
      let bparts = [];

      let path = '';
      for (let part of parts) {
        if (part)
          path += '/' + part;

        bparts.push({
          folder: part,
          path: path || '/'
        });
      }

      return bparts;
    }
  }
});