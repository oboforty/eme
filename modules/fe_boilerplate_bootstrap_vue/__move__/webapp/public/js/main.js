import {component as App} from '/js/example_app.js';

function init_mixins(settings, user) {
  Vue.mixin({
    settings: settings,
  });
}

export function init_app(settings, user) {
  // mixins:
  init_mixins(settings, user);

  // gui:
  let gui = new Vue({
    el: '#app-example',

    data: {
    },
    methods: {
      child: function(name) {
        return this.$refs[name];
      },
    }
  });
}
